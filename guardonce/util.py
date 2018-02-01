# -*- coding: utf-8 -*-
# Copyright (C) 2016-2018 Cordell Bloor
# Published under the MIT License

"""Shared utilities between checkguard, guard2once and once2guard."""

from __future__ import print_function
import sys
import os
import re
from fnmatch import fnmatch
from functools import partial
from itertools import islice

py2 = sys.version_info < (3,)

def ends_with_blank_line(contents):
    """
    Returns true if the given string ends with a line that is either empty or
    only composed of whitespace.
    """
    return re.search('\n\s*\n\Z', contents) is not None

def next_nonempty_line(contents, start):
    """
    Returns the index of the first character of the next line containing
    non-whitespace characters, or returns len(contents) if there is no such
    line.
    """
    line_end = len(contents) - 1
    for i, c in enumerate(islice(contents, start, None), start):
        if c == '\n':
           line_end = i
        elif c not in ' \t':
           break
    return line_end + 1

def next_line(contents, start):
    """
    Returns the index of the first character of the next line, or returns
    len(contents) if there is no next line.
    """
    for i, c in enumerate(islice(contents, start, None), start):
        if c == '\n':
           return i + 1
    return len(contents)

def guess_guard(contents):
    """
    Returns the guard, as well as the start and end indexes of the include
    guard from the start of the file, or throws ValueError if not found.
    Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*ifndef[ \t]+([\w]+)"
        + r"[ \t]*\n[ \t]*\#[ \t]*define[ \t]+\1([ \t]+1)?[ \t]*$",
        re.MULTILINE)
    guard_found = False
    for match in regex.finditer(contents):
        # if it matches our regex, it's probably a guard, but check
        # that there's some content within to be a little more sure
        nextline_start = next_nonempty_line(contents, match.end())
        nextline_end = next_line(contents, nextline_start)
        try:
            index_guard_end(contents, nextline_start, nextline_end)
        except ValueError as e:
            guard_found = True
            break
    if not guard_found:
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
        + r"[ \t]*\n[ \t]*\#[ \t]*define[ \t]+" + guard_symbol
        + r"([ \t]+1)?[ \t]*$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('guard start not found')
    return match.span()

def index_guard_end(contents, pos=0, endpos=None):
    """
    Returns the start and end indexes of the last endif line from the
    file, or throws ValueError if not found. Comments are not supported.
    """
    if endpos is None:
        endpos = len(contents)
    regex = re.compile(r"^[ \t]*\#[ \t]*endif([/ \t]+.*|[ \t]*)$",
        re.MULTILINE)
    match = None
    for match in regex.finditer(contents, pos, endpos):
        pass
    if not match:
        raise ValueError('guard end not found')
    return match.span()

class FileMetadata:
    """
    Information about a file's encoding and line endings.
    """
    def __init__(self):
        self.bom = False
        self.crlf = False

bom = '\xef\xbb\xbf' if py2 else '\ufeff'
open_kwargs = {} if py2 else {'encoding':'utf8'}

def process_input(contents):
    """
    Analyse file contents and strip bom if necessary.
    """
    metadata = FileMetadata()
    if contents.startswith(bom):
        contents = contents[len(bom):]
        metadata.bom = True
    return (contents, metadata);

def get_file_contents(filename):
    if filename is None:
        return process_input(sys.stdin.read())
    with open(filename, 'r', **open_kwargs) as f:
        return process_input(f.read())

def process_output(contents, metadata):
    """
    Prepend bom if necessary.
    """
    if metadata.bom:
        contents = bom + contents
    return contents

def write_file_contents(filename, contents, metadata):
    if filename is None:
        return sys.stdout.write(process_output(contents, metadata))
    with open(filename, 'w', **open_kwargs) as f:
        return f.write(process_output(contents, metadata))

def print_error(error):
    print(error, file=sys.stderr)

def is_header_file(filename):
    '''Returns true if the given file is identified as a C/C++ header file.'''
    return filename.endswith(('.h', '.hpp', '.H', '.hh', '.hxx'))

def is_excluded(filepath, exclusions):
    '''Returns true if the given file matches any of the exclusion patterns.'''
    return any(map(partial(fnmatch, filepath), exclusions))

def apply_to_headers(func, directory, exclusions):
    for root, dirs, files in os.walk(directory, onerror=print_error):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_header_file(filename) and not is_excluded(filepath, exclusions):
                func(filepath, filename)
