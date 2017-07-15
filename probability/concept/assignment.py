from probability.other.container_variable import ContainerVariable


class Assignment(ContainerVariable):
    """
    Assign a
    """

    def __init__(self, random_variable, event_assigned):
        """
        :param RandomVariable random_variable:
        :param Event event_assigned:
        """
        self._random_variable = random_variable
        self.event = event_assigned

    def __repr__(self):
        if self.event.is_singleton:
            return '{} = {}'.format(self.random_variable, self.event)
        else:
            return '{} ∈ {}'.format(self.random_variable, self.event)

    @property
    def name(self):
        return self.random_variable.name

    def __hash__(self):
        return self.name.__hash__()

    @property
    def random_variable(self):
        return self._random_variable

    @property
    def as_set(self):
        return {self.random_variable}

    @property
    def assigned(self):
        return True

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return super.__eq__(self, other)

        return self.random_variable == other.random_variable \
           and self.event == other.event
