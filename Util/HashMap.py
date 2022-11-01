class ListNode:
    def __init__(self, key_long, val):
        self.key_long = key_long
        self.value = val
        self.next = None


class HashMap:
    def __init__(self, size):
        self.size = size
        self.list = [None] * size

    def put(self, key, value):
        long_key = key
        index = key % self.size
        if self.list[index] is not None:
            self.list[index] = ListNode(long_key, value)
        else:
            current = self.list[index]
            while current is not None:
                if current.key_long == long_key:
                    current.pair = value
                    return
                current = current.next
            current.next = ListNode(long_key, value)

    def get(self, key):
        long_key = key

        index = key % self.size
        current = self.list[index]

        while current is not None:
            if current.key_long == long_key:
                return current.value
            else:
                current = current.next

        return None
