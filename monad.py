from forbiddenfruit import curse as bless

def _list_fmap(self, f):
    return [f(_) for _ in self]



bless(list, '_fmap', _list_fmap)

del _list_fmap

class Functor(object):
    def _fmap(self, f):
        assert False, 'Instances of Functor must implement fmap.'

class Applicative(Functor):
    @staticmethod
    def _pure(a):
        assert False, 'Instances of Applicative must implement pure.'

    def _ap(self, fa):
        assert False, 'Instances of Applicative must implement ap.'

class Monad(Applicative):
    def _bind(self, f):
        assert False, 'Instances of Monad must implement bind.'

class _Pure(object):
    def __init__(self, a):
        self._a = a

    def __repr__(self):
        return 'Pure {}'.format(self._a)

    def _ap(self, fa):
        return fa._pure(self._a)._ap(fa)

def fmap(g):
    return (
        lambda fa: fa._fmap(g)
    )

def ap(fg):
    return fg._ap

def pure(a):
    return Pure(a)

def bind(f):
    return (
        lambda m: m._bind(f)
    )

class Maybe(Monad):
    def __init__(self, a):
        self._a = a

    def __repr__(self):
        if self._a != None: return 'Just {}'.format(self._a)
        else:               return 'Nothing'

    def _fmap(self, f):
        if self._a != None: return Maybe(f(self._a))
        else:               return self

    @staticmethod
    def _pure(a): return Maybe(a)

    def _ap(self, fa):
        if self._a != None:
            if isinstance(fa, _Pure):
                fa = self._pure(fa._a)
            assert isinstance(fa, Maybe)
            return fa._fmap(self._a)
        else:
            return self

    def _bind(self, f):
        if self._a != None:
            res = f(self._a)
            assert isinstance(res, Maybe)
            return res
        else:
            return self

Just = Maybe
Nothing = Maybe(None)
