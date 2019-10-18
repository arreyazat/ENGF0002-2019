class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, node):
        if self.next != None:
            raise ValueError("Append to non-empty node")
        self.next = node

    def delete_next(self):
        if self.next != None:
            self.next = self.next.next


def test_node():
    n1 = Node(1)
    assert(n1.value == 1)
    assert(n1.next == None)
    
    n2 = Node(2)
    n1.append(n2)
    assert(not n1.next is None)
    
    n3 = Node(3)
    assert(n2.next is None)
    n2.append(n3)
    assert(not n2.next is None)

    n4 = Node(4)
    try:
        n1.append(n4)
    except ValueError as err:
        assert "Append to non-empty node" in str(err)

    n3.append(n4)
    node = n1
    count = 1
    while not node.next is None:
        node = node.next
        count += 1

    assert(node == n4)
    assert(count == 4)

    n1.delete_next()
    assert(n1.next is n3)

    n1.delete_next()
    assert(n1.next is n4)

    n1.delete_next()
    assert(n1.next is None)

    # no error when deleting from end of list
    n1.delete_next()
    assert(n1.next is None)
