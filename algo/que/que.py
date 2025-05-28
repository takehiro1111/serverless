from collections import deque
from typing import List


class Que:
    def __init__(self):
        self.que = []

    @property
    def get_que(self):
        return self.que

    def enqueue(self, data):
        self.que.append(data)

    def deque(self):
        self.que.pop(0)

    def que_reverse(self, queue: list[int]):
        new_que = []
        while queue:
            new_que.append(queue.pop())

        return new_que


if __name__ == "__main__":
    # q = deque()
    # q.append(1)
    # q.append(2)
    # q.append(3)
    # q.append(4)
    # q.append(5)
    # print(q)
    # q.popleft()
    # q.popleft()
    # q.popleft()
    # print(q)

    q = Que()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)
    print(q.get_que)
    q.deque()
    q.deque()
    q.deque()
    print(q.get_que)

    print(q.que_reverse(q.get_que))
