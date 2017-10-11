# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from subprocess import Popen, PIPE
import collections
import os
import shlex
import sys

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
