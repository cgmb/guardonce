# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Create functions that generate include guard tokens from patterns."""

import re
from string import capwords

class ParseState:
    Normal, Token, Complete = range(3)

class ParserError(Exception):
    pass

def next_token(pattern, startIndex):
    """
    Given a pattern string and a startIndex, returns the end index of the next
    token, including whitespace on either side.
    """
    state = ParseState.Normal
    index = startIndex
    for i in range(startIndex, len(pattern)):
        if pattern[i].isspace():
            if state == ParseState.Token:
                state = ParseState.Complete
        elif pattern[i] == '|':
            break # always delimits tokens
        else:
            if state == ParseState.Complete:
                break # start of new token
            state = ParseState.Token
        index = i
    return index + 1

def tokenize(pattern):
    tokens = []
    start = 0
    end = 0
    while end != len(pattern):
        end = next_token(pattern, start)
        tokens.append(pattern[start:end].strip())
        start = end
    return tokens

def snake(s):
    """
    Converts an input string in PascalCase to snake_case.
    """
    snek = []
    prev_up = False
    for idx, c in enumerate(s):
        up = c.isupper()
        next_up = s[idx+1].isupper() if idx+1 < len(s) else False
        if (up and not prev_up and idx != 0 or
            up and prev_up and not next_up and idx != len(s)):
            snek.append('_')
        snek.append(c.lower())
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
    Replace, ReplaceWith, AppendWith, PrependWith, SurroundWith = range(1,6)

def compile_pattern(pattern):
    """
    Takes a pattern specification as a string, and returns a function that
    turns a file context into an include guard.
    """
    chain = []
    function = None
    expected_arg = None
    args = []
    raw = False
    for token in tokenize(pattern):
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
                chain.append(lambda ctx, s: ctx.filepath)
            elif token == 'upper':
                chain.append(lambda ctx, s: s.upper())
            elif token == 'lower':
                chain.append(lambda ctx, s: s.lower())
            elif token == 'snake':
                chain.append(lambda ctx, s: snake(s))
            elif token == 'pascal':
                chain.append(lambda ctx, s: pascal(s))
            elif token == 'replace':
                expected_arg = Args.Replace
            elif token == 'append':
                expected_arg = Args.AppendWith
            elif token == 'prepend':
                expected_arg = Args.PrependWith
            elif token == 'surround':
                expected_arg = Args.SurroundWith
            elif token == 'raw':
                raw = True
            elif token != '|':
                raise ParserError('Unknown function "%s" in pattern' % token)
        elif token == '|':
            raise ParserError('Missing argument from "%s" in pattern' % function)
        elif expected_arg == Args.Replace:
            expected_arg = Args.ReplaceWith
            args.append(token)
        elif expected_arg == Args.ReplaceWith:
            chain.append(lambda ctx, s, f=args[0], t=token: s.replace(f, t))
            expected_arg = None
            args = []
        elif expected_arg == Args.AppendWith:
            chain.append(lambda ctx, s, suffix=token: s + suffix)
            expected_arg = None
        elif expected_arg == Args.PrependWith:
            chain.append(lambda ctx, s, prefix=token: prefix + s)
            expected_arg = None
        elif expected_arg == Args.SurroundWith:
            chain.append(lambda ctx, s, arg=token: arg + s + arg)
            expected_arg = None

    if expected_arg:
        raise ParserError('Missing argument from "%s" in pattern' % function)

    def process(ctx):
        s = ''
        for fn in chain:
            s = fn(ctx, s)
        return s if raw else sanitize(s)
    return process
