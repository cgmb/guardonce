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

def make_regex(pattern, guard_symbol=None):
    """
    Performs a few substitutions so the pattern can use format-style
    shorthands, then compiles and returns the regex.
    """
    replacements = {
        's' : r"[ \t]", # space characters
        'guard' : guard_symbol
    }
    return re.compile(pattern.format(**replacements), re.MULTILINE)

def make_regexes(patterns, guard_symbol=None):
    """
    Yields a generator that lazily compiles the given regex patterns.
    """
    for pattern in patterns:
        yield make_regex(pattern, guard_symbol)

def guess_guard(contents):
    """
    Returns the guard, as well as the start and end indexes of the include
    guard from the start of the file, or throws ValueError if not found.
    Comments are not supported.
    """
    patterns = [
        r"^{s}*[#]{s}*ifndef{s}+(?P<guard>[\w]+){s}*\n"
            + r"{s}*[#]{s}*define{s}+(?P=guard)({s}+1)?{s}*$",
        r"^{s}*[#]{s}*if{s}*[!]{s}*defined(?:{s}+|{s}*(?P<paren>[(]){s}*)(?P<guard>[\w]+){s}*(?(paren)[)]){s}*\n"
            + r"{s}*[#]{s}*define{s}+(?P=guard)({s}+1)?{s}*$",
    ]
    for regex in make_regexes(patterns):
        for match in regex.finditer(contents):
            # if it matches our regex, it's probably a guard, but check
            # that there's some content within to be a little more sure
            nextline_start = next_nonempty_line(contents, match.end())
            nextline_end = next_line(contents, nextline_start)
            try:
                index_guard_end(contents, nextline_start, nextline_end)
            except ValueError as e:
                return (match.group('guard'),) + match.span()
    raise ValueError('guard start not found')

def index_pragma_once(contents):
    """
    Returns the start and end indexes of the pragma once directive from
    the start of the file, or throws ValueError if not found. Comments
    are not supported.
    """
    regex = make_regex(r"^{s}*\#{s}*pragma{s}+once{s}*$")
    match = regex.search(contents)
    if match:
        return match.span()
    raise ValueError('pragma once not found')

def index_guard_start(contents, guard_symbol):
    """
    Returns the start and end indexes of the include guard from the start of the
    file, or throws ValueError if not found. Comments are not supported.
    """
    patterns = [
        r"^{s}*[#]{s}*ifndef{s}+{guard}{s}*\n"
            + r"{s}*[#]{s}*define{s}+{guard}(?:{s}+1)?{s}*$",
        r"^{s}*[#]{s}*if{s}*[!]{s}*defined(?:{s}+|{s}*(?P<paren>[(]){s}*){guard}{s}*(?(paren)[)]){s}*\n"
            + r"{s}*[#]{s}*define{s}+{guard}({s}+1)?{s}*$",
    ]
    for regex in make_regexes(patterns, guard_symbol):
        match = regex.search(contents)
        if match:
            return match.span()
    raise ValueError('guard start not found')

def index_guard_end(contents, pos=0, endpos=None):
    """
    Returns the start and end indexes of the last endif line from the
    file, or throws ValueError if not found. Comments are not supported.
    """
    if endpos is None:
        endpos = len(contents)
    regex = make_regex(r"^{s}*[#]{s}*endif{s}*(?:[/][/*].*)?$")
    match = None
    for match in regex.finditer(contents, pos, endpos):
        pass
    if match:
        return match.span()
    raise ValueError('guard end not found')

class FileMetadata:
    """
    Information about a file's encoding and line endings.
    """
    def __init__(self):
        self.bom = False
        self.crlf = False

bom = b'\xef\xbb\xbf'

def ds(s):
    """
    Decodes the given byte string in Python 3.
    """
    if py2:
        return s
    return s.decode(encoding='utf-8', errors='surrogateescape')

def es(s):
    """
    Encodes the given string in Python 3.
    """
    if py2:
        return s
    return s.encode(encoding='utf-8', errors='surrogateescape')

def process_input(contents):
    """
    Analyse file contents and simplify. Strip the BOM if necessary,
    normalize line endings, and decode.
    """
    metadata = FileMetadata()
    if contents.startswith(bom):
        contents = contents[len(bom):]
        metadata.bom = True
    first_newline_idx = contents.find(b'\n')
    if first_newline_idx > 0:
        metadata.crlf = contents.startswith(b'\r', first_newline_idx-1)
        contents = contents.replace(b'\r\n', b'\n')
    contents = ds(contents)
    return (contents, metadata);

def get_file_contents(filename):
    if filename is None:
        return process_input(sys.stdin.read())
    with open(filename, 'rb') as f:
        return process_input(f.read())

def process_output(contents, metadata):
    """
    Undo the operations done in process_input to prepare contents for writing.
    """
    contents = es(contents)
    if metadata.crlf:
        contents = contents.replace(b'\n', b'\r\n')
    if metadata.bom:
        contents = bom + contents
    return contents

def write_file_contents(filename, contents, metadata):
    if filename is None:
        return sys.stdout.write(ds(process_output(contents, metadata)))
    with open(filename, 'wb') as f:
        return f.write(process_output(contents, metadata))

def is_header_file(filename):
    '''Returns true if the given file is identified as a C/C++ header file.'''
    return filename.endswith(('.h', '.hpp', '.H', '.hh', '.hxx'))

def is_excluded(filepath, exclusions):
    '''Returns true if the given file matches any of the exclusion patterns.'''
    return any(map(partial(fnmatch, filepath), exclusions))

def apply_to_headers(func, directory, exclusions):
    '''
    Apply the given function to all the header files in the given directory and
    all its subdirectories, excluding files and subdirectories matching any
    pattern in the list of exclusions.
    '''
    # Workaround for lack of nonlocal keyword in Python 2.7
    class Status:
        pass
    status = Status()
    status.ok = True

    def report_error(error):
        '''Report an error to the user, but continue processing.'''
        status.ok = False
        print(error, file=sys.stderr)

    for root, dirs, files in os.walk(directory, onerror=report_error):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_header_file(filename) and not is_excluded(filepath, exclusions):
                status.ok &= func(filepath, filename)
    return status.ok
