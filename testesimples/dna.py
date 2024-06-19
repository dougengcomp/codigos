'''Deoxyribonucleic acid (DNA) is a chemical found in the nucleus of cells and carries the "instructions" for the development and functioning of living organisms.

If you want to know more: http://en.wikipedia.org/wiki/DNA

In DNA strings, symbols "A" and "T" are complements of each other, as "C" and "G". Your function receives one side of the DNA (string, except for Haskell); you need to return the other complementary side. DNA strand is never empty or there is no DNA at all (again, except for Haskell).

More similar exercise are found here: http://rosalind.info/problems/list-view/ (source)

Example: (input --> output)

"ATTGC" --> "TAACG"
"GTAT" --> "CATA"'''



def DNA_strand(dna):
    char_list = [char for char in dna]
    i=0
    for char in char_list:
        if char=='A':#A vira T
            char_list[i]='T'
            #print (f"i={i} A vira T charlist =",char_list)
            i+=1
            continue
        elif char=='C':#C vira G
            char_list[i]='G'
            #print (f"i={i} C vira G charlist =",char_list)
            i+=1
            continue
        elif char=='T':#T vira A
            char_list[i]='A'
            #print (f"i={i} T vira A charlist =",char_list)
            i+=1
            continue
        elif char=='G':#G vira C
            char_list[i]='C'
            #print (f"i={i} G vira C charlist =",char_list)
            i+=1
            continue
        else:
            #print (f"i={i} nada charlist =",char_list)
            i+=1
            continue
    single_string=''.join(char_list)
    return single_string
    


print (DNA_strand("ATTGC"))