# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from .util import (quickcall, w, with_sandbox, contents_of)

guard2once = 'guardonce.guard2once'

def test_help():
    stdout, stderr, exitcode = quickcall(guard2once, '--help')
    assert_equal(stderr, '')
    assert_not_equal(stdout, '')
    assert_equal(exitcode, 0)

@with_sandbox('tests/data/utf8-bom-guard.h')
def test_utf8_with_bom_guard_stdout(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s', path)
    assert_equal(stderr, '')
    assert_equal(stdout, '')
    assert_equal(contents_of(path), contents_of('tests/data/utf8-bom-once.h'))
    assert_equal(exitcode, 0)

@with_sandbox('tests/data/utf8-bom-once.h')
def test_utf8_with_bom_once(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s', path)
    assert_equal(stderr, '')
    assert_equal(stdout, '')
    assert_equal(contents_of(path), contents_of('tests/data/utf8-bom-once.h'))
    assert_equal(exitcode, 0)

@with_sandbox('tests/data/utf8-bom-unprotected.h')
def test_utf8_with_bom_unprotected(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s', path)
    assert_equal(stderr, '')
    assert_equal(stdout, '')
    assert_equal(contents_of(path), contents_of('tests/data/utf8-bom-unprotected.h'))
    assert_equal(exitcode, 0)

@with_sandbox()
def test_file_open_error(sandbox, **kwargs):
    missing_path = os.path.join(sandbox, 'missing.h')
    stdout, stderr, exitcode = quickcall(guard2once, missing_path)
    assert_equal(stdout, '')
    assert_not_equal(stderr, '')
    assert_not_equal(exitcode, 0)

@with_sandbox('tests/data/newline-crlf-guard.h')
def test_preserves_crlf(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s', path)
    assert_equal(contents_of(path), contents_of('tests/data/newline-crlf-once.h'))
    assert_equal(stderr, '')
    assert_equal(stdout, '')
    assert_equal(exitcode, 0)

@with_sandbox('tests/data/newline-lf-guard.h')
def test_preserves_lf(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s', path)
    assert_equal(contents_of(path), contents_of('tests/data/newline-lf-once.h'))
    assert_equal(stderr, '')
    assert_equal(stdout, '')
    assert_equal(exitcode, 0)
