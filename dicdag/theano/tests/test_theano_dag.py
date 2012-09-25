from dicdag.theano import *
from dicdag.theano.theano_dag import theano_graph_to_tuple_dag
from dicdag.util import unique
import theano

def info(var):
    return var.name, var.dtype, var.broadcastable, var.type
def namify_dict(d):
    return {k.name: v for k,v in d.items()}

def simple_example():
    x = theano.tensor.matrix('x')
    y = theano.tensor.matrix('y')
    z = x + y
    return (x, y), (z,)

def complex_example():
    x = theano.tensor.matrix('x')
    y = theano.tensor.matrix('y')
    z = theano.tensor.matrix('z')
    a = x + y * z
    b = theano.tensor.dot(a, z)
    c = a + a + b
    d = x[:2] + y + c

    return (x, y, z), (d, c)

def _test_theano_graph_dag_equivalence(i, o):
    variables = theano.gof.graph.variables(i, o)
    theano.gof.utils.give_variables_names(variables)
    dag, inputs, outputs = theano_graph_to_dag(i, o)
    assert set(map(info, variables)) == set(map(info, tuple(dag.keys())+inputs))

    dag = namify_dict(dag)
    assert all(type(dag[var.name]['fn']) == type(var.owner.op
                                                 if var.owner else None)
               for var in variables
               if var.name not in map(str, inputs))
    assert all(map(info, dag[var.name]['args']) == map(info,
                                                       var.owner.inputs
                                                       if var.owner else ())
               for var in variables
               if var.name not in map(str, inputs))

def _test_roundtrip(i, o):
    i2, o2 = dag_to_theano_graph(*theano_graph_to_dag(i, o))
    f = theano.FunctionGraph(i, o)
    f2 = theano.FunctionGraph(i2, o2)
    assert (theano.printing.debugprint(f,  file='str') ==
            theano.printing.debugprint(f2, file='str'))

def _test_all_have_names(i, o):
    dag, inputs, outputs = theano_graph_to_tuple_dag(i, o)
    assert unique(map(str, tuple(dag.keys())+inputs))


def _test_example(example):
    inputs, outputs = example()
    variables = theano.gof.graph.variables(inputs, outputs)
    theano.gof.utils.give_variables_names(variables)
    _test_all_have_names(inputs, outputs)
    _test_theano_graph_dag_equivalence(inputs, outputs)
    _test_roundtrip(inputs, outputs)

def test_simple():
    _test_example(simple_example)
def test_complex():
    _test_example(complex_example)
