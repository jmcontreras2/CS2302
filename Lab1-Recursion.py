#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 1 - Recursion
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 9/6/2019

#Purpose of Program: The purpose of this program is to take a user's inputted word
#and find anagrams for that word found in a .txt file containing over 466,000 words.


#NOTE: Part 1, 2.1, and 2.2 are separated through comments. They each have their own
# else branch. Uncomment from here until end of block to use. Comment parts that are not being tested.

import time #We use the time library to calculate time taken for the anagram finding functions to run.


#This function takes a set of permutations and checks if they're in the set of words.
#This is done so that the big set of words isn't passed every recursive call.

#It is used throughout the file so I placed it at the top.
def checkInSetOfWords(permutationList, setOfWords):
    AnagramsList = []
    for p in permutationList:
        if p in setOfWords:
            AnagramsList += [p]
    return AnagramsList

###############################################################################
#######################   Part 1 Functions      ###############################
###############################################################################

#### This is my permutation finding function, permuttionFinder.
def permutationFinder(unchosenCharacters, chosenCharacters, userWord):
    ###Base Case: When unchosenCharacters's length is 0, the particular permutation being formed is completed.
    # Here, we check that this permutation is in the set of words from the .txt file and that it is not the
    # original word inputted. If these conditions check out, then we return the word to add to the list of anagrams.
    # Else, we return an empty list to not negatively affect the anagrams list.
    if len(unchosenCharacters) == 0:
        if chosenCharacters != userWord:
            return [chosenCharacters]
        else:
            return []
    else:
        ### Recursive Case: The recursive case starts at the first character, then recursively creates all the
        # possible permutations of its characters. We choose a letter for the permutation and then recursively
        #combine it with the remaining letters according to the unexplored permutations that remain.
        permutations = []
        for i in range(len(unchosenCharacters)):
            chosenLettertoPass =unchosenCharacters[i]
            unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
            permutations += (permutationFinder(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord))
        ### We return the final list of permutations when permutationsFinder is finished.
        return permutations
    
###############################################################################
#######################   Part 2 Functions      ###############################
###############################################################################  

###############################################################################
################  Part 2 Functions for First Optimization  ####################
############################################################################### 

#permutations2p1 implements the first optimization by checking that the letters we are going to
#pass aren't in the partial permutation that is being created so the same permutation isn't created
#multiple times.
def permutations2p1(unchosenCharacters, chosenCharacters, userWord):
    if len(unchosenCharacters) == 0:
        if chosenCharacters != userWord:
            return [chosenCharacters]
        else:
            return []
    else:
        # The recursive case happens only if the character that is going to be passed to continue the permutation is not already
        # in the permutation in process.
        permutations = []
        for i in range(len(unchosenCharacters)):
            chosenLettertoPass =unchosenCharacters[i]
            if chosenLettertoPass in chosenCharacters:
                pass
            else:
                unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
                permutations += (permutations2p1(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord))
        ### We return the final list of anagrams when anagramFinder is finished.
    return permutations

###############################################################################
################  Part 2 Functions for Second Optimization  ###################
############################################################################### 

#The function setPrefix uses a helper function stringCombinations to create the actual prefixes, then stores them in a set to make sure none are repeating.
def setPrefix(userSet):
    setofPrefixes = set()
    for a in userSet:
        setofPrefixes.update(stringCombinations(a, 0))
    return setofPrefixes

#The helper function stringCombinations creates all the prefixes of a word recursively and returns a list of prefixes.
def stringCombinations(userString, i):
    if i == len(userString)-1:
        return ''
    else:
        stringList = []
        stringList += userString[0], userString[:i + 1]

        print
        stringList += stringCombinations(userString, i + 1)
    finalPrefixSet = set(stringList)
    return finalPrefixSet

#Permutations2p2 implements the second optimization by checking if the the partial permutation being created
#is in the prefix set.
def permutations2p2(unchosenCharacters, chosenCharacters, userWord, prefixSet):
    if len(unchosenCharacters) == 0:
        if chosenCharacters != userWord:
            return [chosenCharacters]
        else:
            return []
    else:
        ## The recursive case only happens when the permutation in process is length 0 (which means it hasn't started the process)
        # or the letter we chose for the next permutation pass is already in the permutation in process.
        permutations = []
        for i in range(len(unchosenCharacters)):
            chosenLettertoPass =unchosenCharacters[i]
            if len(chosenCharacters) == 0:
                unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
                permutations += (permutations2p2(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord, prefixSet))
            elif chosenCharacters in prefixSet:
                unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
                permutations += (permutations2p2(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord, prefixSet))
            else:
                return []
        ### We return the final list of anagrams when permutations2p2 is finished.
        return permutations


###############################################################################
##########  Anagram Finder Function with both Optimizations ###################
############################################################################### 

### Permutations2 implements both optimizations found in permutations2p1 and permutations 2p2
def permutations2(unchosenCharacters, chosenCharacters, userWord, prefixSet):
    if len(unchosenCharacters) == 0:
        if chosenCharacters != userWord:
            return [chosenCharacters]
        else:
            return []
    else:
        permutations = []
        for i in range(len(unchosenCharacters)):
            chosenLettertoPass =unchosenCharacters[i]
            if chosenLettertoPass in chosenCharacters:
                pass
            if len(chosenCharacters) == 0:
                unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
                permutations += (permutations2(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord, prefixSet))
            elif chosenLettertoPass in chosenCharacters:
                pass
            elif chosenCharacters in prefixSet:
                unchosenLetterstoPass = unchosenCharacters[:i] + unchosenCharacters[i + 1:]
                permutations += (permutations2(unchosenLetterstoPass, chosenCharacters + chosenLettertoPass, userWord, prefixSet))
            else:
                return []
        ### We return the final list of permutatoins when permutations2 is finished.
        return permutations
    
###############################################################################
##########  An Anagram Finder Algorithm I came up with      ###################
############################################################################### 
    
#The anagramCollector takes the user inputted word as well as set of words from the .txt file and starts a loop.
#The anagramCollector loops through the words in the set of words given, and for each word, recursively checks if that
#word is an anagram of the user inputted word by passing the user inputted word and word from set of words to the 
#anagram checker. If it is an anagram, it adds it to the list of anagrams then returns that list.
def anagramCollector(userWord, wordsSet):
    anagrams = []
    for i in wordsSet:
        if userWord == i:
            pass
        else:
            anagramCheck = anagramChecker(userWord, i)
            if anagramCheck:
                anagrams += [i]
    return anagrams

#The anagramChecker implements the first optimization by only generating the anagrams that are necessary when checking the
#the words for anagrams. It first checks to see if the length of the user inputted word and the length of the word from the
#set of words is the same. If the lengths are not the same, then anagramChecker returns False. If they are the same, 
#anagramChecker checks to see if the first word in the user inputted word is contained in the second word. If it's not, it
#returns false. If it is, then anagramChecker passes the user inputted word minus the matched character as well as the word
#from the set of words minus the matched character. This way, we check to see that the two words have the same length
#and the exact same characters. This means we don't create n! permutations while performing this task.
def anagramChecker(userWord, word):
    if len(userWord) != len(word):
        return False
    elif len(userWord) == 0:
        return True
    else:
        for i in range(len(word)):
            if userWord[0] == word[i]:
                return anagramChecker(userWord[1:], word[:i] + word[i+1:])
        return False 
  
    
    
    
    
    
    
    
    ###########################################################################
    ###########                  Beginning of Program                ##########
    ###########################################################################
        
words = set(open('words_alpha.txt').read().split())  #This variable reads in the words from the .txt file and stores them in a set.
prefixSet = setPrefix(words) #This variable creates a set of prefixes from the words in the txt file.
programQuit = 0 #This variable is used to check if the user wants to keep finding anagrams or quit the program.
while programQuit != 1: #This while loops is used to check if the user wants to keep finding anagrams or quit the program.
    userWord = input("Welcome to my Anagram Finder. Enter a word to find anagrams for that word, or enter an empty string to quit the program. ")
    if len(userWord) == 0: #If the length of the string is empty, we quit the program.
        print("Thank you for using my Angram program. Have a good day.")
        programQuit = 1
        
        
        
    ###########################################################################
    ###########                        PART 1 Test                   ##########
    ###########################################################################        
   
    else:
        startTime = time.time()    #This variable takes a measure of the time before the anagram finding function is started.
        userWordPermutations = permutationFinder(userWord, '', userWord) #This variable calls the anagram finding function and stores the list of anagrams.
        userWordAnagrams = checkInSetOfWords(userWordPermutations, words)
        endTime = time.time()      #This variable takes a measure of the time after the anagram finding function is finished.
        userWordAnagrams = sorted(set(userWordAnagrams)) #We store the anagrams list in a set to remove duplicates then sort them alphabetically.
        totalTime = endTime - startTime    #This variable takes the difference of the ending and beginning times of the function to calculate total time taken to find anagrams.
        print("It took approximately ", round(totalTime, 6), "to find the following ", len(userWordAnagrams), " anagrams.")
        for i in userWordAnagrams: #We print the anagrams in the anagram list.
            print(i)
    
    ###########################################################################
    ###########     PART 2 Test w/ only first optimization           ##########
    ###########################################################################
#    else:
#        start = time.time()
#        userWordPermutations2p1 = permutations2p1(userWord, '', userWord)
#        userWordAnagrams2p1 = checkInSetOfWords(userWordPermutations2p1, words)
#        end = time.time()
#        userWordAnagrams2p1Set = sorted(set(userWordAnagrams2p1))
#        print('It took approximately ', (end-start), ' to find the following', len(userWordAnagrams2p1Set), ' anagrams.')
#        for u in userWordAnagrams2p1Set:
#            print(u)

    
    ###########################################################################
    ###########       PART 2 Test w/ only second optimization        ##########
    ###########################################################################          
    
#    else:
#       start = time.time()
#       userWordPermutations2p2 = permutations2p2(userWord, '', userWord, prefixSet)
#       userWordAnagrams2p2 = checkInSetOfWords(userWordPermutations2p2, words)
#       end = time.time()
#       userWordAnagrams2p2Set = sorted(set(userWordAnagrams2p2))
#       print('It took approximately ', (end-start), ' to find the following', len(userWordAnagrams2p2Set), ' anagrams.')
#       for u in userWordAnagrams2p2Set:
#           print(u)
            
    ###########################################################################
    ###########          PART 2 Test w/ both optimizations         ############
    ###########################################################################  

#    else:
#       start = time.time()
#       userWordPermutations2 = permutations2(userWord, '', userWord, prefixSet)
#       userWordAnagrams2 = checkInSetOfWords(userWordPermutations2, words)
#       end = time.time()
#       userWordAnagrams2Set = sorted(set(userWordAnagrams2))
#       print('It took approximately ', (end-start), ' to find the following', len(userWordAnagrams2Set), ' anagrams.')
#       for u in userWordAnagrams2Set:
#           print(u)        
    
    
    
    ###########################################################################
    ###########                  MISC. Algorithm I designed          ##########
    ###########################################################################
    
    ###While trying to come up with the recursive functions for this lab, I stumbled
    ###upon the idea that we could just compare the length of the user inputted word
    ###to the word in the txt file, as well as check to see if the letters are in the
    ###word from the .txt file. This circumvents creating n! permutations. 
    ###This algorithm performs better than the one in part one but does not 
    ###outperform the algorithm with the two optimizations.
    
#    else:
#        start = time.time()
#        userWordAnagramsMISC = anagramCollector(userWord, words)
#        end = time.time()
#        userWordAnagramsMISCSet = sorted(set(userWordAnagramsMISC))
#        print('It took approximately ', (end-start), ' to find the following', len(userWordAnagramsMISCSet), ' anagrams.')
#        for u in userWordAnagramsMISCSet:
#            print(u)