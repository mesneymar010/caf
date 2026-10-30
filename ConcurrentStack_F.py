import threading

class ConcurrentStack:
    def __init__(self):
        self.stack = []
        self.lock = threading.Lock()

    def push(self, x):
        with self.lock:
            self.stack.append(x)

    def pop(self):
        with self.lock:
            return self.stack.pop() if self.stack else "Stack Empty"

    def display(self):
        with self.lock:
            print(self.stack)

def push_items(s, values):
    for x in values:
        s.push(x)

s = ConcurrentStack()

t1 = threading.Thread(target=push_items, args=(s, [10, 20]))
t2 = threading.Thread(target=push_items, args=(s, [30, 40]))

t1.start()
t2.start()
t1.join()
t2.join()

print("Stack:")
s.display()

print("Popped:", s.pop())
print("After Pop:")
s.display()