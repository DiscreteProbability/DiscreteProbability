import unittest

from discrete_probability.concept.event import Event


class EventTestCase(unittest.TestCase):

    def test_by_set(self):
        event = Event({1, 2, 3})

        self.assertEqual(Event.by({1, 2, 3}), event)

    def test_by_event(self):
        event = Event({1, 2, 3})

        self.assertEqual(Event.by(event), event)

    def test_by_any(self):
        event = Event({1})
        event2 = Event({'test'})

        self.assertEqual(Event.by(1), event)
        self.assertEqual(Event.by('test'), event2)
