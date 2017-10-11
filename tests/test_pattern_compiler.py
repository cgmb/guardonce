# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from guardonce.pattern_compiler import *

def windows_only(f):
    """Only execute on windows systems"""
    f.__test__ = os.name == "nt"
    return f

def unix_only(f):
    """Only execute on unix systems"""
    f.__test__ = os.name == "posix"
    return f

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

def test_path_no_arg_with_filter():
    '''Bug #19'''
    pattern = 'path | upper'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','Match.h')
    assert_equals(createGuard(ctx), 'SRC_MATCH_H')

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

def test_path_zero_arg():
    pattern = 'path 0'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'Match_h')

def test_path_negative_arg():
    pattern = 'path -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'widgets_Match_h')

def test_path_negative_big_arg():
    pattern = 'path -2'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

@unix_only
def test_path_absolute_path():
    pattern = 'path -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = '/dev/null'
    assert_equals(createGuard(ctx), 'null')

@windows_only
def test_path_absolute_path_windows():
    pattern = 'path -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = 'C:\Program Files (x86)\Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

@raises(ParserError)
def test_path_bad_arg():
    pattern = 'path lkj'
    createGuard = compile_pattern(pattern)

def test_parents_arg():
    pattern = 'path | parents 1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'widgets_Match_h')

@raises(ParserError)
def test_parents_missing_arg():
    pattern = 'path parents'
    createGuard = compile_pattern(pattern)

def test_parents_big_arg():
    pattern = 'path | parents 10'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'src_widgets_Match_h')

def test_parents_zero_arg():
    pattern = 'path | parents 0'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'Match_h')

def test_parents_negative_arg():
    pattern = 'path | parents -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = os.path.join('src','widgets','Match.h')
    assert_equals(createGuard(ctx), 'widgets_Match_h')

def test_parents_negative_big_arg():
    pattern = 'path | parents -2'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

@raises(ParserError)
def test_parents_bad_arg():
    pattern = 'path | parents lkj'
    createGuard = compile_pattern(pattern)

@unix_only
def test_parents_absolute_path():
    pattern = 'path | parents -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = '/dev/null'
    assert_equals(createGuard(ctx), 'null')

@windows_only
def test_parents_absolute_path_windows():
    pattern = 'path | parents -1'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filepath = 'C:\Program Files (x86)\Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

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

def test_remove():
    pattern = 'name | remove atch'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'M_h')

def test_replace():
    pattern = 'name | replace M W'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Watch_h')

def test_replace_multiple_characters():
    pattern = 'name | replace bunny teapot'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'bunny.h'
    assert_equals(createGuard(ctx), 'teapot_h')

def test_replace_with_whitespace():
    pattern = "name | replace a ' ' | raw"
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'M tch.h')

def test_replace_with_empty_string():
    pattern = "name | replace a '' | raw"
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Mtch.h')

@raises(ParserError)
def test_replace_with_unclosed_single_quote():
    pattern = "name | replace a ' "
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_replace_with_unclosed_double_quote():
    pattern = 'name | replace a " '
    createGuard = compile_pattern(pattern)

def test_raw():
    pattern = 'name | raw'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = 'Match.h'
    assert_equals(createGuard(ctx), 'Match.h')

@raises(ParserError)
def test_raw_not_last():
    pattern = 'name | raw | upper'
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_empty_pattern():
    pattern = ''
    createGuard = compile_pattern(pattern)

@raises(ParserError)
def test_does_not_start_with_source():
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

def test_arg_single_quote():
    pattern = "name | replace '|' W"
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = '|.h'
    assert_equals(createGuard(ctx), 'W_h')

def test_arg_double_quote():
    pattern = 'name | replace "|" W'
    createGuard = compile_pattern(pattern)
    ctx = Context()
    ctx.filename = '|.h'
    assert_equals(createGuard(ctx), 'W_h')

@raises(ParserError)
def test_missing_filter():
    pattern = 'name |'
    createGuard = compile_pattern(pattern)
