# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from .util import (quickcall, w, with_sandbox)

checkguard = 'guardonce.checkguard'

def test_help():
    stdout, stderr, exitcode = quickcall(checkguard, '--help')
    assert_equal(stderr, '')
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

@with_sandbox()
def test_file_open_error(sandbox, **kwargs):
    missing_path = os.path.join(sandbox, 'missing.h')
    stdout, stderr, exitcode = quickcall(checkguard, missing_path)
    assert_equal(stdout, '')
    assert_not_equal(stderr, '')
    assert_not_equal(exitcode, 0)

def test_cp1252_guard():
    path = 'tests/data/cp1252-guard.h'
    stdout, stderr, exitcode = quickcall(checkguard, '-o guard', path)
    assert_equal(stdout, w(''))
    assert_equal(stderr, '')
    assert_equal(exitcode, 0)
