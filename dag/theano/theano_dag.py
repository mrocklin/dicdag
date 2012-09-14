from theano import FunctionGraph
from theano.gof.utils import give_variables_names

def clone(x):
    return x.clone()
import dag
dag.clone = clone
from dag import *



def fgraph_to_tuple_dag(fgraph):
    fgraph = fgraph.clone()
    give_variables_names(fgraph.variables)

    newvars = {var: clone(var) for var in fgraph.variables}

    # Produces dag with inputs and outputs as tuples
    dag = {tuple(map(newvars.__getitem__, node.outputs)):
            {'fn'  : node.op,
             'args': tuple(map(newvars.__getitem__, node.inputs))}
             for node in fgraph.nodes}

    inputs  = tuple(map(newvars.__getitem__, fgraph.inputs))
    outputs = tuple(map(newvars.__getitem__, fgraph.outputs))

    return dag, inputs, outputs

def tuple_dag_to_fgraph(dag, inputs, outputs):
    def ith_output(fn, inputs, idx, old_var):
        new_var = fn.make_node(*inputs).outputs[idx]
        new_var.name = old_var.name
        return new_var

    return FunctionGraph(*tuple_dag_to_graph(dag, inputs, outputs, ith_output))

# Composite functions
def fgraph_to_dag(fgraph):
    tdag, inputs, outputs = fgraph_to_tuple_dag(fgraph)
    dag = remove_singleton_indices(tuple_dag_to_index_dag(tdag))
    return dag, inputs, outputs

def dag_to_fgraph(dag, inputs, outputs):
    tdag = remove_index_entries(insert_single_indices(dag))
    return tuple_dag_to_fgraph(tdag, inputs, outputs)
