import unittest

from probability.other.utils import Utils
from probability.concept.event import Event


class UtilsTestCase(unittest.TestCase):

    def test_generate_event_by_set(self):
        event = Event({1, 2, 3})

        self.assertEqual(Utils.build_event({1, 2, 3}), event)

    def test_generate_event_by_event(self):
        event = Event({1, 2, 3})

        self.assertEqual(Utils.build_event(event), event)

    def test_generate_event_any(self):
        event = Event({1})
        event2 = Event({'test'})

        self.assertEqual(Utils.build_event(1), event)
        self.assertEqual(Utils.build_event('test'), event2)
