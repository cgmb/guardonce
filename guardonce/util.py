# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Shared utilities between checkguard, guard2once and once2guard."""

from __future__ import print_function
import sys
import os
import re
from fnmatch import fnmatch
from functools import partial

def guess_guard(contents):
    """
    Returns the guard, as well as the start and end indexes of the include
    guard from the start of the file, or throws ValueError if not found.
    Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*ifndef[ \t]+([\w]+)"
        + r"[ \t]*\n[ \t]*\#[ \t]*define[ \t]+\1[ \t]*$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('guard start not found')
    return (match.group(1),) + match.span()

def index_pragma_once(contents):
    """
    Returns the start and end indexes of the pragma once directive from
    the start of the file, or throws ValueError if not found. Comments
    are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*pragma[ \t]+once[ \t]*$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('pragma once not found')
    return match.span()

def index_guard_start(contents, guard_symbol):
    """
    Returns the start and end indexes of the include guard from the start of the
    file, or throws ValueError if not found. Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*ifndef[ \t]+" + guard_symbol
        + r"[ \t]*\n[ \t]*\#[ \t]*define[ \t]+" + guard_symbol + r"[ \t]*$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('guard start not found')
    return match.span()

def index_guard_end(contents):
    """
    Returns the start and end indexes of the last endif line from the
    file, or throws ValueError if not found. Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*endif([ \t]+.*|[ \t]*)$",
        re.MULTILINE)
    match = None
    for match in regex.finditer(contents):
        pass
    if not match:
        raise ValueError('guard end not found')
    return match.span()

def get_file_contents(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_file_contents(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)

def print_error(error):
    print(error, file=sys.stderr)

def is_header_file(filename):
    '''Returns true if the given file is identified as a C/C++ header file.'''
    return filename.endswith(('.h', '.hpp', '.H', '.hh'))

def is_excluded(filepath, exclusions):
    '''Returns true if the given file matches any of the exclusion patterns.'''
    return any(map(partial(fnmatch, filepath), exclusions))

def apply_to_headers(func, directory, exclusions):
    for root, dirs, files in os.walk(directory, onerror=print_error):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_header_file(filename) and not is_excluded(filepath, exclusions):
                func(filepath, filename)
