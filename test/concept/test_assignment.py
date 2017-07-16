import unittest

from probability.concept.random_variable import RandomVariable, Assignment
from probability.concept.event import Event


class AssignmentTestCase(unittest.TestCase):

    def test_assigned(self):
        assignment = Assignment('A', Event({1, 2, 3}))

        self.assertTrue(assignment.assigned)

    def test___eq__(self):
        assignment = RandomVariable('A') == {1, 2, 3}
        assignment2 = RandomVariable('A') == {2, 3}
        assignment3 = RandomVariable('B') == {1, 2, 3}

        self.assertEqual(assignment, assignment)
        self.assertNotEqual(assignment, assignment2)
        self.assertNotEqual(assignment, assignment3)
