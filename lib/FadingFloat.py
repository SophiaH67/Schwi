from .ExpiringList import ExpiringList


class FadingFloat:
    def __init__(self, base_value: float, max_age: int):
        """
        :param max_age: The maximum age of an item in the list in seconds
        """
        self.base_value = base_value
        self.expiring_list = ExpiringList(max_age)

    def __float__(self):
        return self.base_value + sum(self.expiring_list)

    def __add__(self, other):
        self.expiring_list.append(other)
        return self

    def __sub__(self, other):
        self.expiring_list.append(-other)
        return self

    def __mul__(self, other):
        self.expiring_list.append(other)
        return self

    def __truediv__(self, other):
        self.expiring_list.append(1 / other)
        return self

    def __str__(self):
        return str(self.__float__())

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return int(self.__float__())

    def __bool__(self):
        return self.__float__() != 0

    def __lt__(self, other):
        return self.__float__() < other

    def __le__(self, other):
        return self.__float__() <= other

    def __eq__(self, other):
        return self.__float__() == other

    def __ne__(self, other):
        return self.__float__() != other

    def __gt__(self, other):
        return self.__float__() > other

    def __iadd__(self, other):
        self.expiring_list.append(other)
        return self
