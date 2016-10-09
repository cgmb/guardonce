# -*- coding: utf-8 -*-
# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.guard2once as o2g

def test_basic():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif
'''
    expected = '''
#pragma once

int main() {
  return 0;
}

'''
    o = o2g.replace_guard(_input, 'MATCH_H')
    assert_multi_line_equal(o, expected)

def test_no_newline_at_eof():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif'''
    expected = '''
#pragma once

int main() {
  return 0;
}
'''
    o = o2g.replace_guard(_input, 'MATCH_H')
    assert_multi_line_equal(o, expected)

def test_unknown_guard():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif
'''
    expected = '''
#pragma once

int main() {
  return 0;
}

'''
    o = o2g.replace_guard(_input, None)
    assert_multi_line_equal(o, expected)

def test_with_comment():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif /* MATCH_H */
'''
    expected = '''
#pragma once

int main() {
  return 0;
}

'''
    o = o2g.replace_guard(_input, 'MATCH_H')
    assert_multi_line_equal(o, expected)

def test_with_comment_unknown_guard():
    _input = '''
#ifndef MATCH_H
#define MATCH_H

int main() {
  return 0;
}
#endif /* MATCH_H */
'''
    expected = '''
#pragma once

int main() {
  return 0;
}

'''
    o = o2g.replace_guard(_input, None)
    assert_multi_line_equal(o, expected)
