# Write a Python class that simulates a Queue. The class should implement methods like push, pop, peek (the last two
# methods should return None if no element is present in the queue).

class Queue:
    def __init__(self):
        self.queue = []

    def push(self, value):
        self.queue.append(value)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def peek(self):
        if self.queue:
            return self.queue[0]
        return None

    def __len__(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def __str__(self):
        return f"Queue({self.queue})"


queue = Queue()
queue.push(1)
queue.push(2)
queue.push(3)
print(queue.pop())
print(queue.peek())
print(queue.is_empty())
print(len(queue))
print(queue)
