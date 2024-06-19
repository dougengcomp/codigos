'''Given two arrays of strings a1 and a2 
return a sorted array r in lexicographical order 
of the strings of a1 which are substrings of strings of a2.

Example 1:
a1 = ["arp", "live", "strong"]

a2 = ["lively", "alive", "harp", "sharp", "armstrong"]

returns ["arp", "live", "strong"]

Example 2:
a1 = ["tarp", "mice", "bull"]

a2 = ["lively", "alive", "harp", "sharp", "armstrong"]

returns [] '''

def in_array(array1, array2):
    r=[]
    for word in array2:
        for element in array1:
            if element in word:
                r.append(element)  
    return sorted (list (set (r)))

a1 = ["arp", "live", "strong"] #element
#a1 = ["tarp", "mice", "bull"]
a2 = ["lively", "alive", "harp", "sharp", "armstrong"] #word
print (in_array(a1,a2))