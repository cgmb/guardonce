# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from guardonce.pattern_compiler import *

class Context:
    pass

def test_name():
    pattern = 'name'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

def test_upper():
    pattern = 'name | upper'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'MATCH_H')

def test_lower():
    pattern = 'name | lower'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'match_h')

def test_prepend():
    pattern = 'name | prepend __'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), '__Match_h')

def test_append():
    pattern = 'name | append __'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h__')

def test_surround():
    pattern = 'name | surround __'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), '__Match_h__')

def test_replace():
    pattern = 'name | replace M W'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'Watch_h')

@raises(ParserError)
def todo_replace_too_many_characters():
    pattern = 'name | replace abc _'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def todo_replace_with_too_many_characters():
    pattern = 'name | replace a bcd'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def todo_replace_with_whitespace():
    pattern = "name | replace a ' '"
    createGuard = compilePattern(pattern)

def test_raw():
    pattern = 'name | raw'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'Match.h')

@raises(ParserError)
def todo_raw_not_last():
    pattern = 'name | raw | upper'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def todo_does_not_start_with_source():
    pattern = 'upper'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def test_replace_insufficient_args():
    pattern = 'name | replace M'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def test_replace_insufficient_args_into_pipe():
    pattern = 'name | replace M | upper'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def test_replace_too_many_args():
    pattern = 'name | replace M J K'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def test_replace_too_many_args_into_pipe():
    pattern = 'name | replace M J K | upper'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def test_bad_arg():
    pattern = 'name upper'
    createGuard = compilePattern(pattern)

@raises(ParserError)
def todo_missing_filter():
    pattern = 'name |'
    createGuard = compilePattern(pattern)
