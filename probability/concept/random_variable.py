from functools import reduce

from typing import Tuple, Union, Iterable
from probability.concept.event import Event


class AssignmentError(Exception):
    pass


class RandomVariable(object):
    """
    **Random variable**, **Random vector** or **Factor**
    """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def assigned(self) -> bool:
        return False

    def assign(self, event: Event) -> 'Assignment':
        return Assignment(self.name, event)

    def __eq__(self, other) -> Union['Assignment', bool]:
        if isinstance(other, RandomVariable):
            return self.name == other.name
        if isinstance(other, type(Ellipsis)):
            return False

        return self.assign(Event.by(other))

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return self.name

    def __or__(self, other: 'RandomVariable') -> 'Conditional':
        return self.given(other)

    def given(self, *evidences: 'RandomVariable') -> 'Conditional':
        query = SetOfRandomVariable((self, ))
        return Conditional(query, SetOfRandomVariable(evidences))


class Assignment(RandomVariable):
    """
    Denotes an assignment of values to a random variable
    """

    def __init__(self, name: str, event: Event):
        super().__init__(name)
        self._event = event

    @property
    def assignment(self) -> Event:
        return self._event

    @property
    def assigned(self) -> bool:
        return True

    def __eq__(self, other: 'Assignment') -> bool:
        if isinstance(other, Assignment):
            return self.name == other.name \
               and self.assignment == other.assignment
        if isinstance(other, RandomVariable):
            return self.name == other.name

        return False

    def __repr__(self):
        representation = '{} = {}' if self.assignment.is_singleton else '{} ∈ {}'
        return representation.format(self.name, self.assignment)

    def __hash__(self):
        return hash(self.name.__hash__() + self.assignment.__hash__())


class SetOfRandomVariable(object):
    """
    :class:`SetOfRandomVariables` is a Set of random variables (assigned or not)
    """

    def from_iterable(self, names: Iterable) -> 'SetOfRandomVariable':
        return SetOfRandomVariable(tuple(RandomVariable(name) for name in names))

    def __init__(self, random_variables: Tuple[RandomVariable, ...]):
        self._random_variables = random_variables
        self._dict = dict(map(lambda variable: (variable.name, variable), self._random_variables))

    @property
    def names(self):
        return list(variable.name for variable in self._random_variables)

    def to_tuple(self):
        return tuple(self._random_variables)

    def to_set(self) -> set:
        return set(self._random_variables)

    def only_random_variables(self) -> Tuple[RandomVariable, ...]:
        """
        Returns only the random variable. If contains a assignment,
        is returned your random variable.
        """
        return tuple(RandomVariable(variable.name) for variable in self._random_variables)

    def __repr__(self):
        variables = tuple(reversed(self.to_tuple()))
        return reduce(lambda X, Y: '{}, {}'.format(Y, X), variables[1:], '') + variables[0].__repr__()

    def __iter__(self):
        return self.to_tuple().__iter__()

    def __getitem__(self, *args):
        return self.to_tuple().__getitem__(*args)

    def __getattr__(self, item):
        try:
            return self._dict[item]
        except:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))

    def __eq__(self, other: 'SetOfRandomVariable'):
        return self.to_set() == other.to_set()


class Conditional(object):

    def __init__(self, query_variables: SetOfRandomVariable, evidences: SetOfRandomVariable):
        """
        query_variables given evidences
        """
        self.query_variables = query_variables
        self.evidences = evidences

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.evidences == other.evidences \
           and self.query_variables == other.query_variables

    def __repr__(self):
        query = self.query_variables
        evidences = self.evidences

        return '{} | {}'.format(query, evidences)
