# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.once2guard as o2g
import guardonce.guard2once as g2o

def test_o2g2o():
    _input = '''
#pragma once

int main() {
  return 0;
}
'''
    guard = 'MATCH_H'
    output = g2o.replace_guard(o2g.replace_pragma_once(_input, guard), guard)
    assert_multi_line_equal(_input, output)

def test_g2o2g():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif
'''
    guard = 'MATCH_H'
    output = o2g.replace_pragma_once(g2o.replace_guard(_input, guard), guard)
    assert_multi_line_equal(_input, output)
