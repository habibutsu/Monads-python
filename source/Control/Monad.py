class Functor(object):

    @classmethod
    def fmap(cls, f, fa):
        """fmap :: (a -> b) -> f a -> f b"""
        return fa.fmap(f)

fmap = Functor.fmap


class Applicative(Functor):

    def apply(self):
        """(<*>) :: f (a -> b) -> f a -> f b  """
        raise NotImplementedError

    def pure(self):
        """pure :: a -> f a"""
        raise NotImplementedError


class Monad(Functor):

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self._value)

    @classmethod
    def mreturn(cls, val):
        """mreturn :: a -> m a"""
        return cls(val)

    def bind(self, func):
        """(>>=) :: m a -> (a -> m b) -> m b"""
        raise NotImplementedError

    @classmethod
    def then(cls, mb):
        """(>>) :: m a -> m b -> m b"""
        raise NotImplementedError


class List(Monad, list):

    def __init__(self, *args):
        return list.__init__(self, args)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            list.__repr__(self))

    def map(self, func):
        return List(*map(func, self))

    def concat(self):
        return List(*reduce(lambda x, y: x + y, self, List()))

    fmap = map

    def bind(self, func):
        """xs >>= f = concat (map f xs)"""
        return self.map(func).concat()

    def apply(self, val):
        return List(*[val.map(fn) for fn in self]).concat()

    def then(self, mobj):
        return List(*[mobj for t in self]).concat()


class Maybe(Monad):

    def __eq__(self, other):
        return (type(self) == type(other)) and (self._value == other._value)

    def then(self, mobj):
        return mobj

class Just(Maybe):

    def fmap(self, func):
        return Just(func(self._value))

    def bind(self, func):
        return func(self._value)

    def apply(self, mobj):
        return self.mreturn(self._value(mobj._value))


class Nothing(Maybe):

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def __init__(self):
        super(Nothing, self).__init__(None)

    def fmap(self, func):
        return self

    def bind(self, func):
        return self
