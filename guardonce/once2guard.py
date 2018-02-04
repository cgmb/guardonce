# -*- coding: utf-8 -*-
# Copyright (C) 2016-2018 Cordell Bloor
# Published under the MIT License

"""Replace #pragma once with C and C++ include guards."""

from __future__ import print_function
import argparse
import sys
import os
from functools import partial
from .pattern_compiler import compile_pattern, ParserError
from .util import (index_pragma_once, get_file_contents, write_file_contents,
    apply_to_headers, ends_with_blank_line, py2)

__version__ = "2.3.0"

class Template:
    """
    A purpose-built string formatter. It replaces % with the value passed to sub.
    % can be escaped as %%. It does nothing else, so there are no surprises.
    string.Template is a decent alternative, but its syntax is more complex
    than really necessary for these purposes.
    """
    def __init__(self, fmtstr):
        self.placeholder = object()
        self.pieces = gather_pieces(fmtstr, self.placeholder)

    def sub(self, guard):
        return ''.join([guard if x is self.placeholder else x for x in self.pieces])

def gather_pieces(fmtstr, placeholder):
    """
    Takes a format string where % marks replacements by placeholder, and %%
    marks replacements by %. The returned object is a list of substrings and
    placeholders.
    """
    pieces = []
    substr = []
    escape = False
    for c in fmtstr:
        if escape:
            if c == '%':
                substr.append(c)
            else:
                pieces.append(''.join(substr))
                substr = []
                pieces.append(placeholder)
                substr.append(c)
            escape = False
        else:
            if c == '%':
                escape = True
            else:
                substr.append(c)
    pieces.append(''.join(substr))
    if escape:
        pieces.append(placeholder)
    return pieces

def replace_pragma_once(contents, guard,
        endif_template=Template('#endif\n'), endif_newline=False):
    guard_open = '#ifndef {0}\n#define {0}'.format(guard)
    guard_close = endif_template.sub(guard)
    try:
        once_start, once_end = index_pragma_once(contents)
    except ValueError:
        return None

    # figure out how many newlines to put before the guard
    if ends_with_blank_line(contents):
        nl = ''
    elif contents.endswith('\n'):
        nl = '\n' if endif_newline else ''
    else:
        nl = '\n\n' if endif_newline else '\n'

    return (contents[:once_start]
        + guard_open
        + contents[once_end:]
        + nl + guard_close)

def process_file(filepath, filename, options):
    class Context:
        pass
    ctx = Context()
    ctx.filepath = filepath
    ctx.filename = filename

    options.guard = options.create_guard(ctx)

    try:
        contents, metadata = get_file_contents(filepath)
        new_contents = replace_pragma_once(contents, options.guard,
            options.endif_template, options.endif_newline)
        if options.stdout and new_contents is None:
            new_contents = contents
        if new_contents:
            output_path = None if options.stdout else filepath
            write_file_contents(output_path, new_contents, metadata)
    except Exception as e:
        print('Error processing {0}:\n\t({1}) {2}'.format(filepath,
            e.__class__.__name__, str(e)), file=sys.stderr)

def process_guard_pattern(pattern):
    create_guard = lambda ctx: None
    if pattern is not None:
        try:
            create_guard = compile_pattern(pattern)
        except ParserError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    return create_guard

def es(ustr):
    '''
    Encodes the given unicode string to str
    '''
    if py2:
        return ustr.encode('utf8')
    else:
        return ustr

def decode_escapes(s):
    import re
    import codecs
    def decode_match(match):
        return es(codecs.decode(match.group(0), 'unicode-escape'))
    # https://stackoverflow.com/a/24519338
    escapes = re.compile(r'''
        ( \\U........      # 8-digit hex escapes
        | \\u....          # 4-digit hex escapes
        | \\x..            # 2-digit hex escapes
        | \\[0-7]{1,3}     # Octal escapes
        | \\N\{[^}]+\}     # Unicode characters by name
        | \\[\\'"abfnrtv]  # Single-character escapes
        )''', re.UNICODE | re.VERBOSE)
    return escapes.sub(decode_match, s)

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
    parser.add_argument('-r','--recursive',
            action='store_true',
            dest='recursive',
            help='recursively search directories for headers')
    parser.add_argument('-s','--endif-style',
            dest='endif_template',
            metavar='template',
            default='#endif\n',
            help='use the given template for the inserted #endif. '
            'The include guard can be referenced in the template with %%. '
            'Any other uses of %% must be escaped as %%%%.')
    parser.add_argument('-l','--endif-newline',
            action='store_true',
            dest='endif_newline',
            help='insert a blank line before #endif if none would exist '
            'otherwise')
    parser.add_argument('-p','--pattern',
            default='name|upper',
            metavar='pattern',
            help='generate include guards that match the specified pattern. '
            "For example, -p 'name | upper' would create the guard MATCH_H "
            'for the file Match.h. See the docs on GitHub for a full '
            'description of the guard pattern language.')
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
    parser.add_argument('--stdout',
            action='store_true',
            dest='stdout',
            help='write output to stdout')
    args = parser.parse_args()

    class Options:
        pass
    options = Options()
    options.create_guard = process_guard_pattern(args.pattern)
    options.endif_template = Template(decode_escapes(args.endif_template))
    options.endif_newline = args.endif_newline
    options.stdout = args.stdout

    if options.stdout and args.recursive:
        print('The recursive option cannot be used when printing to stdout',
            file=sys.stderr)
        sys.exit(1)
    elif options.stdout and len(args.files) > 1:
        print('Only one file can be specified at a time when printing to stdout',
            file=sys.stderr)
        sys.exit(1)

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
