# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Replace C and C++ include guards with #pragma once."""

from __future__ import print_function
import argparse
import sys
import os
from functools import partial
from .pattern_compiler import compile_pattern, ParserError
from .util import (guess_guard, index_guard_start, index_guard_end,
    get_file_contents, write_file_contents, apply_to_headers)

__version__ = "2.1.0"

def replace_guard(contents, guard, strip=False):
    try:
        if guard:
            start1, end1 = index_guard_start(contents, guard)
        else:
            guard, start1, end1 = guess_guard(contents)
        start2, end2 = index_guard_end(contents)
        if end2 < len(contents) and contents[end2] == '\n':
            end2 += 1

        replaced = (contents[:start1] + '#pragma once' +
                contents[end1:start2] + contents[end2:])

        if strip:
            return replaced.rstrip() + '\n'
        else:
            return replaced
    except ValueError:
        return None

def process_file(filepath, filename, options):
    class Context:
        pass
    ctx = Context()
    ctx.filepath = filepath
    ctx.filename = filename

    options.guard = options.create_guard(ctx)

    try:
        contents = get_file_contents(filepath)
        new_contents = replace_guard(contents, options.guard,
                strip=options.strip)
        if new_contents:
            write_file_contents(filepath, new_contents)
    except Exception as e:
        print(e, file=sys.stderr)

def process_guard_pattern(pattern):
    create_guard = lambda ctx: None
    if pattern is not None:
        try:
            create_guard = compile_pattern(pattern)
        except ParserError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    return create_guard

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
    parser.add_argument('-r','--recursive',
            action='store_true',
            dest='recursive',
            help='recursively search directories for headers')
    parser.add_argument('-p','--pattern',
            default=None,
            metavar='pattern',
            help='replace only include guards that match the specified '
            "pattern. For example, -p 'name | upper' would only change the "
            'guard in Match.h if it had the symbol MATCH_H. See the docs on '
            'GitHub for a full description of the guard pattern language.')
    parser.add_argument('-e','--exclude',
            action='append',
            dest='exclusions',
            metavar='pattern',
            default=[],
            help='exclude files that match the given fnmatch pattern. '
            'Any * is a wildcard matching everything; '
            'a ? matches any single character; '
            '[_] matches any characters within the brackets; '
            'and [!_] matches any characters not within the brackets.')
    parser.add_argument('-s','--strip',
            action='store_true',
            dest='strip',
            help='strip trailing whitespace after removing guard')
    args = parser.parse_args()

    class Options:
        pass
    options = Options()
    options.strip = args.strip
    options.create_guard = process_guard_pattern(args.pattern)

    for f in args.files:
        if os.path.isdir(f):
            if args.recursive:
                process = partial(process_file, options=options)
                apply_to_headers(process, f, args.exclusions)
            else:
                print('"%s" is a directory' % f, file=sys.stderr)
                sys.exit(1)
        else:
            process_file(f, os.path.basename(f), options)

if __name__ == "__main__":
    main()
