
class Event(object):

    def __init__(self, elements):
        """
        :param set elements:
        """
        self.elements = elements

    def __repr__(self):
        element = self.elements if not self.is_singleton else next(self.elements.__iter__())
        return element.__repr__()

    def __len__(self):
        return self.elements.__len__()

    def __eq__(self, other):
        return self.elements == other.elements

    @property
    def is_singleton(self):
        """
        This set is a singleton (unit set)?
        :return:
        """
        return len(self.elements) == 1
