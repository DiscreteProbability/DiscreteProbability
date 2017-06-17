import pandas as pd
from probability.random_variable import RandomVariable


class Probability2(object):

    def __init__(self, sample_space):
        self.sample_space = sample_space

    def __call__(self, *args, **kwargs):
        print(args, kwargs)
        variable = args[0]

        if type(variable) == RandomVariable:
            return self._probability_variable(*args)
        else:
            return self._probability_value(variable)

    def _probability_variable(self, *args):
        variables = [variable.name for variable in args]
        df = self.sample_space.data

        return df.groupby(variables).sum()

    def _probability_value(self, variable_value):
        space = self.sample_space
        df = self.sample_space.data
        value_column = df.columns[-1]

        name = variable_value.variable.name
        value = variable_value.value

        return df[df[name] == value][value_column].sum() / space.values.sum()


def ProbabilityCalculator(sample_space, *args, **kwargs):
    class P(object):

        def __init__(self, *args, **kwargs):
            self.value = ProbabilityCalculator(sample_space, *args, **kwargs)

        def __truediv__(self, other):
            return self.value / other.value

    if not args:
        return 0

    elif isinstance(args[0], Conditional):
        S = sample_space
        conditional = args[0]

        x = conditional.x
        y = conditional.y

        return P(x, y) / P(y)

    # Marginal
    elif len(args) == 1:
        x = args[0].key
        return sample_space[x].sum()

    # Conjunta
    else:
        x = args[0].key
        y = args[1].key

        return sample_space[x][y]

    raise Exception('Não tratei isso ainda')


class Probability(object):
    @staticmethod
    def for_sample_space(sample_space):
        """
        :param sample_space bidimentional dataframe
        """
        return lambda *args, **kwargs: ProbabilityCalculator(sample_space, *args, **kwargs)


class Conditional(object):
    def __init__(self, x, given_y):
        self.x = x
        self.y = given_y

    def __repr__(self):
        return "'{}' given '{}'".format(self.x, self.y)


class Event(object):
    def __init__(self, key):
        self.key = key

    def __or__(self, other):
        return Conditional(self, other)

"""
P = Probability.for_sample_space(item_b)
'''
def P(X, Y):
    print(item_b)
'''



a = Event('a')
b = Event('b')

print('P() =', P())
print('P(a) =', P(a))
print('P(a, b) =', P(a, b))
print('P(a | b) =', P(a | b))

#P(X==x | Y==y) = P(X==x, Y==y)/P(Y==y)
"""