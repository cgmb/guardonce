# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Cordell Bloor
# Published under the MIT License

"""Create functions that generate include guard tokens from patterns."""

import os
import re
from string import capwords

class ParseState:
    Normal, Token, SingleQuote, DoubleQuote, Complete = range(5)

class ParserError(Exception):
    pass

def next_token(pattern, start):
    """
    Given a pattern string and a start index, returns the end index of the next
    token, including whitespace on either side.
    """
    state = ParseState.Normal
    index = start
    for i in range(start, len(pattern)):
        if state == ParseState.SingleQuote:
            if pattern[i] == "'":
                state = ParseState.Complete
        elif state == ParseState.DoubleQuote:
            if pattern[i] == '"':
                state = ParseState.Complete
        else:
            if pattern[i].isspace():
                if state == ParseState.Token:
                    state = ParseState.Complete
            elif pattern[i] == '|':
                break # delimits tokens
            elif pattern[i] == '"':
                if state == ParseState.Complete:
                    break # start of new token
                state = ParseState.DoubleQuote
            elif pattern[i] == "'":
                if state == ParseState.Complete:
                    break # start of new token
                state = ParseState.SingleQuote
            else:
                if state == ParseState.Complete:
                    break # start of new token
                state = ParseState.Token
        index = i

    if state in [ParseState.SingleQuote, ParseState.DoubleQuote]:
        raise ParserError('Pattern contains unclosed quote')

    return index + 1

def unquote(s):
    """
    Strips matching single and double quotes from the start and end of the
    given string.
    """
    if len(s) > 1 and ((s[0] == '"' and s[-1] == '"') or
                       (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    else:
        return s

def tokenize(pattern):
    tokens = []
    start = 0
    end = 0
    while end != len(pattern):
        end = next_token(pattern, start)
        tokens.append(pattern[start:end].strip())
        start = end
    return tokens

def trim_parents(filepath, crumbs):
    """
    Discards part of the given filepath. The base file is always kept. The
    crumbs argument specifies how many parent directories to keep. Negative
    crumb values are interpreted as relative to the total number of parents.
    """
    if crumbs < 0:
        if os.path.isabs(filepath):
            crumbs -= 1
        crumbs = max(crumbs + filepath.count(os.sep), 0)
    idx = len(filepath)
    for i in range(crumbs + 1):
        if idx >= 0:
            idx = filepath.rfind(os.sep, 0, idx)
    if idx < 0:
        return filepath
    else:
        return filepath[idx+1:]

def snake(s):
    """
    Converts an input string in PascalCase to snake_case.
    """
    snek = []
    prev_up = False
    prev_alnum = False
    for idx, c in enumerate(s):
        alnum = c.isalnum()
        up = c.isupper()
        next_up = s[idx+1].isupper() if idx+1 < len(s) else False
        if (up and not prev_up and prev_alnum and idx != 0 or
            up and prev_up and not next_up and idx != len(s)):
            snek.append('_')
        snek.append(c.lower())
        prev_alnum = alnum
        prev_up = up
    return ''.join(snek)

def pascal(s):
    """
    Converts an input string in snake_case to PascalCase. Also handles
    names containing spaces... god help you if you actually need that.
    """
    return capwords(s.replace('_',' ')).replace(' ','')

def sanitize(s):
    """
    Removes characters that are not allowed in macro names. Anything
    that's not alphanumeric is replaced with underscore.
    """
    return re.sub(r"\W", '_', s)

class Args:
    """
    An enum representing all arguments that can be passed to functions.
    """
    (Replace, ReplaceWith, AppendWith, PrependWith, SurroundWith,
        PathCrumbs, Remove, TrimParentsBy) = range(1,9)

def compile_pattern(pattern):
    """
    Takes a pattern specification as a string, and returns a function that
    turns a file context into an include guard.
    """
    sources = ['name','path']

    chain = []
    function = None
    expected_arg = None
    optional_arg = False
    args = []
    raw = False

    tokens = tokenize(pattern)
    if not tokens:
        raise ParserError('Pattern is empty')
    elif tokens[0] not in sources:
        raise ParserError('First function in pattern must be a source')
    elif tokens[-1] == '|':
        raise ParserError('Pattern ends with pipe to nowhere')

    for token in tokens:
        if raw:
            raise ParserError('Raw function is a sink and must be last')

        if not expected_arg:
            if not function:
                function = token
            elif token == '|':
                function = None
            else:
                raise ParserError('Unexpected argument "%s" in pattern' % token)

            if token == 'name':
                chain.append(lambda ctx, s: ctx.filename)
            elif token == 'path':
                expected_arg = Args.PathCrumbs
                optional_arg = True
            elif token == 'upper':
                chain.append(lambda ctx, s: s.upper())
            elif token == 'lower':
                chain.append(lambda ctx, s: s.lower())
            elif token == 'snake':
                chain.append(lambda ctx, s: snake(s))
            elif token == 'pascal':
                chain.append(lambda ctx, s: pascal(s))
            elif token == 'remove':
                expected_arg = Args.Remove
            elif token == 'replace':
                expected_arg = Args.Replace
            elif token == 'append':
                expected_arg = Args.AppendWith
            elif token == 'prepend':
                expected_arg = Args.PrependWith
            elif token == 'surround':
                expected_arg = Args.SurroundWith
            elif token == 'parents':
                expected_arg = Args.TrimParentsBy
            elif token == 'raw':
                raw = True
            elif token != '|':
                raise ParserError('Unknown function "%s" in pattern' % token)
        elif token == '|':
            if optional_arg:
                function = None
                if expected_arg == Args.PathCrumbs:
                    chain.append(lambda ctx, s: ctx.filepath)
                    expected_arg = None
                    optional_arg = False
            else:
                raise ParserError('Missing argument from "%s" in pattern' % function)
        elif expected_arg == Args.Remove:
            chain.append(lambda ctx, s, t=unquote(token): s.replace(t, ''))
            expected_arg = None
        elif expected_arg == Args.Replace:
            expected_arg = Args.ReplaceWith
            args.append(unquote(token))
        elif expected_arg == Args.ReplaceWith:
            chain.append(lambda ctx, s, f=args[0], t=unquote(token): s.replace(f, t))
            expected_arg = None
            args = []
        elif expected_arg == Args.AppendWith:
            chain.append(lambda ctx, s, suffix=unquote(token): s + suffix)
            expected_arg = None
        elif expected_arg == Args.PrependWith:
            chain.append(lambda ctx, s, prefix=unquote(token): prefix + s)
            expected_arg = None
        elif expected_arg == Args.SurroundWith:
            chain.append(lambda ctx, s, arg=unquote(token): arg + s + arg)
            expected_arg = None
        elif expected_arg == Args.TrimParentsBy:
            try:
                crumbs = int(token)
            except ValueError:
                raise ParserError('Invalid argument "%s" given to parents must be an integer' % token)
            chain.append(lambda ctx, s, crumbs=crumbs: trim_parents(s, crumbs))
            expected_arg = None
        elif expected_arg == Args.PathCrumbs:
            try:
                crumbs = int(token)
            except ValueError:
                raise ParserError('Invalid argument "%s" given to path; must be an integer' % token)
            chain.append(lambda ctx, s, crumbs=crumbs: trim_parents(ctx.filepath, crumbs))
            expected_arg = None
            optional_arg = False

    if optional_arg:
        if expected_arg == Args.PathCrumbs:
            chain.append(lambda ctx, s: ctx.filepath)
    elif expected_arg:
        raise ParserError('Missing argument from "%s" in pattern' % function)

    def process(ctx):
        s = ''
        for fn in chain:
            s = fn(ctx, s)
        return s if raw else sanitize(s)
    return process
