from probability.concept.assignment import Assignment
from probability.concept.conditional import ConditionalRandomVariable
from probability.concept.random_variable import RandomVariable, RandomVariables


class ElementsList(object):
    """
    List of elements. This class is used for simplify parse ProbabilityDistribution
    """

    def __init__(self, *args):
        """
        :param tuple args: RandomVariable, Assignment, ConditionalRandomVariable
                           or variable values: object or set
        """
        self.elements = args

    def contains_conditional_distribution(self):
        return any(type(element) == ConditionalRandomVariable for element in self.elements)

    def contains_assignment(self):
        return any(type(element) == Assignment for element in self.elements)

    def is_only_values(self):
        return all(self._element_is_value(element) for element in self.elements)

    def _element_is_value(self, element):
        types = (RandomVariable, Assignment, ConditionalRandomVariable)
        return not any(isinstance(element, t) for t in types)

    def __len__(self):
        return self.elements.__len__()

    def is_conditional_random_variable(self):
        return len(self) == 1 and isinstance(self[0], ConditionalRandomVariable)

    def to_conditional_random_variable(self):
        index_conditional = list(isinstance(e, ConditionalRandomVariable) for e in self.elements).index(True)

        conditional = self[index_conditional]

        query = self[:index_conditional] + conditional.query_variables.subset
        evidences = conditional.evidences.subset + self[index_conditional+1:]

        return ConditionalRandomVariable(RandomVariables(query), RandomVariables(evidences))

    def _conditional_index(self):
        pass

    def __getitem__(self, item):
        return self.elements.__getitem__(item)
