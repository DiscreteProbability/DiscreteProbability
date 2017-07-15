from probability.concept.event import Event
from typing import Union, Any


class Utils:

    @staticmethod
    def build_event(other: Union[Event, set, Any]) -> Event:
        if type(other) == Event:
            return other
        elif type(other) == set:
            return Event(other)
        else:
            return Event({other})

    @staticmethod
    def parse_lazy_notation(variables, subset, ignore=None):
        """
        Replace ellipsis (...) in subset for variables - subset - ignore

        :param variables:
        :param subset:
        :param ignore:

        :return:
        """
        ignore = [] if ignore is None else ignore

        index = subset.index(...)

        head = subset[:index]
        middle = tuple(set(variables) - set(subset) - set(ignore))
        tail = subset[index + 1:]

        return head + middle + tail
