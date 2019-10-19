class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

    def get_next(self):
        return self.next

    def get_value(self):
        return self.value

    def append(self, node):
        if self.next != None:
            raise ValueError("Append to non-empty node")
        self.next = node

    def is_end(self):
        return self.next == None

    def tail(self):
        if self.next == None:
            return self
        else:
            return self.next.tail()

    def delete_next(self):
        if self.next != None:
            self.next = self.next.get_next()

    def insert_after(self, value):
        #insert a value after the current node
        node = Node(value)
        node.next = self.next
        self.next = node

    def insert_list_after(self, node):
        #insert the list starting with node into the current list after the current node
        if node == None:
            return  #nothing to do
        list_tail = node.tail()
        assert(list_tail != None)
        list_tail.next = self.next
        self.next = node

    def length(self):
        if self.next == None:
            return 1
        else:
            return 1 + self.next.length()

    def find_by_index(self, index):
        if index == 0:
            return self.value
        if self.next == None:
            raise IndexError("Attempt to index past end of list")
        return self.next.find_by_index(index - 1)

    #generate a python list from the linked list
    def list(self):
        lst = []
        node = self
        while node != None:
            lst.append(node.get_value())
            node = node.get_next()
        return lst

def test_node():
    n1 = Node(1)
    assert(n1.get_value() == 1)
    assert(n1.get_next() == None)
    assert(n1.length() == 1)
    
    n2 = Node(2)
    assert(n1.is_end())
    n1.append(n2)
    assert(not n1.is_end())
    assert(n1.length() == 2)
    
    n3 = Node(3)
    assert(n2.is_end())
    n2.append(n3)
    assert(not n2.is_end())
    assert(n1.length() == 3)

    n4 = Node(4)
    try:
        n1.append(n4)
    except ValueError as err:
        assert "Append to non-empty node" in str(err)

    n3.append(n4)
    assert(n1.length() == 4)
    assert(n1.tail() is n4)

    n1.delete_next()
    assert(n1.length() == 3)
    assert(n1.get_next() is n3)

    #create a new little list
    n5 = Node(5)
    n6 = Node(6)
    n5.append(n6)
    n7 = Node(7)
    n6.append(n7)
    assert(n5.length() == 3)

    assert(n1.length() == 3)
    n1.insert_list_after(n5)  #insert n5 and its list after n1 in its list
    assert(n1.length() == 6)
    assert(n1.get_next() is n5)
    assert(n7.get_next() is n3)

    lst = n1.list()
    assert(lst == [1,5,6,7,3,4])

    n1 = Node(1)
    n2 = Node(2)
    n1.append(n2)
    n3 = Node(3)
    n2.append(n3)
    n1.insert_after(42)
    assert(n1.list() == [1,42,2,3])
    n1.delete_next()
    assert(n1.list() == [1,2,3])
    assert(n1.find_by_index(0) == 1)
    assert(n1.find_by_index(1) == 2)
    assert(n1.find_by_index(2) == 3)
