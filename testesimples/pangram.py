import string

def ispangram(str1, alphabet=string.ascii_lowercase):
    alphabet_set = set()
    input_string_set = set()
    i=0
    for a in alphabet:
        alphabet_set.add (alphabet[i])
        i+=1
    k=0
    str2=str1.lower()
    for letter in str2:
        if str2[k]==' ':
            #print (f"k={k} and space found")
            k+=1
        else:
            input_string_set.add (str2[k])
            #print (f"k={k} and new set is {input_string_set}")
            k+=1
    #print (input_string_set)
    #print (alphabet_set)
    if input_string_set==alphabet_set:
        print ("is pangram")
    else: 
        print ("is not pangram")

ispangram("The Quick brown fox Jumps over the lazy dog")