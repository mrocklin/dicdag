""" Conversion between theano.FunctionGraph and dicdag dicts

See Also:
    theano_graph_to_dag(i, o)
    dag_to_theano_graph(dag, inputs, outputs)
"""

from theano_dag import theano_graph_to_dag, dag_to_theano_graph, ith_output
import theano_dag
