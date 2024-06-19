
'''
ROT13 is a simple letter substitution cipher that replaces a letter with the letter 13 letters after it in the alphabet. ROT13 is an example of the Caesar cipher.

Create a function that takes a string and returns the string ciphered with Rot13. If there are numbers or special characters included in the string, they should be returned as they are. Only letters from the latin/english alphabet should be shifted, like in the original Rot13 "implementation".

Please note that using encode is considered cheating.
'''

#result = ['even' if num % 2 == 0 else 'odd multiples of 3' if num % 3 == 0 else 'other' for num in nums]



def rot13(message):
    ciphered=[char if not ((91 > ord(char) > 64) or (123 > ord(char) > 96)) else chr((ord(char)+13)) if ((78 > ord(char) > 64) or (110 > ord(char) > 96)) else chr((ord(char)-13)) for char in list(message)]
    return ''.join(ciphered)

#print (ord('a'))
print (rot13 ('abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ!@#$%¨&*;.,><|:+-/'))
#rot13('aA bB zZ 1234 *!?%') ==>'nN oO mM 1234 *!?%'
