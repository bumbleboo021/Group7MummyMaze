class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
class Queue:
    def __init__(self):
        self.head = None
        self.len = 0
        self.tail = None
    def push(self, val):
        new_node = Node(val)
        if self.len == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = self.tail.next
        self.len += 1
        pass
    def pop(self):
        if self.len == 0:
            return -1
        val = self.head.val
        self.head = self.head.next
        if self.len == 1:
            self.tail = None

        self.len -= 1
        return val
    def pr(self):
        cur = self.head
        while cur is not None:
            print(cur.val,end = " ")
            cur = cur.next
        print()

