# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

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
