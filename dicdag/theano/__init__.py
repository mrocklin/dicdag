""" Conversion between theano.FunctionGraph and dicdag dicts

See Also:
    fgraph_to_dag(fgraph)
    dag_to_fgraph(dag, inputs, outputs)
"""

from theano_dag import fgraph_to_dag, dag_to_fgraph, ith_output
import theano_dag
