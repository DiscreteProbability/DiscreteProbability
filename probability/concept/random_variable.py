from functools import reduce

from typing import Tuple, Union
from probability.other.utils import Utils
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

        return self.assign(Utils.build_event(other))

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
        if isinstance(other, RandomVariable):
            return self.name == other.name \
               and self.assignment == other.assignment

        return False


class SetOfRandomVariable(object):
    """
    :class:`SetOfRandomVariables` is a Set of random variables (assigned or not)
    """

    def __init__(self, random_variables: Tuple[RandomVariable]):
        self._set = random_variables
        self._dict = dict(map(lambda variable: (variable.name, variable), self._set))

    def __repr__(self):
        variables = tuple(reversed(self._set))
        return reduce(lambda X, Y: '{}, {}'.format(Y, X), variables[1:], '') + variables[0].__repr__()

    @property
    def set(self):
        return self._set

    def __eq__(self, other: 'SetOfRandomVariable'):
        return self.set == other.set


class Conditional(object):

    def __init__(self, query_variables: SetOfRandomVariable, evidences: SetOfRandomVariable):
        """
        query_variables given evidences
        """
        self.query_variables = query_variables
        self.evidences = evidences

    def __eq__(self, other):
        return self.evidences == other.evidences \
           and self.query_variables == other.query_variables

    def __repr__(self):
        query = self.query_variables
        evidences = self.evidences

        return '{} | {}'.format(query, evidences)
