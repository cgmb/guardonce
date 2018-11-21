# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from .util import (quickcall, w, with_sandbox, contents_of)

once2guard = 'guardonce.once2guard'

def test_help():
    stdout, stderr, exitcode = quickcall(once2guard, '--help')
    assert_equal(stderr, '')
    assert_equal(exitcode, 0)

@with_sandbox()
def test_file_open_error(sandbox, **kwargs):
    missing_path = os.path.join(sandbox, 'missing.h')
    stdout, stderr, exitcode = quickcall(once2guard, missing_path)
    assert_equal(stdout, '')
    assert_not_equal(stderr, '')
    assert_not_equal(exitcode, 0)

@with_sandbox('tests/data/newline-crlf-once.h')
def test_preserves_crlf(sandbox, path, **kwargs):
    stdout, stderr, exitcode = quickcall(once2guard, '-lp', ['path|remove ' + path + ' |append MATCH_H'], path)
    assert_equal(stdout, '')
    assert_equal(stderr, '')
    assert_equal(exitcode, 0)
    assert_equal(contents_of(path), contents_of('tests/data/newline-crlf-guard.h'))

@with_sandbox('tests/data/newline-lf-once.h')
def test_preserves_lf(sandbox, path, **kwargs):
    stdout, stderr, exitcode = quickcall(once2guard, '-lp', ['path|remove ' + path + ' |append MATCH_H'], path)
    assert_equal(stdout, '')
    assert_equal(stderr, '')
    assert_equal(exitcode, 0)
    assert_equal(contents_of(path), contents_of('tests/data/newline-lf-guard.h'))
