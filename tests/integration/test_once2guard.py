# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

import os
from nose.tools import *
from .util import (quickcall, w, with_sandbox)

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
