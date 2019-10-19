from linked_list import Node

class LinkedList():
    def __init__(self):
        self.head_node = None
        self.tail_node = None
        self.list_length = 0

    # return the head node
    def head(self):
        return self.head_node

    # return the tail node
    def tail(self):
        return self.tail_node

    # return the list length
    def length(self):
        return self.list_length

    # append a value to the list
    def append(self, value):
        node = Node(value)
        self.list_length += 1
        if self.head_node == None:
            self.head_node = node
            self.tail_node = node
        else:
            assert(self.tail_node.next == None)
            self.tail_node.next = node
            self.tail_node = node

    # return a copy of the list
    def copy(self):
        newlist = LinkedList()
        node = self.head_node
        while node != None:
            newlist.append(node.value)
            node = node.next
        return newlist
            
    # append the contents of llist to this list
    def append_list(self, llist):
        if llist.length() == 0:
            return
        # First make a copy.  Otherwise the original llist will still
        # index the same nodes, and then modifications will leave the
        # lists head, tail or length out of sync.
        llist_copy = llist.copy()
        if self.head_node == None:
            self.head_node = llist_copy.head_node
            self.tail_node = llist_copy.tail_node
        else:
            self.tail_node.next = llist_copy.head_node
            self.tail_node = llist_copy.tail_node
        self.list_length += llist_copy.length()

    # remove the first element of the list, and return its stored value
    def pop_front(self):
        if self.head_node == None:
            raise IndexError("Attempt to pop from empty list")
        node = self.head_node
        self.head_node = node.next
        if self.head_node == None:
            self.tail_node = None
        self.list_length -= 1
        return node.get_value()

    # find the node at position index
    def get_node_by_index(self, index):
        if self.head_node == None:
            raise IndexError("Attempt to index past end of list")
        node = self.head_node
        if index < 0:
            raise IndexError("Invalid negative index")
        while index > 0:
            node = node.get_next()
            if node == None:
                raise IndexError("Attempt to index past end of list")
            index -= 1
        return node

    # return the value stored at position index
    def get_value(self, index):
        node = self.get_node_by_index(index)
        return node.get_value()

    # insert the value in the list, after the node at position index
    def insert_after(self, index, value):
        node = self.get_node_by_index(index)
        newnode = Node(value)
        newnode.next = node.next
        node.next = newnode
        if newnode.next == None:
            self.tail_node = newnode
        self.list_length += 1

    # insert the value in the list, before the node at position index
    def insert_before(self, index, value):
        newnode = Node(value)
        if index == 0:
            newnode.next = self.head_node
            if self.head_node == None:  # insert_before(0,*) should still work on an empty list
                self.tail_node = newnode
            self.head_node = newnode
        else:
            node = self.get_node_by_index(index - 1)
            newnode.next = node.next
            node.next = newnode
        self.list_length += 1

    #generate a python list from the linked list
    def list(self):
        return self.head_node.list()

def test_list():
    llist = LinkedList()
    assert(llist.length() == 0)
    try:
        llist.get_value(0)
    except IndexError as err:
        assert("Attempt to index past end of list" in str(err))
    
    llist.append(0)
    assert(llist.length() == 1)
    assert(llist.get_value(0) == 0)
    try:
        llist.get_value(1)
    except IndexError as err:
        assert("Attempt to index past end of list" in str(err))
    assert(llist.list() == [0])

    llist.append(1)
    assert(llist.length() == 2)
    assert(llist.list() == [0,1])
    assert(llist.tail_node.value == 1)

    llist.insert_before(1, 3)
    assert(llist.length() == 3)
    assert(llist.list() == [0,3,1])
    assert(llist.tail_node.value == 1)

    llist.insert_before(0, 4)
    assert(llist.length() == 4)
    assert(llist.list() == [4,0,3,1])
    assert(llist.tail_node.value == 1)

    llist.insert_after(0, 5)
    assert(llist.length() == 5)
    assert(llist.list() == [4,5,0,3,1])
    assert(llist.tail_node.value == 1)
    
    llist.insert_after(4, 6)
    assert(llist.length() == 6)
    assert(llist.list() == [4,5,0,3,1,6])
    assert(llist.tail_node.value == 6)
    
    assert(llist.pop_front() == 4)
    assert(llist.length() == 5)
    assert(llist.list() == [5,0,3,1,6])
    assert(llist.tail_node.value == 6)

    assert(llist.pop_front() == 5)
    assert(llist.pop_front() == 0)
    assert(llist.pop_front() == 3)
    assert(llist.pop_front() == 1)
    assert(llist.pop_front() == 6)
    try:
        llist.pop_front()
    except IndexError as err:
        assert("Attempt to pop from empty list" in str(err))

    llist.append(1)
    llist.append(2)
    llist.append(3)
    assert(llist.list() == [1,2,3])
    llist2 = llist.copy()
    assert(llist2.list() == [1,2,3])
    llist.append(4)
    llist2.append(5)
    assert(llist.list() == [1,2,3,4])
    assert(llist2.list() == [1,2,3,5])
    
    llist.append_list(llist2)
    assert(llist.list() == [1,2,3,4,1,2,3,5])
    assert(llist.length() == 8)
    assert(llist.tail_node.value == 5)

    #test corner cases of empty lists
    llist3 = LinkedList()
    llist4 = llist3.copy()
    assert(llist4.length() == 0)
    assert(llist4.head_node == None)
    assert(llist4.tail_node == None)
    llist3.append_list(llist4)
    assert(llist3.length() == 0)
    assert(llist3.head_node == None)
    assert(llist3.tail_node == None)

    llist4.append(42)
    llist3.append_list(llist4)
    assert(llist3.length() == 1)
    assert(llist3.head_node.value == 42)
    assert(llist3.tail_node.value == 42)
