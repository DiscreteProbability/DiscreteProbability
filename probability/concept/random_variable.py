from abc import ABCMeta, abstractmethod
from functools import reduce

from probability.concept.assignment import Assignment
from probability.concept.conditional import ConditionalRandomVariable
from probability.concept.event import Event

from probability.other.container_variable import ContainerVariable


class AbstractRandomVariable(metaclass=ABCMeta):

    def given(self, *evidences):
        query = RandomVariables((self, ))
        return ConditionalRandomVariable(query, RandomVariables(evidences))

    @property
    @abstractmethod
    def as_set(self):
        """
        :return set:
        """
        return None


class RandomVariable(AbstractRandomVariable, ContainerVariable):
    """
    **Random variable**, **Random vector** or **Factor**
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def random_variable(self):
        return self

    def __eq__(self, other):
        if type(other) == RandomVariable:
            return self.name == other.name

        return Assignment(self, self._generate_event(other))

    def _generate_event(self, other):
        if type(other) == Event:
            event = other
        elif type(other) == set:
            event = Event(other)
        else:
            event = Event({other})

        return event

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return self.name

    @property
    def as_set(self):
        return {self}

    def union(self, other):
        return UnionRandomVariable(self, other)

    def __or__(self, other):
        other = RandomVariables((other, ))
        this = RandomVariables((self, ))

        return ConditionalRandomVariable(this, other)


class RandomVariables(AbstractRandomVariable):
    """
    `SetOfRandomVariables`

    Data structures that contain RandomVariables (possibly with assignments).
    """

    def __init__(self, subset):
        """
        :param tuple subset:
        """
        self.subset = subset

    @property
    def as_set(self):
        return set(self.subset)

    def __repr__(self):
        return reduce(lambda X, Y: '{}, {}'.format(Y, X), reversed(self.subset[:-1]), '') + self.subset[-1].__repr__()

    def __iter__(self):
        return self.subset.__iter__()

    @property
    def names(self):
        return list(element.name for element in self.subset)


class UnionRandomVariable(object):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

