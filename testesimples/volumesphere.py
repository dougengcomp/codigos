import math
def volumeofsphere (r=0):
    return (4/3)*(math.pi)*(r)**3

#print (volumeofsphere (2))

def ran_check(num,low,high):
    return (low-1)<num<(high+1)

#print (ran_check(0,1,3))

def up_low(s:str):
    upper=0
    lower=0
    spaces=0
    print (f"Original String: {s}")
    for letter in s:
        if letter.isupper():
            upper +=1
        elif letter == " " :
            spaces +=1      
        elif letter.islower():
            lower +=1
    print (f"No. of Upper case characters: {upper}") 
    print (f"No. of Lower case Characters: {lower}")
    print (f"No. of space Characters: {spaces}")

#s = 'Hello Mr. Rogers, how are you this fine Tuesday?'
#up_low(s)

def unique_list(lst):
    uniquelst=[]
    for a in lst:
        try:
            if  (uniquelst.index(a) >-1):
                pass                
        except:
            uniquelst.append(a)
    print (uniquelst)

#unique_list([1,1,1,1,2,2,3,3,3,3,4,5])

def multiply(numbers):
    result=1
    for a in numbers:
        result=result*a 
    return result
#print (multiply([0,1,2,3,-4]))

def palindrome(s:str):
    my_string_without_spaces = s.replace(" ", "")
    reversed_string = my_string_without_spaces[::-1]
    print (reversed_string)
    if my_string_without_spaces==reversed_string :
        print ("is palindrome")
    else:
        print ("is not pal")
palindrome ("nurses run")