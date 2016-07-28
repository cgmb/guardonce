# Copyright (C) 2016 Cordell Bloor
# Published under the MIT License

from nose.tools import *
import guardonce.checkguard as go

def test_ok():
    contents = '''
#endif
'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 7)

def test_ok_space_before_hash():
    contents = '''
 #endif
'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 8)

def test_ok_space_after_hash():
    contents = '''
# endif
'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 8)

def test_ok_space_endif():
    contents = '''
#endif 
'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 8)

def test_no_newline_at_eof():
    contents = '''
#endif'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 7)

@raises(ValueError)
def test_no_endif():
    contents = '''
#endf
'''
    go.indexGuardEnd(contents)

def test_comment():
    contents = '''
#endif /* MATCH_H */
'''
    s,e = go.indexGuardEnd(contents)
    assert_equals(s, 1)
    assert_equals(e, 21)
