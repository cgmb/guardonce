# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

"""Create functions that generate include guard tokens from patterns."""

class ParserError(Exception):
    pass

def compilePattern(pattern):
    """
    Takes a pattern specification as a string, and returns a function that
    turns a file context into an include guard.
    """
    pass
