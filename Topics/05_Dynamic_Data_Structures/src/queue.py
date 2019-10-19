from simple_node import Node

class Queue():
    def __init__(self):
        self.head = None
        self.tail = None

    # append a value to the end of the queue
    def append(self, value):
        node = Node(value)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    # remove the first queued element, and return its stored value
    def pop_front(self):
        if self.head == None:
            raise ValueError("Attempt to pop from empty queue")
        node = self.head
        self.head = node.next
        if self.head == None:
            self.tail = None
        return node.value

    # is the queue empty?
    def is_empty(self):
        return self.head is None

def test_queue():
    q = Queue()
    try:
        q.pop_front()
    except ValueError as err:
        assert("Attempt to pop from empty queue" in str(err))
    
    lst = [1,2,3,5,6,7,8,9,10]
    for item in lst:
        q.append(item)

    lst2 = []
    while not q.is_empty():
        lst2.append(q.pop_front())

    assert(lst2 == lst)
    try:
        q.pop_front()
    except ValueError as err:
        assert("Attempt to pop from empty queue" in str(err))
