class Stack:
    def __init__(self):
        self.stack = []

    @property
    def get_stack(self):
        return self.stack

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        self.stack.pop()


stack = Stack()

if __name__ == "__main__":
    stack.push(1)
    stack.push(2)
    print(stack.get_stack)
    stack.pop()
    print(stack.get_stack)
    stack.push(3)
    stack.push(4)
    print(stack.get_stack)
    stack.pop()
    print(stack.get_stack)
