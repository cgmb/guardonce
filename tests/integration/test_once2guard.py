# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from .util import (quickcall, w)

once2guard = 'guardonce.once2guard'

def test_help():
    stdout, stderr, exitcode = quickcall(once2guard, '--help')
    assert_equal(exitcode, 0)
