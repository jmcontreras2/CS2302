#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 2 - Sorting
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 9/20/2019

#Purpose of Program: This program takes a list, sorts it, then returns the kth element 
#in the list through various methods. It can do this through bubblesort, quicksort, 
#various modified versions of quicksort that are recursive and iterative. 



########## NOTE ABOUT HOW TO USE THIS PROGRAM  ################################

## I've implemented a very crude user interface.

## In order to use the program, please run as-is and follow on-screen instructions.
# The user will be prompted with the following choices to enter (the user is to enter the integer):

# 1: Tests select_bubble()'s accuracy and time.
# 2: Tests select_quick()'s accuracy and time.
# 3: Tests select_modified_quick()'s accuracy and time.
# 4: Tests select_quick_S()'s accuracy and time.
# 5: Tests select_modified_quick_W()'s accuracy and time.

import random
import time
import sys
sys.setrecursionlimit(5000)
###############################################################################
####################       Part 1 Functions       #############################
###############################################################################

#select_bubble takes a list, sorts it recursively using bubble sort, then returns the kth element in the list.
def select_bubble(L, k):
    bubblesort(L)
    return L[k]

#A recursive implementation of the sorting algorithm bubblesort.
def bubblesort(L):
    flag = True
    while flag:
        flag = False
        for i in range(len(L) - 1):
            if L[i] > L[i + 1]:
                temp = L[i]
                L[i] = L[i + 1]
                L[i + 1] = temp
                flag = True
            

#select_quick takes a list, recursively sorts it using quicksort, then returns the kth element in the list.
def select_quick(L, k):
    quicksort(L, 0, len(L)-1)
    return L[k]

#A recursive implementation of the sorting algorithm quicksort. The if statement makes a bounds check to make sure
#that the recursive call is calling on the list in a way that makes sense. 
# Quicksort partitions the list to a left side that is less than a pivot and a right side that is greater than the pivot.
#It does this with the partition function and when partition is finished, it returns the index of where the pivot is located.
#Quicksort then recursively calls quicksort using this pivotLocation to partition the list and continue sorting those partitions.
    
#The pivot is selected using a median of three because this method uses more information than a single data point like the pivot selection 
#methods of first, last, and random do. It means we have three data points and we know we are taking a value that at the very least
#sits between two values. quicksort() also places the pivot in the first slot of the list so that we know where it is and we don't iterate
#over it.

#Once partition returns the pivot index in the partially sorted list, we call quicksort on the list to the left of the pivot and on the
#list to the right of the pivot. 
def quicksort(L, left, right):
  if left < right:
    pivotIndex = median_of_three(L, left, right)
    pivot = L[pivotIndex]
    if pivotIndex != left:
        temp = L[left]
        L[left] = pivot
        L[pivotIndex] = temp
    pivotLocation = partition(L, left, right, pivot)
    quicksort(L, left, pivotLocation - 1)
    quicksort(L, pivotLocation + 1, right)
 
#Median of three takes a list and the left and right bounds. It uses this information to calculate a first, mid, and last value.
#It then compares these three values to see which one is the median. It then returns this as the pivot.
def median_of_three(L, left, right):
  mid = (left + right) // 2
  pivot = left
  if L[left] < L[mid]:
    if L[mid < L[right]]:
      pivot = mid
  elif L[left] < L[right]:
    pivot = left
  return pivot

#Partition takes a list, the index of a list's left bound, the index of a list's right bound, and a pivot.
#Partition then uses this information to put elements less than the pivot to the left part of the list and 
#elements greater than the pivot to the right part of the list. It finishes by putting the pivot in its appropriate
#place relative to the rest of the elements. 

#I use the left bound to iterate through the list and as it does, puts values less than the pivot in the left position, then moves
#that pointer a space forward. This ensures that when the iteration is finished, the index that pivotFinal is in, is the appropriate index
#for the pivot.
#then returns the index of that pivot.
def partition(L, left, right, pivot):
  pivotFinal = left
  for i in range(left, right + 1):
    if L[i] < pivot:
      pivotFinal += 1
      temp = L[i]
      L[i] = L[pivotFinal]
      L[pivotFinal] = temp
  temp = L[left]
  L[left] = L[pivotFinal]
  L[pivotFinal] = temp
  return pivotFinal
     
#select_modified_quick calls a modified quicksort function that only sorts the part of the list that contains the kth element, and returns
#the kth element.
def select_modified_quick(L, k):
    modified_quicksort(L, 0, len(L)-1, k)
    return L[k]

#modified_quicksort compares k to the pivot, and if k is equal to the pivot, returns L[pivotIndex],
#if k is less than the pivot, the modified quicksort sorts the list to the left of the pivot, if k is greater than the pivot,
#the modified quicksort sorts the list to the right of the pivot.
def modified_quicksort(L, left, right, k):
  if left < right:
    pivotIndex = median_of_three(L, left, right)
    pivot = L[pivotIndex]
    if pivotIndex != left:
        temp = L[left]
        L[left] = pivot
        L[pivotIndex] = temp
    pivotIndex = partition(L, left, right, pivot)
    if k == pivotIndex:
        return pivot
    elif k < pivotIndex:
      modified_quicksort(L, left, pivotIndex - 1, k)
    else:
      modified_quicksort(L, pivotIndex + 1, right, k)

###############################################################################
####################       Part 2 Functions       #############################
###############################################################################
      
def select_quick_S(L, k):
    quicksort_S(L, 0, len(L) - 1)
    return L[k]

def quicksort_S(L, left, right):    
    stack = []
    stack.append(left)
    stack.append(right)
    while len(stack) > 0:
        rightbound = stack.pop(-1)
        leftbound = stack.pop(-1)
        if rightbound - leftbound < 0:
            continue
        pivotIndex = median_of_three(L, leftbound, rightbound)
        pivot = L[pivotIndex]
        if pivotIndex != leftbound:
            temp = L[leftbound]
            L[leftbound] = pivot
            L[pivotIndex] = temp
        pivot = L[leftbound]
        pivotLocation = partition(L, leftbound, rightbound, pivot)
        stack.append(leftbound)
        stack.append(pivotLocation - 1)
        stack.append(pivotLocation + 1)
        stack.append(rightbound)

def select_modified_quick_W(L, k):
    modified_quicksort_W(L, 0, len(L) -1, k)
    return L[k]

def modified_quicksort_W(L, left, right, k):
    while left < right:
        pivotIndex = median_of_three(L, left, right)
        pivot = L[pivotIndex]
        if pivotIndex != left:
            temp = L[left]
            L[left] = pivot
            L[pivotIndex] = temp
        pivotIndex = partition(L, left, right, pivot)
        if k == pivotIndex:
            return L[pivotIndex]
        elif k < pivotIndex:
            right = pivotIndex - 1
        else:
            left = pivotIndex + 1

###############################################################################
################## Functions created for Testing  #############################
###############################################################################
    
def isSorted(L):
    for i in range(len(L)-1):
        if L[i] > L[i + 1]:
            return False
        return True

#this function generates a random list of length n.
def generate_random_L(n):
    L = []
    for j in range(n):
        L += [random.randint(-20, 20)]
    return L

#this functoin generates a random k that's between o and the last index of L.
def generate_random_k(L):
    k = random.randint(0, len(L)-1)
    return k
 
# this function runs a test on accuracy for select_bubble.         
def test_select_bubble_accuracy(L, k):
    print()
    print('Testing select_bubble\'s accuracy.')
    print()
    print('printing unsorted L: ', L)
    a = select_bubble(L, k)
    print('printing k: ', k)
    print('printing kth element: ', a)
    print('printing sorted L: ', L)
    print('Is the list sorted?: ', isSorted(L))
    
# this function runs a test on select_bubble's time.
def test_select_bubble_time(L, k):
    print()
    print('Testing select_bubble\'s time for a list of ', len(L), ' items.')
    start = time.time()
    select_bubble(L, k)
    end = time.time()
    print('It took select_bubble ', (end - start), ' seconds to sort a list of', len(L), ' items.')
    
# this function runs a test on accuracy for select_quick.         
def test_select_quick_accuracy(L, k):
    print()
    print('Testing select_quick\'s accuracy.')
    print()
    print('printing unsorted L: ', L)
    a = select_quick(L, k)
    print('printing kth element: ', a)
    print('printing sorted L: ', L)
    print('printing k: ', k)
    print('Is the list sorted?: ', isSorted(L))
    
# this function runs a test on select_quick's time.
def test_select_quick_time(L, k):
    print()
    print('Testing select_quick\'s time for a list of ', len(L), ' items.')
    start = time.time()
    select_quick(L, k)
    end = time.time()
    print('It took select_quick ', (end - start), ' seconds to sort a list of', len(L), ' items.')
    
# this function runs a test on accuracy for select_modified_quick.         
def test_select_modified_quick_accuracy(L, k):
    print()
    print('Since this method does not fully sort the list, the kth element found by select_quick is provided for comparison.')
    print()
    print('Testing select_modified_quick\'s accuracy.')
    print()
    print('printing unsorted L: ', L)
    a = select_modified_quick(L, k)
    print('printing k: ', k)
    print('printing kth element acquired using select_modified_quick: ', a)
    print('printing kth element acquired using select_quick: ', select_quick(L, k))
    print('printing sorted L using select_quick: ', L)
    
# this function runs a test on select_modified_quick's time.
def test_select_modified_quick_time(L, k):
    print()
    print("Testing select_modified_quick\'s time for a list of ", len(L), ' items.')
    start = time.time()
    select_modified_quick(L, k)
    end = time.time()
    print('It took select_modified_quick ', (end - start), ' seconds to sort a list of', len(L), ' items.')

# this function runs a test on accuracy for select_quick_S.         
def test_select_quick_S_accuracy(L, k):
    print()
    print('Testing select_quick_S\'s accuracy.')
    print()
    print('printing unsorted L: ', L)
    a = select_quick_S(L, k)
    print('printing k: ', k)
    print('printing kth element acquired from select_modified_quick_S: ', a)
    print('printing sorted L using select_quick: ', L)
    print('Is the list sorted?: ', isSorted(L))
    
# this function runs a test on select_modified_quick_S's time.
def test_select_quick_S_time(L, k):
    print()
    print('Testing select_quick_S\'s time for a list of ', len(L), ' items.')
    start = time.time()
    select_quick_S(L, k)
    end = time.time()
    print('It took select_modified_quick ', (end - start), ' seconds to sort a list of', len(L), ' items.')

# this function runs a test on accuracy for select_quick_W.         
def test_select_modified_quick_W_accuracy(L, k):
    print()
    print('Since this method does not fully sort the list, the kth element found by select_quick is provided for comparison.')
    print()
    print('Testing select_modified_quick_W\'s accuracy.')
    print()
    print('printing unsorted L: ', L)
    a = select_modified_quick_W(L, k)
    print('printing k: ', k)
    print('printing kth element acquired from select_modified_quick_S: ', a)
    print('printing kth element acquired using select_quick: ', select_quick(L, k))
    print('printing sorted L using select_quick: ', L)
    
# this function runs a test on select_modified_quick_W's time.
def test_select_quick_W_time(L, k):
    print()
    print('Testing select_quick_W\'s time for a list of ', len(L), ' items.')
    start = time.time()
    select_modified_quick_W(L, k)
    end = time.time()
    print('It took select_modified_quick ', (end - start), ' seconds to sort a list of', len(L), ' items.')
    
    
    
    
    
###############################################################################
####################      Testing  Part 1         #############################
###############################################################################
    
#All sorting algorithms are tested for accuracy and time.

#For accuracy, we create a list filled with random numbers, both negative and positive, to
#test the sorting algorithms on. We also randomize k from a range of 0 to the 
#the last index of the list. We keep the list to a length that makes visual
#verification of the sorted nature of the list possible. We print the list to
#check it is sorted and we print the kth element to verify its accuracy.
    
#After verifying the accuracy of the sorting algorithms, we now measure the amount
#of time it takes to complete for various lengths of lists. 

#For all the sorting algorithms, we test with list sizes of: 10, 100, 1000, and 10,000.
  
next_loop = False
while not next_loop:
    a = input("Pressing 1 tests select_bubble(). Pressing 2 tests select_quick(). Pressing 3 tests select_modified_quick(). Pressing 4 tests select_quick_S() implemented with a stack. Pressing 5 tests select_modified_quick_W() implemented with a while loop only. Enter an empty string to quit: ")
####################     select_bubble(L, k):     #############################
    if (a == '1'): 
        
#Testing select_bubble's accuracy.
    
        L = generate_random_L(10)
        k = generate_random_k(L)
        test_select_bubble_accuracy(L, k)

#Testing select_bubble's time.

        sizes = [10, 100, 1000, 10000]
        
        for i in sizes:
            L = generate_random_L(i)
            k = generate_random_k(L)
            test_select_bubble_time(L, k)

####################     select_quick(L, k):     #############################
    elif (a == '2'): 

#Testing select_quick's accuracy.

        L = generate_random_L(10)
        k = generate_random_k(L)
        test_select_quick_accuracy(L, k)

#Testing select_quick's time.

        sizes = [10, 100, 1000, 10000]
        for i in sizes:
            L = generate_random_L(i)
            k = generate_random_k(L)
            test_select_quick_time(L, k)

####################     select_modified_quick(L, k):     #############################
    
    elif (a == '3'):       
#WTesting select_modified_quick's accuracy. Since select_modified_quick() does not 
#sort the full list, we use select_quick() to verify the accuracy of select_modified_quick().
    
        L = generate_random_L(10)
        k = generate_random_k(L)
        test_select_modified_quick_accuracy(L, k)

#Testing select_modified_quick's time.
    
        sizes = [10, 100, 1000, 10000]
        
        for i in sizes:
            L = generate_random_L(i)
            k = generate_random_k(L)
            test_select_modified_quick_time(L, k)
    
###############################################################################
####################      Testing  Part 2         #############################
###############################################################################

#################    select_quick_S(L, k):     ########################

    elif (a == '4'):

#select_quick_S() refers to the select quicksort function
#that implements quicksort as a stack rather than recursion.

#Testing select_quick_S's() accuracy.

        L = generate_random_L(10)
        k = generate_random_k(L)
        test_select_quick_S_accuracy(L, k)

#Testing select_quick_S's() time.

        sizes = [10, 100, 1000, 10000]
        
        for i in sizes:
            L = generate_random_L(i)
            k = generate_random_k(L)
            test_select_quick_S_time(L, k)
    
#################    select_modified_quick_W(L, k):     #######################

    elif(a == '5'):

#select_quick_W() refers to the select_modified_quick() function that was
#implemented using a while loop only.
    
#Testing select_modified_quick_W's() accuracy.
    
        L = generate_random_L(10)
        k = generate_random_k(L)
        test_select_modified_quick_W_accuracy(L, k)
    
#Testing select_modified_W's() time.

        sizes = [10, 100, 1000, 10000]
        
        for i in sizes:
            L = generate_random_L(i)
            k = generate_random_k(L)
            test_select_quick_W_time(L, k)

    else:
        next_loop = True
