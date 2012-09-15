DicDag
======

A few simple data structures to represent computations as Directed Acyclic Graphs. Also conversion functions between these formats.

Style
-----

Much of the code within this module is functional in nature. It does not adhere to standard Python best practices.

Formats
-------

Almost all formats are dictionaries. Dependence in the graph is managed by the key-value relationship in a dictionary.

Each format has to worry about the following challenges:

* How do you handle functions with multiple outputs?
* How fast is it to traverse the graph going forwards (towards outputs)?
* How fast is it to traverse the graph going backwards (towards inputs)?

###Dag###

Our standard format looks like the following
    
    {out-variable: {'fn': operation, 'args': (inputs)}, ...}

This is easy to traverse backwards (from outputs to inputs) but does not handle forward traversals or multiple outputs well. 

For complete representation this format also needs to include a tuple of inputs and outputs to the graph. Otherwise the order of these is uncertain.

###Tuple-Dag###

A slight variation manages multiple outputs well but is no longer able to easily traverse in either direction.

    {(outputs): {'fn': operation, 'args': (inputs)}, ...}

###Index-Dag###

We can handle both backward traversals and multiple outputs by inserting index operations into the graph. We supply functions that convert Tuple-Dags to Dags by adding index operations as follows:

    {(c, d): {'fn': op, 'args': (a, b)}
    ==>>
    { c    : {'fn': index, 'args': ((c, d), 0)},
      d    : {'fn': index, 'args': ((c, d), 1)},
     (c, d): {'fn': op, 'args': (a, b)}}

Where `a, b, c, d` are generic variables and `op` is a generic operation. `index` is a keyword. 

We provide functions to simplify this "blown out" representation in the common case where there is only one output

###UniDag###

A unipartite dag has only one kind of element, a job. It does not consider variables separately. They are effectively the edges of the graph. It has a very simple format

    {a: (b, c), b: (c,)}

In this case `a,b,c` are all jobs. The entry `a: (b, c)` implies that `a` immediately precedes `b` and `c`. 

This simplified format is used in some scheduling algorithms.

###Theano FunctionGraph###

Theano is a Python library for constructing and compiling numeric computations. It implements its own FunctionGraph type. We supply converters to this type.

###Conversions###

The main contribution of this repository is to convert between various formats. We supply the following bidirectional conversions

* tuple-dag <--> Theano
* tuple-dag <--> index-dag
* index-dag <--> dag
* dag <--> unidag

Because all links are bidirectional it is possible to convert between any pair of formats.
