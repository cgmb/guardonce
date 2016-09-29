# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Create functions that generate include guard tokens from patterns."""

class ParseState:
    Normal, Token, Complete = range(3)

class ParserError(Exception):
    pass

def nextToken(pattern, startIndex):
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
        end = nextToken(pattern, start)
        tokens.append(pattern[start:end].strip())
        start = end
    return tokens

class Args:
    Replace, ReplaceWith, AppendWith, PrependWith, SurroundWith = range(1,6)

def compilePattern(pattern):
    """
    Takes a pattern specification as a string, and returns a function that
    turns a file context into an include guard.
    """
    funcs = []
    expected_arg = None
    args = []
    function = None
    for token in tokenize(pattern):
        if not expected_arg:
            if not function:
                function = token
            elif token == '|':
                function = None
            else:
                raise ParserError('Unexpected argument "%s" in pattern' % token)

            if token == 'name':
                funcs.append(lambda ctx, s: ctx.fileName)
            elif token == 'upper':
                funcs.append(lambda ctx, s: s.upper())
            elif token == 'lower':
                funcs.append(lambda ctx, s: s.lower())
            elif token == 'replace':
                expected_arg = Args.Replace
            elif token == 'append':
                expected_arg = Args.AppendWith
            elif token == 'prepend':
                expected_arg = Args.PrependWith
            elif token == 'surround':
                expected_arg = Args.SurroundWith
            elif token != '|':
                raise ParserError('Unknown function "%s" in pattern' % token)
        elif token == '|':
            raise ParserError('Missing argument from "%s" in pattern' % function)
        elif expected_arg == Args.Replace:
            expected_arg = Args.ReplaceWith
            args.append(token)
        elif expected_arg == Args.ReplaceWith:
            funcs.append(lambda ctx, s, f=args[0], t=token: s.replace(f, t))
            expected_arg = None
            args = []
        elif expected_arg == Args.AppendWith:
            funcs.append(lambda ctx, s, suffix=token: s + suffix)
            expected_arg = None
        elif expected_arg == Args.PrependWith:
            funcs.append(lambda ctx, s, prefix=token: prefix + s)
            expected_arg = None
        elif expected_arg == Args.SurroundWith:
            funcs.append(lambda ctx, s, arg=token: arg + s + arg)
            expected_arg = None

    if expected_arg:
        raise ParserError('Missing argument from "%s" in pattern' % function)

    def process(ctx):
        s = ''
        for fn in funcs:
            s = fn(ctx, s)
        return s.replace('.','_')
    return process
