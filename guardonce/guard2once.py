# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Replace C and C++ include guards with #pragma once."""

from __future__ import print_function
import argparse
import sys
import os
import re
from fnmatch import fnmatch
from functools import partial
from .pattern_compiler import compilePattern, ParserError
from .util import guessGuard, indexGuardStart, indexGuardEnd, getFileContents, writeFileContents, applyToHeaders, printError

__version__ = "1.0.0"

def replaceGuard(contents, guard):
    try:
        if guard:
            start1, end1 = indexGuardStart(contents, guard)
        else:
            guard, start1, end1 = guessGuard(contents)
        start2, end2 = indexGuardEnd(contents)
        return (contents[:start1] + '#pragma once' +
                contents[end1:start2] + contents[end2:])
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
        newContents = replaceGuard(contents, options.guard)
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
            description='Replace C and C++ include guards with #pragma once.')
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
            default=None,
            metavar='pattern',
            help='search for include guards based on the specified pattern')
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
