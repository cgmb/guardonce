# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Cordell Bloor
# Published under the MIT License

"""Find C or C++ header files with incorrect or missing include guards."""

from __future__ import print_function
import argparse
import sys
import os
from functools import partial
from .pattern_compiler import compile_pattern, ParserError
from .util import (guess_guard, index_guard_start, index_guard_end,
    index_pragma_once, get_file_contents, apply_to_headers)

__version__ = "2.3.0"

def is_reserved_token(token):
    return token[0] == '_' or token.find('__') != -1

def is_protected_by_guard(contents, guard_symbol):
    try:
        if guard_symbol:
            index_guard_start(contents, guard_symbol)
        else:
            guess_guard(contents)

        index_guard_end(contents)
        return True
    except ValueError:
        return False

def is_protected_by_once(contents):
    try:
        index_pragma_once(contents)
        return True
    except ValueError:
        return False

def is_protected(contents, options):
    return (options.accept_guard and is_protected_by_guard(contents, options.guard)
        or options.accept_once and is_protected_by_once(contents))

def is_file_protected(filename, options):
    contents, metadata = get_file_contents(filename)
    return is_protected(contents, options)

def process_file(filepath, filename, options):
    class Context:
        pass
    ctx = Context()
    ctx.filepath = filepath
    ctx.filename = filename

    options.guard = options.create_guard(ctx)

    if options.print_guard:
        print(options.guard)
        return

    try:
        if not is_file_protected(filepath, options):
            print(filepath)
    except Exception as e:
        print('Error processing {0}:\n\t({1}) {2}'.format(filepath,
            e.__class__.__name__, str(e)), file=sys.stderr)

def process_pattern(guard_pattern):
    create_guard = lambda ctx: None
    if guard_pattern is not None:
        try:
            create_guard = compile_pattern(guard_pattern)
        except ParserError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    return create_guard

def main():
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
    parser.add_argument('-r','--recursive',
            action='store_true',
            dest='recursive',
            help='recursively search directories for headers')
    parser.add_argument('-p','--pattern',
            default=None,
            metavar='pattern',
            help='check that include guards match the specified pattern. For '
            "example, -p 'name | upper' would create an expectation that "
            'Match.h has the include guard MATCH_H. See the docs on GitHub '
            'for a full description of the guard pattern language.')
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
    parser.add_argument('-o','--only',
            dest='type',
            metavar='type',
            default='any',
            choices=['guard','once','g','o'],
            help='only accept the specified type of include protection. '
            "Use 'guard' or 'g' to only accept include guards, or "
            "use 'once' or 'o' to only accept #pragma once.")
    parser.add_argument('-n','--print-guard',
            action='store_true',
            dest='print_guard',
            help='skip the check and instead print the include guards generated '
            'by --pattern.')
    args = parser.parse_args()

    if args.print_guard and args.pattern is None:
        print('Cannot print expected guard without guard pattern. Specify --pattern.', file=sys.stderr)
        sys.exit(1)

    class Options:
        pass
    options = Options()
    options.accept_guard = args.type in ['g', 'guard', 'any']
    options.accept_once = args.type in ['o', 'once', 'any']
    options.create_guard = process_pattern(args.pattern)
    options.print_guard = args.print_guard

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
