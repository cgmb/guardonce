# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Find C or C++ header files with incorrect or missing include guards."""

from __future__ import print_function
import argparse
import sys
import os
import re
from fnmatch import fnmatch
from functools import partial

__version__ = "1.0.0"

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

def isProtectedByGuard(contents, guardSymbol):
    try:
        indexGuardStart(contents, guardSymbol)
        indexGuardEnd(contents)
        return True
    except ValueError:
        return False

def isProtectedByPragmaOnce(contents):
    try:
        indexPragmaOnce(contents)
        return True
    except ValueError:
        return False

def isProtected(contents, guardSymbol, options):
    return (options.guardOk and isProtectedByGuard(contents, guardSymbol)
        or options.onceOk and isProtectedByPragmaOnce(contents))

def isFileProtected(fileName, guardSymbol, options):
    contents = getFileContents(fileName)
    return isProtected(contents, guardSymbol, options)

def getFileContents(fileName):
    with open(fileName, 'r') as f:
        return f.read()

def fileNameGuardSymbol(ctx):
    return ctx.fileName.upper().replace('.', '_')

def filePathGuardSymbol(ctx):
    return ctx.filePath.upper().replace('.', '_').replace('/','_')

def processFile(filePath, guardSymbol, options):
    try:
        if not isFileProtected(filePath, guardSymbol, options):
            print(filePath)
    except Exception as e:
        print(e, file=sys.stderr)

def processFile2(filePath, fileName):
    class Context:
        pass
    ctx = Context()
    ctx.filePath = filePath
    ctx.fileName = fileName
    
    class Options:
        pass
    options = Options()
    options.guardOk = True
    options.onceOk = True

    return processFile(filePath, fileNameGuardSymbol(ctx), options)

def processFile3(fileName):
    processFile2(os.path.abspath(fileName), fileName)

def printError(error):
    print(error, file=sys.stderr)

def isHeaderFile(fileName):
    '''Returns true if the given file is identified as a C/C++ header file.'''
    return fileName.endswith(('.h', '.hpp'))

def isExcluded(filePath, exclusions):
    '''Returns true if the given file matches any of the exclusion patterns.'''
    return any(map(partial(fnmatch, filePath), exclusions))

def applyToHeaders(func, directory, exclusions):
    for root, dirs, files in os.walk(directory, onerror=printError):
        for fileName in files:
            filePath = os.path.join(root, fileName)
            if isHeaderFile(fileName) and not isExcluded(filePath, exclusions):
                func(filePath, fileName)

def main(arglist=None):
    parser = argparse.ArgumentParser(
            description='Find C or C++ header files with incorrect or missing '
            'include guards.')
    parser.add_argument('files',
            metavar='file',
            nargs='+',
            help='the file(s) to check; directories require the recursive '
            'option')
    parser.add_argument('-V','--version', action='version',
            version='%(prog)s ' + __version__)
    parser.add_argument('-v','--verbose',
            action='store_true',
            help='display more information about actions being taken')
    parser.add_argument('-r','--recursive',
            action='store_true',
            dest='recursive',
            help='recursively search directories for headers')
    parser.add_argument('-e','--exclude', 
            action='append',
            dest='exclusions',
            metavar='pattern',
            default=[],
            help='exclude files that match the given pattern')
    args = parser.parse_args(arglist)

    for f in args.files:
        if os.path.isdir(f):
            if args.recursive:
                applyToHeaders(processFile2, f, args.exclusions)
            else:
                printError('"%s" is a directory' % f)
                sys.exit(1)
        else:
            processFile3(os.abspath(f), f)

if __name__ == '__main__':
    main()
