import re
'''
Write a function that takes in a string of one or more words, and returns the same string, 
but with all words that have five or more letters reversed (Just like the name of this Kata).
Strings passed in will consist of only letters and spaces. 
Spaces will be included only when more than one word is present.
'''

def spin_words(sentence):
    def reverse_word(a):
        return str (a[::-1])

    pattern=r'\w{5,}'
    mylistofwords=sentence.split()
    i=0
    for word in mylistofwords:
        if re.search(pattern,word) != None:
            mylistofwords[i]=reverse_word(word)
        i+=1
        final_string=' '.join (mylistofwords,)
    return final_string

print (spin_words("ABCDE fghij klmnopq"))