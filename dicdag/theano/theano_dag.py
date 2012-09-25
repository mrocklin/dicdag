import theano
from theano.gof.utils import give_variables_names


def clone(x):
    return x.clone()
import dicdag
dicdag.clone = clone
from dicdag import *

# Composite functions
def theano_graph_to_dag(i, o):
    """ Converts a theano.FunctionGraph to a dict dag

    inputs:
        i, o    - a theano graph described by input and output variables
    outputs:
        dag     - a dict of the form
                - {var1: {'fn': fn, 'args': arguments}, ... }
        inputs  - tuple of inputs to the computation
        outputs - tuple of outputs of the computation

    >>> import theano
    >>> from dag.theano import theano_graph_to_dag
    >>> x = theano.tensor.matrix('x')
    >>> y = theano.tensor.dot(x, x); y.name = 'y'
    >>> dag, inputs, outputs = theano_graph_to_dag((x,), (y,))
    >>> dag
    {y: {'args': (x, x), 'fn': <theano.tensor.basic.Dot at 0x3800350>}}
    >>> inputs, outputs
    ((x,), (y,))

    # reverse
    >>> i, o = dag_to_theano_graph(dag, inputs, outputs)
    """
    tdag, inputs, outputs = theano_graph_to_tuple_dag(i, o)
    dag = remove_singleton_indices(tuple_dag_to_index_dag(tdag))
    return dag, inputs, outputs

def dag_to_theano_graph(dag, inputs, outputs):
    """ Converts a dicdag into a theano.FunctionGraph

    inputs:
        dag     - a dict of the form
                - {var1: {'fn': fn, 'args': arguments}, ... }
        inputs  - tuple of inputs to the computation
        outputs - tuple of outputs of the computation
    outputs:
        inputs  - tuple of theano variables
        outputs - tuple of theano variables

    >>> import theano
    >>> from dag.theano import theano_graph_to_dag
    >>> x = theano.tensor.matrix('x')
    >>> y = theano.tensor.dot(x, x); y.name = 'y'
    >>> dag, inputs, outputs = theano_graph_to_dag((x,), (y,))
    >>> dag
    {y: {'args': (x, x), 'fn': <theano.tensor.basic.Dot at 0x3800350>}}
    >>> inputs, outputs
    ((x,), (y,))

    # reverse
    >>> i, o = dag_to_theano_graph(dag, inputs, outputs)
    """

    tdag = dag_to_tdag(dag)
    return tuple_dag_to_theano_graph(tdag, inputs, outputs)


def theano_graph_to_tuple_dag(i, o):
    """ Converts a theano.FunctionGraph into a tuple-dag

    This dag is of the form

        {(outputs): {'fn': fn, 'args': inputs}, ...}

    All keys are tuples

    This format is used when some functions create multiple outputs.
    It can be converted or simplified with functions in the root dag library.
    """
    i, o = theano.gof.graph.clone(i, o)
    variables = theano.gof.graph.variables(i, o)
    apply_nodes = theano.gof.graph.list_of_nodes(i, o)
    give_variables_names(variables)

    newvars = {var: clone(var) for var in variables}

    # Produces dag with inputs and outputs as tuples
    dag = {tuple(map(newvars.__getitem__, node.outputs)):
            {'fn'  : node.op,
             'args': tuple(map(newvars.__getitem__, node.inputs))}
             for node in apply_nodes}

    inputs  = tuple(map(newvars.__getitem__, i))
    outputs = tuple(map(newvars.__getitem__, o))

    return dag, inputs, outputs

def ith_output(fn, inputs, idx, old_var):
    new_var = fn.make_node(*inputs).outputs[idx]
    new_var.name = old_var.name
    return new_var

def tuple_dag_to_theano_graph(dag, inputs, outputs):
    """ Converts a tuple-dag into a theano graph

    This dag is of the form

        {(outputs): {'fn': fn, 'args': inputs}, ...}

    All keys are tuples

    This format is used when some functions create multiple outputs.
    It can be converted or simplified with functions in the root dag library.
    """

    return tuple_dag_to_graph(dag, inputs, outputs, ith_output)
