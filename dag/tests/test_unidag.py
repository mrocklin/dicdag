from unidag import *

small_dag = {'b': {'fn': 1, 'args': ('a', )}}
small_back_unidag = {(('a', ), 1, 'b'): ()}
small_unidag = {(('a', ), 1, 'b'): ()}

medium_dag = {'b': {'fn': 1, 'args': ('a', )},
              'c': {'fn': 2, 'args': ('a', 'b')}}
medium_back_unidag = {(('a', 'b'), 2, 'c'): ((('a',), 1, 'b'),),
                     (('a', ),    1, 'b'): ()}
medium_unidag = {(('a', 'b'), 2, 'c'): (),
                 (('a', ),    1, 'b'): ((('a', 'b'), 2, 'c'),)}

def test_dag_to_backward_unidag_small():
    assert dag_to_backward_unidag(small_dag) == small_back_unidag

def test_dag_to_backward_unidag_medium():

    assert dag_to_backward_unidag(medium_dag) == medium_back_unidag

def test_dag_to_unidag_small():
    assert dag_to_unidag(small_dag) == small_unidag

def test_dag_to_unidag_medium():
    assert dag_to_unidag(medium_dag) == medium_unidag

def test_backward_unidag_to_dag_small():
    assert backward_unidag_to_dag(small_back_unidag) == small_dag

def test_backward_unidag_to_dag_medium():
    assert backward_unidag_to_dag(medium_back_unidag) == medium_dag

def test_unidag_to_dag_small():
    assert unidag_to_dag(small_unidag) == small_dag

def test_unidag_to_dag_medium():
    assert unidag_to_dag(medium_unidag) == medium_dag

