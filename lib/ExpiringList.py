import arrow


class ExpiringList(list):
    def __init__(self, max_age: int):
        """
        :param max_age: The maximum age of an item in the list in seconds
        """
        self.max_age = max_age
        self.age_list: list[arrow.Arrow] = []
        super().__init__()

    def remove_expired(self):
        """
        Remove all items that are older than the maximum age
        """
        expire_before = arrow.now().shift(seconds=-self.max_age)
        while self.age_list and self.age_list[0] < expire_before:
            super().pop(0)
            self.age_list.pop(0)

    def append(self, item):
        self.remove_expired()
        self.age_list.append(arrow.now())
        super().append(item)

    def pop(self, index=-1):
        self.remove_expired()
        self.age_list.pop(index)
        return super().pop(index)

    def __len__(self) -> int:
        self.remove_expired()
        return super().__len__()


if __name__ == "__main__":
    import time

    list = ExpiringList(10)
    list.append(1)
    print(list)
    print("Sleeping for 5 seconds")
    time.sleep(5)
    list.append(2)
    print(list)
    print("Sleeping for 5 seconds")
    time.sleep(5)
    list.append(3)
    print(list)
    print("Sleeping for 5 seconds")
    time.sleep(5)
    list.append(4)
    print(list)
