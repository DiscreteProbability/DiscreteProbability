class ConditionalRandomVariable(object):

    def __init__(self, query_variables, evidences):
        """
        *query_variables given evidences*

        :param RandomVariables query_variables:
        :param RandomVariables evidences:
        """
        self.query_variables = query_variables
        self.evidences = evidences

    def __repr__(self):
        query = self.query_variables
        evidences = self.evidences

        return '{} | {}'.format(query, evidences)
