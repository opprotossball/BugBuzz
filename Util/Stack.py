
class Element:
    def __init__(self, val, next):
        self.value = val
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def put(self, el):
        self.top = Element(el, self.top)

    def pop(self):
        el = self.top
        if el is not None:
            self.top = self.top.next
        return el

    def __copy__(self):
        stack = Stack()
        endStack = Stack()
        el = self.top
        while el is not None:
            stack.put(el.val)
        while not stack.isEmpty():
            endStack.put(stack.pop)
        return endStack

    def isEmpty(self):
        return self.top is None
