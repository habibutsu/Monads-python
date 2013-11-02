import unittest
from Control.Monad import *


class ListTestCase(unittest.TestCase):

    def test_fmap(self):
        self.assertEqual(
            fmap(lambda x: x*2, List(2,3)),
            List(4,6))

    def test_bind(self):

        r = List(2, 3).bind(lambda x: List(x*2)).bind(lambda x: List(x+1))
        self.assertEqual(r, List(5, 7))

    def test_apply(self):
        #[(\x->x*2),(\x->x+3)] <*> [1,2,3]
        r = List(lambda x: x*2, lambda x: x+1).apply(List(2, 3))
        self.assertEqual(r, List(4, 6, 3, 4))

    def test_apply_then(self):
        self.assertEqual(
            List(2, 3).bind(lambda x: List(x*2)).then(List(5, 6)),
            List(5, 6, 5, 6))


class MaybeTestCase(unittest.TestCase):

    def test_nothing(self):
        self.assertEqual(
            Nothing(),
            Nothing())

    def test_fmap_just(self):
        # fmap (*2) (Just(2))
        self.assertEqual(
            fmap(lambda x: x*2, Just(2)),
            Just(4))

    def test_fmap_nothing(self):
        # fmap (*2) (Nothing)
        self.assertEqual(
            fmap(lambda x: x*2, Nothing()),
            Nothing())

    def test_bind_just(self):

        self.assertEqual(
            Just(2).bind(lambda x: Just(x*2)).bind(lambda x: Just(x+2)),
            Just(6))

        self.assertEqual(
            Just(2).bind(lambda x: Nothing()).bind(lambda x: Just(x+2)),
            Nothing())

    def test_apply_just(self):
        #
        self.assertEqual(
                Just(lambda x: x*2).apply(Just(2)),
                Just(4))

    def test_then_just(self):
        # Just(2) >>= \x -> Just(x*2) >> \x -> Just(10)
        self.assertEqual(
                Just(2).bind(lambda x: Just(x*2)).then(Just(10)),
                Just(10))

        # Just(\x -> x*2) <*> Just(2) >> Just(10)
        self.assertEqual(
                Just(lambda x: x*2).apply(Just(2)).then(Just(10)),
                Just(10))

    def test_bin_nothing(self):
        self.assertEqual(
            Nothing().bind(lambda x: Just(x*2)),
            Nothing())