
import pdb

def sum_three (astr,bstr,c):
    #convert input from str to int a,b considered single digit 0-9, c will always be 0 or 1
    a=int(astr)
    b=int(bstr)
    if (a < 0 or b < 0 or c < 0):
        return None
    elif (a+b+c)<10:
        return int(0),str(a+b+c)
    elif (a+b+c)>9:
        x=(a+b+c-10)
        return int(1),str(x)
    
def pre_sum(a,b):
    if (len(a)==0) and (len(b)==0):
        return ('0','0')
    
    elif (len(a)==0) and (len(b)!=0):
        return ('0',b)
    elif (len(a)!=0) and (len(b)==0):
            return (a,'0')

    elif len(a)!=len(b):
        if len(a)>len(b):
            a_least_significant_half=a[len(a)-len(b)::]
            a_most_significant_half=a[:len(a)-len(b):]
            #pdb.set_trace()
            return a_most_significant_half, a_least_significant_half, b
        else:
            b_least_significant_half=b[len(b)-len(a)::]
            b_most_significant_half=b[:len(b)-len(a):]
            return b_most_significant_half,b_least_significant_half, a
    else:
        return (a,b)
 

def sum_strings(string_of_int_a, string_of_int_b):
    result=[]
    triplet=pre_sum(string_of_int_a,string_of_int_b)
    #pdb.set_trace()

    if len(triplet)==2: #strings have the same size
        min_length = min(len(triplet[0]), len(triplet[1]))
        #pdb.set_trace()
        result.append(sum_three(triplet[0][min_length-1], triplet[1][min_length-1],int(0))) #first iteration carry is zero, takes last char on string
        #pdb.set_trace()
        for i in range((min_length-2),-1,-1):
            #pdb.set_trace()
            result.insert(0,sum_three(triplet[0][i], triplet[1][i],result[0][0]))
        if result[0][0]==1: #if final carryover
            prefinal=f"1{''.join([t[1] for t in result])}"
        else:
            prefinal=''.join([t[1] for t in result])
        return prefinal
    else:
        min_length = min(len(triplet[1]), len(triplet[2]))
        result.append(sum_three(triplet[1][min_length-1], triplet[2][min_length-1],int(0))) #first iteration carry is zero, takes last char on string
        #pdb.set_trace()
        for i in range((min_length-2),-1,-1):
            #pdb.set_trace()
            result.insert(0,sum_three(triplet[1][i], triplet[2][i],result[0][0]))
        if result[0][0]==1: #if final carryover
            pre_prefinal=f"1{''.join([t[1] for t in result])}"
            #pdb.set_trace()
            return sum_strings (f"{triplet[0]}{min_length*'0'}",pre_prefinal)
        else:
            #pdb.set_trace()
            prefinal=f"{triplet[0]+''.join([t[1] for t in result])}"
            return prefinal

#print (sum_three(9,1,0))
print (sum_strings("", ""))

    


    