# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from .util import (quickcall, w, with_sandbox, contents_of)

guard2once = 'guardonce.guard2once'

def test_help():
    stdout, stderr, exitcode = quickcall(guard2once, '--help')
    assert_equal(exitcode, 0)

@with_sandbox('tests/data/utf8-bom-guard.h')
def test_utf8_with_bom_guard_stdout(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s --stdout', path)
    assert_equal(stdout, contents_of('tests/data/utf8-bom-once.h'))

@with_sandbox('tests/data/utf8-bom-once.h')
def test_utf8_with_bom_once(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s --stdout', path)
    assert_equal(stdout, contents_of('tests/data/utf8-bom-once.h'))

@with_sandbox('tests/data/utf8-bom-unprotected.h')
def test_utf8_with_bom_unprotected(path, **kwargs):
    stdout, stderr, exitcode = quickcall(guard2once, '-s --stdout', path)
    assert_equal(stdout, contents_of('tests/data/utf8-bom-unprotected.h'))
