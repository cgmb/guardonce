# -*- coding: utf-8 -*-
# Copyright (C) 2017 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.checkguard as c

def test_unknown_pattern_requires_content_between_guard_start_and_end():
    _input = '''
#ifndef ONE
#define ONE 1
#endif

int main() {
  return 0;
}
'''
    assert_false(c.is_protected_by_guard(_input, None))

def test_known_pattern_does_not_require_content_between_guard_start_and_end():
    _input = '''
#ifndef ONE
#define ONE 1
#endif
'''
    assert_true(c.is_protected_by_guard(_input, 'ONE'))

def test_reserved_tokens():
    assert_true(c.is_reserved_token('_MY_HEADER_'))
    assert_true(c.is_reserved_token('MY__HEADER'))
    assert_false(c.is_reserved_token('MY_HEADER_'))
