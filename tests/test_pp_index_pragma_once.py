# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.pp_parser as go

def test_ok():
    contents= '''
#pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 13)

def test_ok_space_before_hash():
    contents= '''
 #pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_ok_space_after_hash():
    contents= '''
# pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_ok_space_after_once():
    contents= '''
#pragma once 
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 14)

def test_no_newline_at_eof():
    contents= '''
#pragma once'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 13)

@raises(ValueError)
def test_no_pragma():
    contents= '''
#prama once
'''
    go.indexPragmaOnce(contents)

@raises(ValueError)
def test_no_once():
    contents= '''
#pragma oce
'''
    go.indexPragmaOnce(contents)

@raises(ValueError)
def test_pragma_once_in_line_comment():
    contents= '''
// #pragma once
'''
    go.indexPragmaOnce(contents)

@raises(ValueError)
def test_pragma_once_in_multiline_comment():
    contents= '''
/* #pragma once */
'''
    go.indexPragmaOnce(contents)

def test_extra_token_after_once():
    contents= '''
#pragma once aklsjdf
'''
    go.indexPragmaOnce(contents)

@raises(ValueError)
def test_extra_symobls_after_once():
    contents= '''
#pragma once +(#*@#*$
'''
    go.indexPragmaOnce(contents)

def test_comment_before_hash():
    contents= '''
/* comment */#pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 26)

def test_space_comment_before_hash():
    contents= '''
 /* comment */#pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_comment_space_before_hash():
    contents= '''
/* comment */ #pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_comment_after_hash():
    contents= '''
#/* comment */pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 26)

def test_space_comment_after_hash():
    contents= '''
# /* comment */pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_comment_space_after_hash():
    contents= '''
#/* comment */ pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_comment_after_pragma():
    contents= '''
#pragma/* comment */once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 25)

def test_space_comment_after_pragma():
    contents= '''
#pragma /* comment */once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 26)

def test_comment_space_after_pragma():
    contents= '''
#pragma/* comment */ once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 26)

def test_comment_after_once():
    contents= '''
#pragma once/* comment */
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 26)

def test_space_comment_after_once():
    contents= '''
#pragma once /* comment */
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_comment_space_after_once():
    contents= '''
#pragma once/* comment */ 
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 27)

def test_line_comment_space_after_once():
    contents= '''
#pragma once // comment
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 1)
    assert_equals(e, 24)

def test_file_content_after_once():
    contents= '''#pragma once

// https://xkcd.com/221/
inline int getRandomNumber()
{
  return 4; // chosen by fair dice roll.
            // guaranteed to be random
}
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 0)
    assert_equals(e, 12)

def test_multiline_comment_before_hash():
    contents= '''/*
*/ #pragma once
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 5)
    assert_equals(e, 18)

def test_multiline_comment_after_once():
    contents= '''#pragma once /*
*/
'''
    s,e = go.indexPragmaOnce(contents)
    assert_equals(s, 0)
    assert_equals(e, 12)
