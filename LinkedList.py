class SinglyLinkedList:
    class ListNode:
        def __init__(self, data = None):
            self.data = data
            self.next = None
    _Length = 0
    _MinusOneElement = None # buffer element
    _LastElement = None
    _IterPtr = None

 
    def __init__(self):
        self._MinusOneElement = self.ListNode()
        self._LastElement = self._MinusOneElement
        self._Length = 0
    
    def __repr__(self):
        return "SinglyLinkedList()"

    def __str__(self):
        result = "["
        First = True
        for i in self:
            if First:
                result += str(i) 
                First = False 
            else: 
                result+= ", " + str(i)
        result += "]"
        return result

    def _deletenext(self, ptr: ListNode):
        ptr.next = ptr.next.next
        self._Length -= 1

    # iteration
    def __next__(self):
        self._IterPtr = self._IterPtr.next
        if self._IterPtr == None:
            raise StopIteration
        return self._IterPtr.data
    def __iter__(self):
        self._IterPtr = self._MinusOneElement
        return self

    # gets item or a slice, O(n) time in both cases, O(1) and O(n) space
    def __getitem__(self, index):
        if type(index) == int:
            if index >= self._Length or index<0:
                raise Exception("Index out of range")
            ptr = self._MinusOneElement.next
            while index > 0:
                ptr = ptr.next
                index -= 1
            return ptr.data
        else:
            New = self.__class__()
            if index.step == None or index.step > 0:
                add = New.append
                index = (index.start if index.start!= None else 0,
                         index.stop if index.start!= None else self._Length,
                         index.step if index.step != None else 1)
            elif index.step < 0:
                add = New.insert
                index = (index.start if (index.start!= None and index.start<self._Length) else (self._Length - 1),
                         index.stop if index.stop!= None else -1,
                         -index.step)
                index = (index[1] + ((index[0] - index[1] - 1)%index[2]) + 1, 
                         index[0] + 1,
                         index[2])
            else:
                raise Exception("slice step cannot be zero")
            if self._Length <= index[0]:
                return New
            i = 0
            ptr = self._MinusOneElement.next
            while i < index[0]:
                ptr = ptr.next 
                i += 1
            if i >= index[1]:
                return New
            while True:
                add(ptr.data)
                j = 0
                while j < index[2]:
                    ptr = ptr.next
                    i += 1
                    if ptr == None or i >= index[1]:
                        return New 
                    j+= 1

    # adds last element, O(1) time and space
    def append(self, data): 
        self._LastElement.next = self.ListNode(data)
        self._LastElement = self._LastElement.next
        self._Length += 1

    # adds new first element, O(1) time and space
    def insert(self, data): 
        ptr = self.ListNode(data)
        ptr.next = self._MinusOneElement.next
        self._MinusOneElement.next = ptr 
        self._Length += 1

    # extends list from the end, O(n) time and space, O(1) time and space if suffix is SinglyLinkedList and Copy is false, but it destroys suffix object
    def extend(self, suffix): 
        Copy = True
        if type(suffix) == SinglyLinkedList and not Copy:
            if suffix.length() != 0:
                self._LastElement.next = suffix._MinusOneElement.next
                self._LastElement = suffix._LastElement
                suffix._MinusOneElement.next = None
                self._Length += suffix._Length
                suffix._Length = 0
            return self
        elif hasattr(suffix, '__iter__'):
            for i in suffix:
                self.append(i)
            return self
        else: 
            raise Exception("'" +str(type(suffix))+ "' object is not iterable")

    # pops first element, O(1) time and space
    def popfirst(self):
        if self._Length == 0:
            raise Exception("Trying to pop element from empty linked list")
        ptr = self._MinusOneElement.next
        self._MinusOneElement.next = self._MinusOneElement.next.next 
        self._Length -= 1
        return ptr.data 

    # pops last element, O(n) time, O(1) space
    def popLast(self):
        if self._Length == 0:
            raise Exception("Trying to pop element from empty linked list")
        ptr = self._MinusOneElement
        while ptr.next != self._LastElement:
            ptr = ptr.next 
        self._LastElement = ptr
        ptr = ptr.next
        self._LastElement.next = None
        self._Length -= 1
        return ptr.data

    # returns length of list, O(1) time and space
    def length(self):
        return self._Length

    # reverses list, O(n) time, O(1) space
    def reverse(self):
        if self._Length <= 1:
            return 
        ptr1 = self._MinusOneElement
        ptr2 = self._MinusOneElement.next
        ptr3 = self._MinusOneElement.next.next
        while ptr3 != None:
            ptr1 = ptr2 
            ptr2 = ptr3 
            ptr3 = ptr3.next
            ptr2.next = ptr1 
        self._LastElement = self._MinusOneElement.next
        self._LastElement.next = None 
        self._MinusOneElement.next = ptr2 
        return self

    # bubble sort, O(1) space, O(n^2) average and max, O(n) time in case sorting after inserting element into sorted list
    def sort(self, comparator = lambda a, b: a<=b):
        self._IterPtr = self._MinusOneElement
        if self._MinusOneElement.next == None:
            return
        if self._MinusOneElement.next.next == None:
            return
        Unfinished = True
        while(Unfinished):
            Unfinished = False
            ptr1 = self._MinusOneElement
            while ptr1.next.next!=None:
                if not comparator(ptr1.next.data, ptr1.next.next.data):
                    Unfinished = True
                    ptr2 = ptr1.next 
                    ptr1.next = ptr2.next
                    ptr2.next = ptr1.next.next
                    ptr1.next.next = ptr2 
                ptr1 = ptr1.next
        while self._LastElement.next != None:
            self._LastElement = self._LastElement.next
        return self

    # quick sort, O(n log(n)) average time, O(log n) average space
    def qsort(self, comparator = lambda a, b: a<=b):
        self._IterPtr = self._MinusOneElement
        if self._MinusOneElement.next == None or self._MinusOneElement.next.next == None:
            return
        def recursiveSorting(start, stop):
            if start.next == stop:
                return
            ptr = None
            ptrleft = start 
            ptrright = start
            ptrmid = start.next
            while ptrright.next != stop:
                if comparator(ptrmid.data, ptrright.next.data):
                    ptrright = ptrright.next
                else:
                    ptr = ptrright.next
                    ptrright.next = ptrright.next.next
                    ptr.next = ptrleft.next
                    ptrleft.next = ptr 
                    ptrleft = ptr
            recursiveSorting(start, ptrmid)
            recursiveSorting(ptrmid, stop) 
        recursiveSorting(self._MinusOneElement, None)
        while self._LastElement.next != None:
            self._LastElement = self._LastElement.next
        return self

    # count number of elements that are equal to counter or s.t. counter(data) == True, O(n)
    def count(self, counter):  
        if not callable(counter):
            compareto = counter
            counter = lambda x: compareto == x
        num = 0
        ptr = self._MinusOneElement.next 
        while(ptr != None):
            if counter(ptr.data):
                num += 1
            ptr = ptr.next
        return num

    # creates copy of list, except iterator position, O(n) time and space
    def copy(self):
        New = self.__class__()
        for i in self:
            New.append(i)
        return New
    
    # clears list
    def clear(self):
        self._Length = 0
        self._LastElement = self._MinusOneElement
        self._IterPtr = self._MinusOneElement
        self._MinusOneElement.next = None

    # deletes first n (all if n == -1) elements equal to condition or s.t. condition(x) == True, O(n)
    def deleteif(self, condition, n = -1):
        if n<0:
            n = self._Length
        if not callable(condition):
            compareto = condition
            condition = lambda x: compareto == x
        ptr = self._MinusOneElement
        while ptr.next != None and n > 0:
            if condition(ptr.next.data):
                self._deletenext(ptr)
                n -= 1
            else:
                ptr=ptr.next 
        self._LastElement = ptr
        return self

    # creates sublist of items where condition(x) == True, O(n)
    def sublist(self, condition):
        New = self.__class__()
        ptr = self._MinusOneElement
        while ptr.next != None:
            if condition(ptr.next.data):
                New.append(ptr.next.data)
            ptr=ptr.next 
        return New





class DoublyLinkedList(SinglyLinkedList):
    class ListNode:
        def __init__(self, data = None):
            self.data = data
            self.next = None
            self.prev = None
    
    def __repr__(self):
        return "DoublyLinkedList()"

    def _deletenext(self, ptr: ListNode):
        if ptr.next.next == None:
            ptr.next = None 
            self._LastElement = ptr
        else:
            ptr.next.next.prev = ptr 
            ptr.next = ptr.next.next
        self._Length -= 1

    # adds last element, O(1) time and space
    def append(self, data):
        self._LastElement.next = self.ListNode(data)
        self._LastElement.next.prev = self._LastElement
        self._LastElement = self._LastElement.next
        self._Length += 1

    # adds first element, O(1) time and space
    def insert(self, data):
        ptr = self.ListNode(data)
        ptr.next = self._MinusOneElement.next
        if self._Length != 0:
            self._MinusOneElement.next.prev = ptr
        self._MinusOneElement.next = ptr
        ptr.prev = self._MinusOneElement
        self._Length += 1 

    # extends list from the end, O(n) time and space, O(1) time and space if suffix is DoublyLinkedList and Copy is false, but it destroys suffix object
    def extend(self, suffix, Copy = True): 
        if type(suffix) == SinglyLinkedList and not Copy:
            if suffix._Length != 0:
                self._LastElement.next = suffix._MinusOneElement.next
                suffix._MinusOneElement.next.prev = self._LastElement
                self._LastElement = suffix._LastElement
                suffix._MinusOneElement.next = None
                self._Length += suffix._Length
                suffix._Length = 0
            return self
        elif hasattr(suffix, '__iter__'):
            for i in suffix:
                self.append(i)
            return self
        else: 
            raise Exception("'" +str(type(suffix))+ "' object is not iterable")

    # pops first element, O(1) time and space
    def popfirst(self):
        if self._Length == 0:
            raise Exception("Trying to pop element from empty linked list")
        ptr = self._MinusOneElement.next
        self._MinusOneElement.next = self._MinusOneElement.next.next 
        if self._MinusOneElement.next != None:
            self._MinusOneElement.next.prev = self._MinusOneElement
        self._Length -= 1
        return ptr.data 

    # pops last element, O(1) time and space
    def popLast(self):
        if self._Length == 0:
            raise Exception("Trying to pop element from empty linked list")
        ptr = self._LastElement
        self._LastElement = self._LastElement.prev
        self._LastElement.next=None
        self._Length -= 1
        return ptr.data

    # reverses list, O(n) time, O(1) space
    def reverse(self):
        if self._Length <= 1:
            return 
        ptr1 = self._MinusOneElement
        ptr2 = self._MinusOneElement.next
        ptr3 = self._MinusOneElement.next.next
        while ptr2 != None:
            ptr2.next = ptr1
            ptr2.prev = ptr3
            ptr1 = ptr2 
            ptr2 = ptr3 
            ptr3 = ptr3.next
        self._LastElement = self._MinusOneElement.next
        self._LastElement.next = None
        self._MinusOneElement.next = ptr1
        self._MinusOneElement.next.prev = self._MinusOneElement
        return self

    # bubble sort, O(1) space, O(n^2) average and max, O(n) time in case sorting after inserting element into sorted list
    def sort(self, comparator = lambda a, b: a<=b):
        self._IterPtr = self._MinusOneElement
        if self._MinusOneElement.next == None:
            return
        if self._MinusOneElement.next.next == None:
            return
        Unfinished = True
        while(Unfinished):
            Unfinished = False
            ptr1 = self._MinusOneElement.next
            while ptr1.next!=None:
                if not comparator(ptr1.data, ptr1.next.data):
                    Unfinished = True
                    ptr2 = ptr1.next
                    ptr1.prev.next = ptr2
                    if ptr2.next!= None:
                        ptr2.next.prev = ptr1
                    ptr1.next = ptr2.next
                    ptr2.prev = ptr1.prev
                    ptr1.prev = ptr2
                    ptr2.next = ptr1
                else:
                    ptr1 = ptr1.next
        while self._LastElement.next != None:
            self._LastElement = self._LastElement.next
        return self

    # quick sort, O(n log(n)) average time, O(log n) average space
    def qsort(self, comparator = lambda a, b: a<=b):
        self._IterPtr = self._MinusOneElement
        if self._MinusOneElement.next == None or self._MinusOneElement.next.next == None:
            return
        def recursiveSorting(start, stop):
            if start.next == stop:
                return
            ptr = None
            ptrleft = start 
            ptrright = start
            ptrmid = start.next
            while ptrright.next != stop:
                if comparator(ptrmid.data, ptrright.next.data):
                    ptrright = ptrright.next
                else:
                    ptr = ptrright.next
                    ptrright.next = ptrright.next.next
                    if ptrright.next != None:
                        ptrright.next.prev = ptrright
                    ptr.next = ptrleft.next
                    ptr.prev = ptrleft
                    ptrleft.next = ptr 
                    ptr.next.prev = ptr
                    ptrleft = ptr
            recursiveSorting(start, ptrmid)
            recursiveSorting(ptrmid, stop) 
        recursiveSorting(self._MinusOneElement, None)
        while self._LastElement.next != None:
            self._LastElement = self._LastElement.next
        return self

    # iterares from the end
    def reverseiterator(self):
        ptr = self._LastElement
        while ptr!=self._MinusOneElement:
            yield ptr.data
            ptr=ptr.prev






        


            


                    


        
    



