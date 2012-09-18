from dicdag.util import *

def test_merge():
    d = {1:2, 3:4}
    e = {4:5}
    assert merge(d, e) == {1:2, 3:4, 4:5}

def test_merge_many():
    d = {1:2, 3:4}
    e = {4:5}
    f = {6:7}
    assert merge(d, e, f) == {1:2, 3:4, 4:5, 6:7}

def test_reverse_dict():
    d = {'a': (1, 2), 'b': (2, 3), 'c':()}
    assert reverse_dict(d) ==  {1: ('a',), 2: ('a', 'b'), 3: ('b',)}

