# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 Cordell Bloor
# Published under the MIT License

from functools import wraps
from shutil import copy2, copytree, rmtree
from subprocess import Popen, PIPE
from tempfile import mkdtemp
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

# http://youtu.be/siwpn14IE7E
def setup_danger_zone(datapath):
    """
    Create a writeable sandbox for the test to operate on.
    """
    tempdir = mkdtemp()
    fullpath = ''
    if datapath is None:
        pass
    elif os.path.isdir(datapath):
        copytree(datapath, tempdir)
    else:
        copy2(datapath, tempdir)
        fullpath = os.path.join(tempdir, os.path.basename(datapath))
    return (tempdir, fullpath)

def teardown_danger_zone(path):
    """
    Destroy the sandbox at the given path.
    """
    rmtree(path)

def with_sandbox(datapath=None):
    """
    Decorator that sets up and tears down a writable sandbox.
    """
    def decorator(fn):
        @wraps(fn)
        def setup_and_teardown(*args, **kwargs):
            sandbox_path, fullpath = setup_danger_zone(datapath)
            r = fn(*args, sandbox=sandbox_path, path=fullpath, **kwargs)
            teardown_danger_zone(sandbox_path)
            return r
        return setup_and_teardown
    return decorator

def contents_of(filename):
    with open(filename, 'rb') as f:
        return ds(f.read())

def quickcall(*args):
    cmd = [sys.executable, '-m']
    for arg in args:
        if isinstance(arg, basestring):
            cmd.extend(shlex.split(arg, False, False))
        elif isinstance(arg, collections.Sequence):
            cmd.extend(arg)
        else:
            cmd.push(str(arg))
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    ret = process.returncode
    return (ds(stdout), ds(stderr), ret)
