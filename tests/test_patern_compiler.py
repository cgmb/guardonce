# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from guardonce.pattern_compiler import *

class Context:
    pass

def test_basic():
    pattern = 'name'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'Match_h')

def test_basic_pipe():
    pattern = 'name | upper'
    createGuard = compilePattern(pattern)
    ctx = Context()
    ctx.fileName = 'Match.h'
    assert_equals(createGuard(ctx), 'MATCH_H')

@raises(ParserError)
def test_bad_arg():
    pattern = 'name upper'
    createGuard = compilePattern(pattern)
