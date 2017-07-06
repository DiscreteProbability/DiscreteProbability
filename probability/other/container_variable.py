from abc import ABCMeta, abstractmethod


class ContainerVariable(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        return None

    @property
    @abstractmethod
    def random_variable(self):
        return None

