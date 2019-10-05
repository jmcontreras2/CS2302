import math
import random
import time

global PrintCounter
global InsertCounter
global DeleteCounter
global MergeCounter
global IndexOfCounter
global MinCounter
global MaxCounter
global HasDuplicatesCounter
global SelectCounter
global SelectInsertCounter

class Node(object):
    #constructor
  def __init__(self, data, next = None):
    self.data = data
    self.next = next
    
class SortedList(object):    
    #constructor
  def __init__(self, head = None, tail = None):
    self.head = head
    self.tail = tail
    
  # I have the print method print 'empty list' to have some type of feedback when printing an empty list.
  # Else, the print method iterates through the list printing each data element.
  def Print(self):
    global PrintCounter
    PrintCounter = 1
    if self.head == None:
      print("Empty List")
    t = self.head
    while t != None: 
      print(t.data, end = '   ')
      t = t.next
      PrintCounter += 1
    print()
    print('Made ', PrintCounter, ' comparison(s) using Print() function.')
    print()
    
  # if the head is empty, we can simply place the element at the head and link the tail as well since it is only one element. 
  # Else, I compare the element to the head. If the element is less than the head, the element becomes the head and links its next to the previous head.
  # Finally, if the insert function did not hit any of the previous cases, it iterates through the list looking for a Node that is 
  # less than i. The first one it finds, it makes the element we want to insert its next. 
  # We make a final check to see if the element was greater than the tail. If it is, we know this element was placed as the tail
  # and must update the tail as such.
  def Insert(self, i):
    global InsertCounter
    global SelectInsertCounter
    InsertCounter = 1
    SelectInsertCounter = 1
    if self.head == None:
      self.head = Node(i)
      self.tail = Node(i)
    else:
      element = Node(i)
      if element.data < self.head.data:
        temp = self.head
        self.head = element
        self.head.next = temp
        if self.tail == None:
            self.tail = temp
        InsertCounter += 1
        SelectInsertCounter += 1
      else:
    
        iter = self.head
        while (iter.next != None) and (iter.next.data < i):
            iter = iter.next
            InsertCounter += 1
            SelectInsertCounter += 1
        element.next = iter.next
        iter.next = element
        iter = element
 
        if element.data > self.tail.data:
            self.tail = element
            InsertCounter += 1
            SelectInsertCounter += 1
    print('Insert() made ', InsertCounter, ' comparison(s) inserting element ', i, ' into current list.')
  
  # If the head is None, we do nothing. 
  #We then iterate through the list, looking to see when i occurs. If i occurs in the iterator's next, then we make the current
  #node's next, its next.next, so that the next (which is equal to i) is disconnected from the linked list.
  # We make a final check to see if the head was also equal to i. If it was, we make the head equal to its next so we can disconnect
  # it from the linked list. Wherever the iter stops will always be the tail so we update the tail.
  def Delete(self, i):
    global DeleteCounter
    DeleteCounter = 0
    if self.head != None:
      iter = self.head
      while iter.next != None:
        if iter.next.data == i:
          iter.next = iter.next.next  
          DeleteCounter += 1
        else:
          iter = iter.next   
          DeleteCounter += 1
      if self.head.data == i:
        self.head = self.head.next
      self.tail = iter
    print('Delete() function made ', DeleteCounter, ' comparisons for deleting element ', i, '.')
  
  # For Merge, I created a temporary sorted list. I then find an appropriate head out of the two heads that I am dealing with, the
  # current head or the M.head. Once this is decided, we iterate through the two lists, comparing the data from each iterator to see which
  # element will be added to the temporary list. Since we know the lists are sorted, we can add the element to the tail's next since
  # every element that is next will always be greater than the ones that were placed in the temporary sorted list. This was done by
  # having an iterator iterate through the temporary list as elements were added. This made the iterator the temporary list's tail at all
  # times. One list will be iterated through completely first so we put two while loops at the end to make sure that we finish iterating 
  #through the one that is not completely #iterated through. We finish by making the current's head the temporary sorted list's head and 
  #the current's tail the iterator that was iterating through the temporary list.
  
  def Merge(self, M):
    global MergeCounter
    MergeCounter = 0
    global MergeInsertCounter
    MergeInsertCounter = 0
    temp = SortedList()
    iterS = self.head
    iterM = M.head
    if iterS.data <= iterM.data:
        temp.head = iterS
        iterS = iterS.next
        MergeCounter += 1
    else:
        temp.head = iterM
        iterM = iterM.next
        MergeCounter += 1
    t = temp.head
    while iterS != None and iterM != None:
      if iterS.data <= iterM.data:
        t.next = iterS
        t = t.next
        iterS = iterS.next
        MergeCounter += 1
      else:
        t.next = iterM
        iterM = iterM.next
        t = t.next
        MergeCounter += 1
    if iterS != None:
      while iterS != None:
        t.next = iterS
        iterS = iterS.next
        t = t.next
        MergeCounter += 1
    if iterM != None:
      while iterM != None:
        t.next = iterM
        iterM = iterM.next
        t = t.next
        MergeCounter += 1
    self.head = temp.head
    self.tail = t
    print('Merge made ', MergeCounter, ' comparison(s).')


  #For IndexOf, we first check if the head is none. If it is we return -1. Elsewise, we iterate through the list until we find the
  #element i. As we iterate, we have a counter keeping track of the index that we are at in the list. Once i is found, the while loop
  #terminates and the counter is returned if iter.data is i or -1 elsewise.
  def IndexOf(self, i):
    global IndexOfCounter
    IndexOfCounter = 1
    if self.head == None:
      print('IndexOf() made 1 comparisons.')
      return -1
    else:
      iter = self.head
      counter = 0
      while iter.data != i and iter.next != None:
        iter = iter.next
        counter += 1
        IndexOfCounter += 1
      if iter.data == i:
        print()
        print('IndexOf() made ', IndexOfCounter, ' comparisons.')
        return counter
      else:
        print()
        print('IndexOf() made ', IndexOfCounter, ' comparisons.')
        return -1
       
  #To clear the list we simply make the head and tail equal none.
  def Clear(self):
    self.head = None
    self.tail = None
    print('Clear() made 0 comparisons.')
  
  #To find the min we can simply return the head of the list since it is sorted in ascending order.
  def Min(self):
    print('Min() made 1 comparison.')
    if self.head == None:
      return math.inf
    else:
      return self.head.data
  
  #To find the max we can simply return the tail of the list since it is sorted in ascending order.
  def Max(self):
    print('Max() made 1 comparison.')
    if self.head == None:
      return -math.inf
    else:
      return self.tail.data
  
  #For HasDuplicates, if the head is None we return False. Elsewise, we iterate through the linked list comparing the current
  #node with the next node to see if they equal each other. If they do, the function returns true and false otherwise. If the 
  #list is iterated through completely, it returns false.
  def HasDuplicates(self):
    global HasDuplicatesCounter
    HasDuplicatesCounter = 1
    if self.head == None:
      print('HasDuplicates made ', HasDuplicatesCounter,' comparisons.')
      return False
    else:
      iter = self.head
      while iter.next != None:
        HasDuplicatesCounter += 1
        if iter.data == iter.next.data:
          print('HasDuplicates() made ', HasDuplicatesCounter, ' comparisons.')
          return True
        iter = iter.next
      print('HasDuplicates() made ', HasDuplicatesCounter, ' comparisons.')
      return False
  
  #Since the list is sorted in ascending order, we can simply iterate through the list and have a counter keep
  # track of what nth smallest element we are at.When n == k, we know we have found the kth smallest element. 
  # We then return that node's data if we found the kth smallest element or math.inf elsewise.
  def Select(self, k):
    global SelectCounter
    SelectCounter = 1
    kth = k - 1
    if kth >= 0:
      SelectCounter += 1
      counter = 0
      iter = self.head
      while counter != kth and iter.next != None:
        iter = iter.next
        SelectCounter += 1
        counter += 1
      if counter == kth:
        print('Select() made ', SelectCounter, ' comparisons.')
        return iter.data
      else:
        print('Select() made ', SelectCounter, ' comparisons.')
        return math.inf
    else:
      print('Select() made ', SelectCounter, ' comparisons.')
      return math.inf
      
class List(object):
    #constructor
    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail
    
    # I have the print method print 'empty list' to have some type of feedback when printing an empty list.
    # Else, the print method iterates through the list printing each data element.
    def Print(self):
        global PrintCounter
        PrintCounter = 0
        if self.head == None:
          print("Empty List")
          PrintCounter += 1
        t = self.head
        while t != None:
          print(t.data, end = '   ')
          t = t.next
          PrintCounter += 1
        print('Made ', PrintCounter, ' comparison(s) using Print() function.')
        print()
    
    #Since we don't need to maintain a sorted nature to this List(), 
    #we can simply append the element i at the end of the linked list. 
    #We do this by making element i the tail's next and updting the list's
    # tail.
    def Insert(self, i):
        global InsertCounter
        InsertCounter = 0
        counter = 0
        element = Node(i)
        if self.head == None:
            counter += 1
            self.head = element
            self.tail = element
            self.head.next = self.tail
            InsertCounter += 1
        else:
            self.tail.next = element
            self.tail = element
            counter += 1
            InsertCounter += 1
        print('Insert() made ', InsertCounter, ' comparison(s) inserting element ', i, ' into current list.')
      
        
  # If the head is None, we do nothing. 
  #We then iterate through the list, looking to see when i occurs. If i occurs in the iterator's next, then we make the current
  #node's next, its next.next, so that the next (which is equal to i) is disconnected from the linked list.
  # We make a final check to see if the head was also equal to i. If it was, we make the head equal to its next so we can disconnect
  # it from the linked list. Wherever the iter stops will always be the tail so we update the tail.
    def Delete(self, i):
        global DeleteCounter
        DeleteCounter = 0
        if self.head != None:
            iter = self.head
            while iter.next != None:
                if iter.next.data == i:
                    iter.next = iter.next.next
                    DeleteCounter += 1
                else:
                    iter = iter.next
                DeleteCounter += 1
            if self.head != None:
                if self.head.data == i:
                    self.head = self.head.next
                    DeleteCounter += 1
            self.tail = iter
        print('Delete() function made ', DeleteCounter, ' comparisons for deleting element ', i, '.')
    
    # Since we don't need to keep an ascending order in List(),  Merge() iterates
    # through the list M and appends each element to the end of the current list.        
    def Merge(self, M):
        global MergeCounter
        MergeCounter = 0
        iter = M.head
        while iter != None:
            self.Insert(iter.data)
            iter = iter.next
            MergeCounter += 1
        print('Merge() made ', MergeCounter, ' comparisons.')

    #For IndexOf, we first check if the head is none. If it is we return -1. Elsewise, we iterate through the list until we find the
    #element i. As we iterate, we have a counter keeping track of the index that we are at in the list. Once i is found, the while loop
    #terminates and the counter is returned if iter.data is i or -1 elsewise.
    def IndexOf(self, i):
      global IndexOfCounter
      IndexOfCounter = 1
      if self.head == None:
        IndexOfCounter += 1
        print('IndexOf() made ', IndexOfCounter, ' comparisons.')
        return -1
      else:
        iter = self.head
        counter = 0
        while iter.data != i and iter.next != None:
          IndexOfCounter += 1
          iter = iter.next
          counter += 1
        if iter.data == i:
          print('IndexOf() made ', IndexOfCounter, ' comparisons.')
          return counter
        else:
          return -1
    
    #To clea the List(), we make the head and tail equal none.    
    def Clear(self):
        print('Clear() made 0 comparisons.')
        self.head = None
        self.tail = None
    
    #Since the List() is not sorted, we iterate through the list and find the 
    # smallest element by making the first element the min then comparing the
    #rest of the elements to this min. If the new element is smaller than the
    #current min, we assign the min variable to the new node.
    #when the iteration is complete, we return the min variable.
    def Min(self):
        global MinCounter
        MinCounter = 1
        if self.head != None:
            iter = self.head.next
            min = self.head
            while iter != None:
                MinCounter += 1
                if min.data > iter.data:
                    min = iter
                    MinCounter += 1
                iter = iter.next
            print('Min() made ', MinCounter, ' comparisons.')
            return min.data
        else:
            print('Min() made ', MinCounter, ' comparisons.')
            return math.inf
    
    #Since the List() is not sorted, we iterate through the list and find the 
    # largest element by making the first element the max then comparing the
    #rest of the elements to this max. If the new element is larger than the
    #current max, we assign the max variable to the new node.
    #when the iteration is complete, we return the max variable.
    def Max(self):
        global MaxCounter
        MaxCounter = 1
        if self.head != None:
            iter = self.head.next
            max = self.head
            while iter != None:
                MaxCounter += 1
                if max.data < iter.data:
                    max = iter
                    MaxCounter += 1
                iter = iter.next
            print('Max() made ', MaxCounter, ' comparisons.')
            return max.data
        else:
            print('Max() made ', MaxCounter, ' comparisons.')
            return -math.inf
    
    #For HasDuplicates, if the head is None we return False. Elsewise, we iterate through the linked list comparing the current
    #node with the next node to see if they equal each other. If they do, the function returns true and false otherwise. If the 
    #list is iterated through completely, it returns false.
    def HasDuplicates(self):
        global HasDuplicatesCounter
        HasDuplicatesCounter = 1
        count = 1
        countinner = 1
        if self.head == None:
            print('HasDuplicates made 1 comparison.')
            return False
        else:
            iter = self.head
            temp = iter.next
            while iter != None:
                while temp != None:
                    HasDuplicatesCounter += 1
                    if iter.data == temp.data and iter is not temp:
                        print('HasDuplicates made ', HasDuplicatesCounter, ' comparisons.')
                        return True
                    temp = temp.next
                    #print('we going inner: ', countinner)
                    countinner += 1
                #print('we going outer: ', count)
                count += 1
                iter = iter.next
                temp = self.head
                HasDuplicatesCounter += 1
        print('HasDuplicates made ', HasDuplicatesCounter, ' comparisons.')
        return False
    
    # For the Select method, I first created a temporary SortedList(). I then used the SortedList() insert method to insert the 
    # unsorted list's elements into the SortedList(). Now that the List() is sorted, we iterate through the list using a counter to
    # keep track of the nth smallest element that we are on. When n == k, we return that node or math.inf if we k was outside the bounds
    # of the length of the linked list.
    def Select(self, k):
        global SelectCounter
        global SelectInsertCounter
        SelectCounter = 0
        SelectInsertCounter = 0
        if self.head != None:
            temp = SortedList()
            iter = self.head
            while iter != None:
                temp.Insert(iter.data)
                iter = iter.next
                SelectCounter += SelectInsertCounter
            print()
            print('Printing temporary sorted list for select() function for regular List() class.')
            print()
            temp.Print()
            counter = 1
            iter = temp.head
            while iter != None and counter != k:
                iter = iter.next
                counter += 1
                SelectCounter += 1
            if iter == None:
                print('Select() made ', SelectCounter, ' comparisons.')
                return math.inf
            else:
                print('Select() made ', SelectCounter, ' comparisons.')
                return iter.data

def randomList():
    list_to_return = []
    for i in range(20):
        list_to_return += [random.randint(-100, 100)]
    return list_to_return
print()
a = randomList()
print('Printing native list to be used for testing: ', a)
print()
print('*****Testing SortedList() Functions*****')
print()
print('Printing an empty list. Expecting \'Empty List.\' Got: ', end = '')
l = SortedList()
l.Print()
print()
print('Testing Insert(). Inserting elements of a random native python list into a sorted list using insert() function.')
print()
for A in a:
    l.Insert(A)
print()
print('Printing the list: ', end = ' '), l.Print()
print()
print("Creating a list m to test Merge() with.")
print()
b = randomList()
m = SortedList()
for B in b:
    m.Insert(B)
print()
print('Printing m: ', end = '   '), m.Print()
print()
print('Testing Merge(). Comparisons made will be printed.')
print()
l.Merge(m)
print()
print('Printing new merged list: ', end = ' ')
l.Print()
print('Testing IndexOf(). Using ', a[9], ' as the element being searched for. Got: ', l.IndexOf(a[9]), ' as index.')
print()
print('Testing HasDuplicates(). Got: ', l.HasDuplicates())
print()
i = random.randint(0, 39)
print('Testing Select(), searching for ', i, '(th)(st)(nd)(rd) smallest element. Got: ', l.Select(i))
l.Print()
print()
print('Testing Delete(). Deleting ', a[10], a[1], b[19],'.' )
l.Delete(a[10]), l.Delete(a[1]), l.Delete(b[19])
l.Print()
print('Testing Min().', l.Min())
print('Testing Max().', l.Max())
print('Testing Clear().')
l.Clear()
print()
l.Print()
print()
print()
print('Creating a list that has no duplicates to test HasDuplicates for a False response')
print()
u = SortedList()
for T in range(40):
    u.Insert(T)
print('Printing new SortedList().'), u.Print()
print()
print('Testing HasDuplicates. Expecting False. Received: ', u.HasDuplicates())
print()
print('*****Testing List() Functions*****')
print()
l = List()
print('Testing Insert(). Inserting elements of a random native python list into a regular list using insert() function.')
print()
for A in a:
    l.Insert(A)
print()
print('Printing the list: ', end = ' '), l.Print()
print()
print("Creating a list m to test Merge() with.")
print()
m = List()
for B in b:
    m.Insert(B)
print()
print('Printing m: ', end = '   '), m.Print()
print()
print('Testing Merge(). Comparisons made will be printed.')
print()
l.Merge(m)
print()
print('Printing new merged list: ', end = ' ')
l.Print()
print('Testing IndexOf(). Using ', a[9], ' as the element being searched for. Got: ', l.IndexOf(a[9]), ' as index.')
print()
print('Testing HasDuplicates(). Got: ', l.HasDuplicates())
print()
print('Testing Select():')
print()
q =  l.Select(i)
print('Searching for the ', i, '(th)(nd)(rd)(st) smallest element. Got: ')
print(q)
print()
print('Testing Delete(). Deleting ', a[10], a[1], b[19],'.' )
l.Delete(a[10]), l.Delete(a[1]), l.Delete(b[19])
l.Print()
print('Testing Min().', l.Min())
print('Testing Max().', l.Max())
print('Testing Clear().')
l.Clear()
print()
l.Print()
print()
print()
print('Creating a list that has no duplicates to test HasDuplicates for a False response')
print()
u = List()
for T in range(40):
    u.Insert(T)
print('Printing new List().', u.Print())
print('Testing HasDuplicates. Expecting False. Received: ', u.HasDuplicates())
    
    



