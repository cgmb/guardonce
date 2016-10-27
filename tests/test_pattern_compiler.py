# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from guardonce.pattern_compiler import *

class Context:
    pass

def test_name():
    pattern = 'name'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

def test_path():
    pattern = 'path'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','Match.h')
    assert_equals(createGuard(ctx), 'src_Match_h')

def test_path_arg():
    pattern = 'path 1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'widgets_Match_h')

def test_path_big_arg():
    pattern = 'path 10'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'src_widgets_Match_h')

@raises(ParserError)
def test_path_bad_arg():
    pattern = 'path lkj'
    createGuard = compile_pattern(pattern)

def test_upper():
    pattern = 'name | upper'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'MATCH_H')

def test_lower():
    pattern = 'name | lower'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'match_h')

def test_snake():
    pattern = 'name | snake'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'MatchFactory.h'
    assert_equals(createGuard(ctx), 'match_factory_h')

def test_snake_acronym():
    pattern = 'name | snake'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'MatchHTTPFactory.h'
    assert_equals(createGuard(ctx), 'match_http_factory_h')

def test_snake_single_letter_word():
    pattern = 'name | snake'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'BreakAStick.h'
    assert_equals(createGuard(ctx), 'break_a_stick_h')

def test_snake_path():
    pattern = 'path 1 | snake'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('Code','CaptureContext.h')
    assert_equals(createGuard(ctx), 'code_capture_context_h')

def test_snake_symbols():
    pattern = 'name | snake | raw'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Micro$oftWord.h'
    assert_equals(createGuard(ctx), 'micro$oft_word.h')

def test_pascal():
    pattern = 'name | pascal'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'match_factory.h'
    assert_equals(createGuard(ctx), 'MatchFactory_h')

def test_prepend():
    pattern = 'name | prepend __'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), '__Match_h')

def test_append():
    pattern = 'name | append __'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h__')

def test_surround():
    pattern = 'name | surround __'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), '__Match_h__')

def test_replace():
    pattern = 'name | replace M W'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Watch_h')

@raises(ParserError)
def todo_replace_too_many_characters():
    pattern = 'name | replace abc _'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def todo_replace_with_too_many_characters():
    pattern = 'name | replace a bcd'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def todo_replace_with_whitespace():
    pattern = "name | replace a ' '"
    createGuard = compile_pattern(pattern)

def test_raw():
    pattern = 'name | raw'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Match.h')

@raises(ParserError)
def todo_raw_not_last():
    pattern = 'name | raw | upper'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def todo_does_not_start_with_source():
    pattern = 'upper'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_replace_insufficient_args():
    pattern = 'name | replace M'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_replace_insufficient_args_into_pipe():
    pattern = 'name | replace M | upper'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_replace_too_many_args():
    pattern = 'name | replace M J K'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_replace_too_many_args_into_pipe():
    pattern = 'name | replace M J K | upper'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_bad_arg():
    pattern = 'name upper'
    createGuard = compile_pattern(pattern)

def todo_arg_single_quote():
    pattern = "name | replace '|' W"
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = '|.h'
    assert_equals(createGuard(ctx), 'W_h')

def todo_arg_double_quote():
    pattern = 'name | replace "|" W'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = '|.h'
    assert_equals(createGuard(ctx), 'W_h')

@raises(ParserError)
def todo_missing_filter():
    pattern = 'name |'
    createGuard = compile_pattern(pattern)
