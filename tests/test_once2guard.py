# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.once2guard as o2g

def test_basic():
    _input = '''
#pragma once

int main() {
  return 0;
}
'''
    expected = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif
'''
    o = o2g.replace_pragma_once(_input, 'MATCH_H')
    assert_multi_line_equal(o, expected)

def test_no_newline_at_eof():
    _input = '''
#pragma once

int main() {
  return 0;
}'''
    expected = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif
'''
    o = o2g.replace_pragma_once(_input, 'MATCH_H')
    assert_multi_line_equal(o, expected)
