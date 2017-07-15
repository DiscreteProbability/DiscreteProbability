class Utils:

    @staticmethod
    def parse_lazy_notation(variables, subset, ignore=None):
        """
        Replace ellipsis (...) in subset for variables - subset - ignore

        :param variables:
        :param subset:
        :param ignore:

        :return:
        """
        ignore = [] if ignore is None else ignore

        index = subset.index(...)

        head = subset[:index]
        middle = tuple(set(variables) - set(subset) - set(ignore))
        tail = subset[index + 1:]

        return head + middle + tail
