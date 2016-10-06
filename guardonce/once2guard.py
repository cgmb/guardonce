# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Replace #pragma once with C and C++ include guards."""

from __future__ import print_function
import argparse
import sys
import os
import re
from fnmatch import fnmatch
from functools import partial
from .pattern_compiler import compilePattern, ParserError
from .util import indexPragmaOnce, getFileContents, writeFileContents

__version__ = "1.0.0"

def replacePragmaOnce(contents, guard):
    guardOpen = '#ifndef {0}\n#define {0}'.format(guard)
    guardClose = '#endif\n'
    try:
        start, end = indexPragmaOnce(contents)
        result = contents[:start] + guardOpen + contents[end:] + guardClose
        return result
    except ValueError:
        return None

def processFile(filePath, fileName, options):
    class Context:
        pass
    ctx = Context()
    ctx.filePath = filePath
    ctx.fileName = fileName

    options.guard = options.createGuard(ctx)

    try:
        contents = getFileContents(filePath)
        newContents = replacePragmaOnce(contents, options.guard)
        if newContents:
            writeFileContents(filePath, newContents)
    except Exception as e:
        print(e, file=sys.stderr)

def processGuardPattern(guardPattern):
    createGuard = lambda ctx: None
    if guardPattern is not None:
        try:
            createGuard = compilePattern(guardPattern)
        except ParserError as e:
            printError(e)
            sys.exit(1)
    return createGuard

def main():
    parser = argparse.ArgumentParser(
            description='Replace #pragma once with C and C++ include guards.')
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
    parser.add_argument('-p','--pattern',
            default='name|upper',
            metavar='pattern',
            help='generate include guards based on the specified pattern')
    parser.add_argument('-e','--exclude',
            action='append',
            dest='exclusions',
            metavar='pattern',
            default=[],
            help='exclude files that match the given pattern')
    args = parser.parse_args()

    class Options:
        pass
    options = Options()
    options.createGuard = processGuardPattern(args.pattern)

    for f in args.files:
        if os.path.isdir(f):
            if args.recursive:
                process = partial(processFile, options=options)
                applyToHeaders(process, f, args.exclusions)
            else:
                printError('"%s" is a directory' % f)
                sys.exit(1)
        else:
            processFile(f, os.path.basename(f), options)
