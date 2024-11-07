# Write a Python class that simulates a Stack. The class should implement methods like push, pop, peek (the last two
# methods should return None if no element is present in the stack).

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        return None

    def __len__(self):
        return len(self.stack)

    def is_empty(self):
        return len(self.stack) == 0

    def __str__(self):
        return f"Stack({self.stack})"


stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.pop())
print(stack.peek())
print(stack.is_empty())
print(len(stack))
print(stack)
