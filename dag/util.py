
## {{{ http://code.activestate.com/recipes/578231/ (r1)
def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__
## end of http://code.activestate.com/recipes/578231/ }}}

def merge(*args):
    return dict(sum([arg.items() for arg in args], []))

def unique(x):
    return len(set(x)) == len(x)
