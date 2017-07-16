import unittest

from probability.concept.random_variable import RandomVariable, SetOfRandomVariable, Assignment, Conditional
from probability.concept.event import Event


class RandomVariableTestCase(unittest.TestCase):

    def test_name(self):
        name = 'A'
        self.assertEqual(RandomVariable(name).name, name)

    def test_assigned(self):
        self.assertFalse(RandomVariable('A').assigned)

    def test_assign(self):
        event = Event({1, 2, 3})
        expected = Assignment('A', event)

        self.assertEqual(RandomVariable('A').assign(event), expected)

    def test___eq__(self):
        self.assertEqual(RandomVariable('A'), RandomVariable('A'))
        self.assertNotEqual(RandomVariable('A'), RandomVariable('B'))

    def test___eq__ellipsis(self):
        self.assertFalse(RandomVariable('A') == ...)

    def test___eq__assign(self):
        event = Event({1, 2, 3})
        expected = Assignment('A', event)

        self.assertEqual(RandomVariable('A') == event, expected)

    def test___repr__(self):
        name = 'A'
        self.assertEqual(RandomVariable(name).__repr__(), name)

    def test_given(self):
        X, Y = RandomVariable('X'), RandomVariable('Y')
        X_barrado = SetOfRandomVariable((X, ))
        Y_barrado = SetOfRandomVariable((Y, ))

        expected = Conditional(X_barrado, Y_barrado)
        self.assertEqual(expected, X.given(Y))

    def test___or___given(self):
        X, Y = RandomVariable('X'), RandomVariable('Y')
        X_barrado = SetOfRandomVariable((X, ))
        Y_barrado = SetOfRandomVariable((Y, ))

        expected = Conditional(X_barrado, Y_barrado)
        self.assertEqual(expected, X | Y)
