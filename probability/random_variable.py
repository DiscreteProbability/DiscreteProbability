class RandomVariable(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) == RandomVariable:
            return self.name == other.name
        else:
            return RandomVariableValue(self, other)

    def __repr__(self):
        return self.name


class RandomVariableValue(object):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def __repr__(self):
        return '{} = {}'.format(self.variable, self.value)
