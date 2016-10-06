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

def guessGuard(contents):
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

def indexPragmaOnce(contents):
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

def indexGuardStart(contents, guardSymbol):
    """
    Returns the start and end indexes of the include guard from the start of the
    file, or throws ValueError if not found. Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*ifndef[ \t]+" + guardSymbol
        + r"[ \t]*\n[ \t]*\#[ \t]*define[ \t]+" + guardSymbol + r"[ \t]*$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('guard start not found')
    return match.span()

def indexGuardEnd(contents):
    """
    Returns the start and end indexes of the last endif line from the
    file, or throws ValueError if not found. Comments are not supported.
    """
    regex = re.compile(r"^[ \t]*\#[ \t]*endif([ \t]+.*|[ \t]*)$",
        re.MULTILINE)
    match = regex.search(contents)
    if not match:
        raise ValueError('guard end not found')
    return match.span()

def getFileContents(fileName):
    with open(fileName, 'r') as f:
        return f.read()

def writeFileContents(fileName, contents):
    with open(fileName, 'w') as f:
        f.write(contents)

def printError(error):
    print(error, file=sys.stderr)

def isHeaderFile(fileName):
    '''Returns true if the given file is identified as a C/C++ header file.'''
    return fileName.endswith(('.h', '.hpp', '.H', '.hh'))

def isExcluded(filePath, exclusions):
    '''Returns true if the given file matches any of the exclusion patterns.'''
    return any(map(partial(fnmatch, filePath), exclusions))

def applyToHeaders(func, directory, exclusions):
    for root, dirs, files in os.walk(directory, onerror=printError):
        for fileName in files:
            filePath = os.path.join(root, fileName)
            if isHeaderFile(fileName) and not isExcluded(filePath, exclusions):
                func(filePath, fileName)
