# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from .util import (quickcall, w)

checkguard = 'guardonce.checkguard'

def test_help():
    stdout, stderr, exitcode = quickcall(checkguard, '--help')
    assert_equal(exitcode, 0)

def test_utf8_with_bom_guard():
    path = 'tests/data/utf8-bom-guard.h'
    stdout, stderr, exitcode = quickcall(checkguard, '-o guard', path)
    assert_equal(stdout, w(''))

def test_utf8_with_bom_once():
    path = 'tests/data/utf8-bom-once.h'
    stdout, stderr, exitcode = quickcall(checkguard, '-o once', path)
    assert_equal(stdout, w(''))

def test_utf8_with_bom_unprotected():
    path = 'tests/data/utf8-bom-unprotected.h'
    stdout, stderr, exitcode = quickcall(checkguard, path)
    assert_equal(stdout, w(path))
