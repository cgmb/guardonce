# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from .util import (quickcall, w)

guard2once = 'guardonce.guard2once'

def test_help():
    stdout, stderr, exitcode = quickcall(guard2once, '--help')
    assert_equal(exitcode, 0)
