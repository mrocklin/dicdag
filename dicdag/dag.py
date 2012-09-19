from util import merge, memodict

def clone(x):
    return x

index = '_index'

def tuple_dag_to_index_dag(tdag):
    """ Convert a tuple-dag into an index dag

    Inserts index operations for all outputs. As a result each pseudo-job has
    only one output, either a tuple or a single variable. It is now easy to
    back-traverse the graph

    Reverses:
        remove_index_entries
    """


    gets = {out:
            {'fn' : index,
             'args' : (outs, i)}
            for outs in tdag if isinstance(outs, tuple)
            for i, out in enumerate(outs)}

    return merge(tdag, gets)

def remove_singleton_indices(dag):
    """ Remove unnecessary index operations from a dag

    merges two operations that look like this
    {(out,) : {'fn': op,  'args': args}
     out    : {'fn': index, 'args': ((out,) 0)}}
    into just one that looks like this
    {out    : {'fn': op,  'args': args}}
    i.e. it unpacks singleton tuples

    Reverses:
        insert_single_indices
    """

    # dict of shortcuts
    quick_outs = {out: dag[(out,)] for out in dag if (out,) in dag}

    def badkey(out):
        return (out in quick_outs
             or (    isinstance(out, tuple)
                 and len(out) == 1
                 and out[0] in quick_outs))

    clean_dag =  {out : dag[out] for out in dag
                                 if not badkey(out)}

    return merge(clean_dag, quick_outs)

def insert_single_indices(dag):
    """ Add in all index operations from tuples, even singletons

    Reverses:
        remove_singleton_indices
    """

    return merge(*[
            {out: dag[out]}
            if isinstance(out, tuple) or dag[out]['fn'] == index else
            {(out,) : dag[out],
              out   : {'fn': index, 'args':((out,), 0)}}
            for out in dag])

def remove_index_entries(dag):
    """ Remove naked variables - only tuples as outputs """
    return {k:v for k,v in dag.items() if v['fn'] != index}


def tuple_dag_to_graph(dag, inputs, outputs, ith_output):
    """
    Convert a tuple-dag to a graph of some form

    inputs:
        dag - a tuple-dag
        inputs - a tuple of input variables
        outputs - a tuple of output varibles
        ith_output - a function to build a variable in a graph
                     :: (op, args, idx_of_output, old_var) -> new_output
    outputs:
        graph - a newly constructed graph

    ith_output in detail:
        You need to specify how to build your graph. Specifically you must
        supply a function which takes an operation and a set of inputs and
        returns the idx'th output of this computation.

        See theano.theano_dag.tuple_dag_to_fgraph.ith_output for an example

    See Also:
        theano.theano_dag.tuple_dag_to_fgraph
    """
    input_set = {}

    def is_input(var):
        return var in inputs
    subvar = {out:outs for outs in dag for out in outs}

    @memodict
    def _build_var(var):
        if is_input(var):
            newvar = clone(var)
            input_set[str(var)] = newvar
            return newvar
        # In which tuple do I live?
        outs = subvar[var]
        idx  = outs.index(var)
        fn   = dag[outs]['fn']
        args = dag[outs]['args']
        # Compute result of the associated function
        # Get the variables for the inputs recursively
        inputs = map(_build_var, args)
        return ith_output(fn, inputs, idx, var)


    graph_outputs = map(_build_var, outputs)
    graph_inputs  = map(input_set.__getitem__, map(str, inputs))

    return graph_inputs, graph_outputs

def dag_to_graph(dag, inputs, outputs, ith_output):
    tdag = remove_index_entries(insert_single_indices(dag))
    return tuple_dag_to_graph(tdag, inputs, outputs, ith_output)

