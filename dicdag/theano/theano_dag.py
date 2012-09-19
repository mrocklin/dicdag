from theano import FunctionGraph
from theano.gof.utils import give_variables_names

def clone(x):
    return x.clone()
import dicdag
dicdag.clone = clone
from dicdag import *

# Composite functions
def fgraph_to_dag(fgraph):
    """ Converts a theano.FunctionGraph to a dict dag

    inputs:
        fgraph - a theano.FunctionGraph
    outputs:
        dag     - a dict of the form
                - {var1: {'fn': fn, 'args': arguments}, ... }
        inputs  - tuple of inputs to the computation
        outputs - tuple of outputs of the computation

    >>> import theano
    >>> from dag.theano import fgraph_to_dag
    >>> x = theano.tensor.matrix('x')
    >>> y = theano.tensor.dot(x, x); y.name = 'y'
    >>> fgraph = theano.FunctionGraph((x,), (y,))
    >>> dag, inputs, outputs = fgraph_to_dag(fgraph)
    >>> dag
    {y: {'args': (x, x), 'fn': <theano.tensor.basic.Dot at 0x3800350>}}
    >>> inputs, outputs
    ((x,), (y,))

    # reverse
    >>> fgraph2 = dag_to_fgraph(dag, inputs, outputs)
    """
    tdag, inputs, outputs = fgraph_to_tuple_dag(fgraph)
    dag = remove_singleton_indices(tuple_dag_to_index_dag(tdag))
    return dag, inputs, outputs

def dag_to_fgraph(dag, inputs, outputs):
    """ Converts a dicdag into a theano.FunctionGraph

    inputs:
        dag     - a dict of the form
                - {var1: {'fn': fn, 'args': arguments}, ... }
        inputs  - tuple of inputs to the computation
        outputs - tuple of outputs of the computation
    outputs:
        fgraph - a theano.FunctionGraph

    >>> import theano
    >>> from dag.theano import fgraph_to_dag
    >>> x = theano.tensor.matrix('x')
    >>> y = theano.tensor.dot(x, x); y.name = 'y'
    >>> fgraph = theano.FunctionGraph((x,), (y,))
    >>> dag, inputs, outputs = fgraph_to_dag(fgraph)
    >>> dag
    {y: {'args': (x, x), 'fn': <theano.tensor.basic.Dot at 0x3800350>}}
    >>> inputs, outputs
    ((x,), (y,))

    # reverse
    >>> fgraph2 = dag_to_fgraph(dag, inputs, outputs)
    """

    tdag = remove_index_entries(insert_single_indices(dag))
    return tuple_dag_to_fgraph(tdag, inputs, outputs)


def fgraph_to_tuple_dag(fgraph):
    """ Converts a theano.FunctionGraph into a tuple-dag

    This dag is of the form

        {(outputs): {'fn': fn, 'args': inputs}, ...}

    All keys are tuples

    This format is used when some functions create multiple outputs.
    It can be converted or simplified with functions in the root dag library.
    """
    fgraph = fgraph.clone()
    give_variables_names(fgraph.variables)

    newvars = {var: clone(var) for var in fgraph.variables}

    # Produces dag with inputs and outputs as tuples
    dag = {tuple(map(newvars.__getitem__, node.outputs)):
            {'fn'  : node.op,
             'args': tuple(map(newvars.__getitem__, node.inputs))}
             for node in fgraph.apply_nodes}

    inputs  = tuple(map(newvars.__getitem__, fgraph.inputs))
    outputs = tuple(map(newvars.__getitem__, fgraph.outputs))

    return dag, inputs, outputs

def ith_output(fn, inputs, idx, old_var):
    new_var = fn.make_node(*inputs).outputs[idx]
    new_var.name = old_var.name
    return new_var

def tuple_dag_to_fgraph(dag, inputs, outputs):
    """ Converts a tuple-dag into a theano.FunctionGraph

    This dag is of the form

        {(outputs): {'fn': fn, 'args': inputs}, ...}

    All keys are tuples

    This format is used when some functions create multiple outputs.
    It can be converted or simplified with functions in the root dag library.
    """

    return FunctionGraph(*tuple_dag_to_graph(dag, inputs, outputs, ith_output))
