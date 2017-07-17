from typing import Union, Any


class Event(object):

    @staticmethod
    def by(data: Union['Event', set, Any]) -> 'Event':
        if type(data) == Event:
            return data
        elif type(data) == set:
            return Event(data)
        else:
            return Event({data})

    def __init__(self, elements: set):
        """
        :param set elements:
        """
        self._elements = elements

    @property
    def elements(self):
        return self._elements

    @property
    def is_singleton(self) -> bool:
        """
        This set is a singleton?

        Singleton also called "Unit set"
        """
        return len(self.elements) == 1

    def __repr__(self):
        element = self.elements if not self.is_singleton else next(self.elements.__iter__())
        return element.__repr__()

    def __len__(self):
        return self.elements.__len__()

    def __eq__(self, other):
        return self.elements == other.elements

    def __hash__(self):
        return str(self.elements).__hash__()