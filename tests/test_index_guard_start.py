# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.checkguard as go

def test_ok():
    contents = '''
#ifndef MATCH_H
#define MATCH_H
'''
    s,e = go.indexGuardStart(contents, 'MATCH_H')
    assert_equals(s, 1)
    assert_equals(e, 32)

def test_ok_space_before_hash():
    contents = '''
 #ifndef MATCH_H
#define MATCH_H
'''
    s,e = go.indexGuardStart(contents, 'MATCH_H')
    assert_equals(s, 1)
    assert_equals(e, 33)

def test_ok_space_after_hash():
    contents = '''
# ifndef MATCH_H
# define MATCH_H
'''
    s,e = go.indexGuardStart(contents, 'MATCH_H')
    assert_equals(s, 1)
    assert_equals(e, 34)

@raises(ValueError)
def test_bad_symbol_string():
    contents = '''
#ifndef MATCH_H
#define MATCH_H
'''
    go.indexGuardStart(contents, 'MISMATCH_H')

@raises(ValueError)
def test_bad_symbol_substring():
    contents = '''
#ifndef MISMATCH_H
#define MISMATCH_H
'''
    go.indexGuardStart(contents, 'STRING_H')

@raises(ValueError)
def test_no_ifndef():
    contents = '''
#ifdef MATCH_H
#define MATCH_H
'''
    go.indexGuardStart(contents, 'MATCH_H')

@raises(ValueError)
def test_no_define():
    contents = '''
#ifndef MATCH_H
#defne MATCH_H
'''
    go.indexGuardStart(contents, 'MATCH_H')

@raises(ValueError)
def test_mismatched_define_symbol():
    contents = '''
#ifndef MATCH_H
#define MISMATCH_H
'''
    go.indexGuardStart(contents, 'MATCH_H')

@raises(ValueError)
def test_extra_junk_on_ifndef():
    contents = '''
#ifndef MATCH_H WEIRD_HUH
#define MATCH_H
'''
    go.indexGuardStart(contents, 'MATCH_H')

@raises(ValueError)
def test_extra_junk_on_define():
    contents = '''
#ifndef MATCH_H
#define MATCH_H WEIRD_HUH
'''
    go.indexGuardStart(contents, 'MATCH_H')

def test_extra_whitespace_on_ifndef():
    contents = '''
#ifndef MATCH_H 
#define MATCH_H
'''
    s,e = go.indexGuardStart(contents, 'MATCH_H')
    assert_equals(s, 1)
    assert_equals(e, 33)

def test_extra_whitespace_on_define():
    contents = '''
#ifndef MATCH_H
#define MATCH_H 
'''
    s,e = go.indexGuardStart(contents, 'MATCH_H')
    assert_equals(s, 1)
    assert_equals(e, 33)
