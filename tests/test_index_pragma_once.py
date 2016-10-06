# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.util as go

def test_ok():
    contents = '''
#pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 13)

def test_ok_space_before_hash():
    contents = '''
 #pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_ok_space_after_hash():
    contents = '''
# pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_ok_space_after_once():
    contents = '''
#pragma once 
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_no_newline_at_eof():
    contents = '''
#pragma once'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 13)

@raises(ValueError)
def test_no_pragma():
    contents = '''
#prama once
'''
    go.indexPragmaOnce(contents)

#def test_comment_after_once():
#    contents = '''
##pragma once /**/
#'''
#    s,e = go.indexPragmaOnce(contents)
#    assert_equals(s, 1)
#    assert_equals(e, 18)
