from typing import Union, Tuple
from probability.concept.random_variable import RandomVariable, SetOfRandomVariable


class Parser:

    @staticmethod
    def lazy_notation(
            variables: SetOfRandomVariable,
            subset: Tuple[Union[RandomVariable, type(...)], ...],
            ignore: Union[SetOfRandomVariable, None] = None) -> SetOfRandomVariable:
        """
        Replace ellipsis (...) in subset for variables - subset - ignore
        """
        if Ellipsis not in subset:
            return SetOfRandomVariable(subset)

        ignore = SetOfRandomVariable(tuple()) if ignore is None else ignore
        index = subset.index(...)

        head = subset[:index]
        middle = tuple(set(variables) - set(subset) - set(ignore))
        tail = subset[index + 1:]

        return SetOfRandomVariable(head + middle + tail)
