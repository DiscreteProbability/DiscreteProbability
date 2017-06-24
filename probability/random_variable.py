class RandomVariable(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) == RandomVariable:
            return self.name == other.name
        else:
            return RandomVariableEvent(self, other)

    def __repr__(self):
        return self.name

    def union(self, other):
        return UnionRandomVariable(self, other)

    def __or__(self, other):
        return ConditionalRandomVariable(self, other)


class RandomVariableEvent(object):

    def __init__(self, variable, event):
        self.variable = variable
        self.event = event

    def __repr__(self):
        return '{} = {}'.format(self.variable, self.event)

    @property
    def name(self):
        return self.variable.name


class UnionRandomVariable(object):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


class ConditionalRandomVariable(object):

    def __init__(self, X, Y):
        self.of = X
        self.given = Y
