# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""A C or C++ parser that's just smart enough to handle most things the
 C preprocessor has to deal with, while finding while finding pragma once or
 include directives."""

class ParseState:
    Normal, LineComment, MultiLineComment = range(3)

class DirectiveState:
    Empty, Hash, Pragma, Done = range(4)

# this is a moment when I wish I'd taken compilers
# we can make do with a solid test suite and a little elbow grease
def indexPragmaOnce(src):
    state = ParseState.Normal
    directive = DirectiveState.Empty
    found = False
    i = 0
    token_start = -1
    directive_start = -1
    directive_end = -1
    prev_newline_commented = False
    num_comments_on_line = 0
    first_normal_index_on_line = -1
    last_normal_index_on_line = -1
    while i <= len(src): # run off the end to process end-of-token
        c = '\0'
        if i < len(src):
            c = src[i]
        nc = '\0'
        if i+1 < len(src):
            nc = src[i+1]

        if state == ParseState.Normal:
            # if we just finished consuming a token,
            # process that first
            is_name_char = c.isalnum() or c == '_'
            is_token_complete = token_start >= 0 and not is_name_char
            if is_token_complete:
                token = src[token_start:i]
                token_start = -1
                if directive == DirectiveState.Empty:
                    raise ValueError('token before directive')
                elif directive == DirectiveState.Hash:
                    if token == 'pragma':
                        directive = DirectiveState.Pragma
                    else:
                        raise ValueError('non-pragma directive')
                elif directive == DirectiveState.Pragma:
                    if token == 'once':
                        directive = DirectiveState.Done
                        if prev_newline_commented:
                            directive_start = first_normal_index_on_line
                        else:
                            directive_start = src.rfind('\n', 0, directive_start) + 1

                        directive_end = src.find('\n', i)
                        if directive_end == -1:
                            directive_end = len(src)

                        found = True
                    else:
                        raise ValueError('non-pragma once directive')

            # now, deal with whatever new thing we've come across
            if c == '/':
                if nc == '/':
                    last_normal_index_on_line = i - 1
                    state = ParseState.LineComment
                    i += 1
                elif nc == '*':
                    last_normal_index_on_line = i - 1
                    state = ParseState.MultiLineComment
                    i += 1
                else:
                    raise ValueError('/ not used for a comment')
            elif c == '#':
                if directive == DirectiveState.Empty:
                    directive = DirectiveState.Hash
                    directive_start = i
                else:
                    raise ValueError('# in directive')
            elif is_name_char:
                if directive not in [
                        DirectiveState.Empty,
                        DirectiveState.Done ]:
                    if token_start <= 0:
                        token_start = i
                else:
                    raise ValueError('token outside of directive')
            elif c == '\n':
                if directive not in [
                        DirectiveState.Empty,
                        DirectiveState.Done ]:
                    raise ValueError('unfinished directive')
                elif found:
                    break
                prev_newline_commented = False
                num_comments_on_line = 0
                first_normal_index_on_line = -1
                last_normal_index_on_line = -1
            elif c.isspace() or c == '\0':
                pass
            else:
                raise ValueError('unrecognized value')
        elif state == ParseState.LineComment:
            if c == '\n':
                state = ParseState.Normal
                prev_newline_commented = False
                num_comments_on_line = 0
                first_normal_index_on_line = -1
                last_normal_index_on_line = -1
        elif state == ParseState.MultiLineComment:
            if c == '*':
                if nc == '/':
                    state = ParseState.Normal
                    i += 1
                    num_comments_on_line += 1
                    if num_comments_on_line == 1:
                        first_normal_index_on_line = i + 1
            elif c == '\n':
                prev_newline_commented = True
                if found:
                    directive_end = last_normal_index_on_line
                    break
        i += 1
    if directive_start < 0 or directive_end < 0:
        raise ValueError('pragma once not found')
    return directive_start, directive_end
