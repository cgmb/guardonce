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
    assert_multi_line_equal(expected, o)

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
    assert_multi_line_equal(expected, o)

def test_blank_line_before_endif_no_newline_at_eof():
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
    o = o2g.replace_pragma_once(_input, 'MATCH_H', endif_newline=True)
    assert_multi_line_equal(expected, o)

def test_blank_line_before_endif():
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
    o = o2g.replace_pragma_once(_input, 'MATCH_H', endif_newline=True)
    assert_multi_line_equal(expected, o)

def test_blank_line_before_endif_existing_whitespace():
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
    o = o2g.replace_pragma_once(_input, 'MATCH_H', endif_newline=True)
    assert_multi_line_equal(expected, o)
