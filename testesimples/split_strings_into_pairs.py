'''Complete the solution so that it splits the string into pairs of two characters. 
If the string contains an odd number of characters then it should 
replace the missing second character of the final pair with an underscore ('_').

Examples:

* 'abc' =>  ['ab', 'c_']
* 'abcdef' => ['ab', 'cd', 'ef'] '''

import re

def solution(s):
    my_list=list(s)
    final_list=[]
    while (len(my_list)>0):
        char1=my_list.pop(0)
        if len(my_list)>0:
            char2=my_list.pop(0)
            final_list.append(str(char1+char2))
        else:
            char2='_'
            final_list.append(str(char1+char2))
    return final_list

print (solution('abcdefg'))