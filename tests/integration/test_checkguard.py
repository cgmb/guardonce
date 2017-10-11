# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from nose.tools import *
from subprocess import Popen, PIPE
import collections
import os
import shlex
import sys

checkguard = 'guardonce.checkguard'

py2 = sys.version_info < (3,)

if not py2:
    basestring = str

def ds(s):
    """
    Decodes the given byte string in Python 3
    """
    if py2:
        return s
    return s.decode()

def w(s):
    """
    Wrap a given string to be expected output
    """
    if s:
        return s + os.linesep
    return s

def quickcall(*args):
    cmd = [sys.executable, '-m']
    for arg in args:
        if isinstance(arg, basestring):
            cmd.extend(shlex.split(arg))
        elif isinstance(arg, collections.Sequence):
            cmd.extend(arg)
        else:
            cmd.push(str(arg))
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    ret = process.returncode
    return (ds(stdout), ds(stderr), ret)

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
