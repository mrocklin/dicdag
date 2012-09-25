from dicdag.dag import *

tuple_dag = {('a',)    : {'fn': 1, 'args': ('b', 'c')},
             ('b', 'd'): {'fn': 2, 'args': ('e',)},
             ('f', )   : {'fn': 3, 'args': ('d', 'a')}}

index_dag = {('a',)    : {'fn': 1, 'args': ('b', 'c')},
             'a'       : {'fn': index, 'args': (('a',), 0)},
             'b'       : {'fn': index, 'args': (('b', 'd'), 0)},
             'd'       : {'fn': index, 'args': (('b', 'd'), 1)},
             ('b', 'd'): {'fn': 2, 'args': ('e',)},
             ('f',)    : {'fn': 3, 'args': ('d', 'a')},
             'f'       : {'fn': index, 'args': (('f',), 0)}}
redin_dag = {'a'       : {'fn': 1, 'args': ('b', 'c')},
             'b'       : {'fn': index, 'args': (('b', 'd'), 0)},
             'd'       : {'fn': index, 'args': (('b', 'd'), 1)},
             ('b', 'd'): {'fn': 2, 'args': ('e',)},
             'f'       : {'fn': 3, 'args': ('d', 'a')}}

def test_tuple_dag_to_index_dag():
    assert tuple_dag_to_index_dag(tuple_dag) == index_dag

def test_remove_singleton_indices():
    assert remove_singleton_indices(index_dag) == redin_dag

def test_insert_single_indices():
    assert insert_single_indices(redin_dag) == index_dag

def test_remove_index_entries():
    assert remove_index_entries(index_dag) == tuple_dag

def test_dag_to_tdag():
    assert dag_to_tdag(redin_dag) == tuple_dag

def test_all():
    assert (remove_index_entries(
                insert_single_indices(
                    remove_singleton_indices(
                        tuple_dag_to_index_dag(tuple_dag))))
            == tuple_dag)

def test_remove_singleton_indices2():
    indag = {'a':   {'fn': index, 'args':(('a',), 0)},
            ('a',): {'fn': 'stuff', 'args': (1,2,3)},
             'b':   {'fn': 'blah', 'args': ()}}

    assert remove_singleton_indices(indag) == {
        'a': {'fn': 'stuff', 'args': (1,2,3)},
        'b': {'fn': 'blah',  'args': ()}}

def test_inputs_of():
    assert  inputs_of(tuple_dag) == {'c', 'e'}
def test_outputs_of():
    assert outputs_of(tuple_dag) == {'f'}
