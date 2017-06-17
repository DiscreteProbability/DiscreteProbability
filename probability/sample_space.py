from probability.probability import Probability2 as Probability
from probability.random_variable import RandomVariable


class SampleSpace(object):

    def __init__(self, data_frame):
        self.data = data_frame

    @property
    def P(self):
        """
        :return: ℙ
        """
        return Probability(self)

    @property
    def variables(self):
        return [RandomVariable(column) for column in self.data.columns[0:-1]]

    @property
    def values(self):
        return self.data[self.data.columns[-1]]

'''
import pandas as pd

data = [
    ['a1', 'b1', 'c1', 1/8],
    ['a1', 'b1', 'c2', 1/8],
    ['a1', 'b2', 'c1', 1/8],
    ['a1', 'b2', 'c2', 1/8],
    ['a2', 'b1', 'c1', 1/8],
    ['a2', 'b1', 'c2', 1/8],
    ['a2', 'b2', 'c1', 1/8],
    ['a2', 'b2', 'c2', 1/8],
]

dataframe = pd.DataFrame(data, columns=['A', 'B', 'C', 'Value'])
sample_space = SampleSpace(dataframe)
A = Variable('A')
B = Variable('B')
C = Variable('C')

P = sample_space.P
print(P(A))
print(P(B))
'''