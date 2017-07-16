import unittest

from probability.concept.random_variable import RandomVariable, SetOfRandomVariable
from probability.other.utils import Parser


class ParserTestCase(unittest.TestCase):

    def test_lazy_notation(self):
        X, Y, Z, W = RandomVariable('X'), RandomVariable('Y'), RandomVariable('Z'), RandomVariable('W')
        variables = SetOfRandomVariable((X, Y, Z, W))
        expected = SetOfRandomVariable((X, Y, Z, W))

        none = (..., )
        result = Parser.lazy_notation(variables, subset=none)
        self.assertEqual(expected, result)

        head = (X, ...)
        result = Parser.lazy_notation(variables, subset=head)
        self.assertEqual(expected, result)
        self.assertEqual(result[0], X)

        tail = (..., X)
        result = Parser.lazy_notation(variables, subset=tail)
        self.assertEqual(expected, result)
        self.assertEqual(result[-1], X)

        head_tail = (W, ..., X)
        result = Parser.lazy_notation(variables, subset=head_tail)
        self.assertEqual(expected, result)
        self.assertEqual(result[0], W)
        self.assertEqual(result[-1], X)

    def test_lazy_notation_not_ellipsis(self):
        X, Y, Z, W = RandomVariable('X'), RandomVariable('Y'), RandomVariable('Z'), RandomVariable('W')

        variables = SetOfRandomVariable((X, Y, Z, W))
        subset = (RandomVariable(X),)

        expected = SetOfRandomVariable((X, ))

        result = Parser.lazy_notation(variables, subset=subset)
        self.assertEqual(expected, result)
