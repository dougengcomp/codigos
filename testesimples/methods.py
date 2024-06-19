mylist = [1,2,3,4,5,6,7,8,9]
work_hours = [('Abby',100),('Billy',400),('Cassie',800), ('Chanchad',2000)]

def check_even_list (arg):
    '''
    checks if any number in a list is even
    '''
    print (arg)
    for temp in arg:
        print (temp)
        if (temp % 2 == 0):
            print ("there´s an even object in the list")
            return True
    print ("only odd in the list")  
    return False 

def return_even_numbers (arg):
    my_even_list=[]
    for item in arg:
        if item % 2 == 0:
            my_even_list.append (item)
        else:
            pass
    return my_even_list

def employee_check(arg):
    max_hours=0
    best_employee=[]
    for employee, hours in arg:
        if hours > max_hours:
            max_hours=hours
            best_employee=employee
        else:
            pass
    return best_employee,max_hours

def lesser_of_two_evens(a,b):
    if (a % 2 ==0)and (b % 2 ==0):
        if (a > b):
            return b
        else:
            return a
    if (a % 2 ==1) or (b % 2 ==1):
        if (a < b):
            return b
        else:
            return a


def animal_crackers(text):
    list_of_words = text.split ()
    if (list_of_words[0][0]==list_of_words[1][0]):
        return True
    else:
        return False

def makes_twenty(n1,n2):
    if (n1+n2==20) or (n1==20) or (n2==20):
        return True
    else:
        return False

def old_macdonald(name):
    mylist = list(name)
    mylist[0]= chr(ord(mylist[0]) - 32)
    mylist[3]= chr(ord(mylist[3]) - 32)
    temp_string=''
    temp_string2 = temp_string.join(mylist)
    return temp_string2

def master_yoda(text):
    list_of_words = text.split ()
    i=len (list_of_words)
    reverse_list=[]
    for word in list_of_words:
        last_word =list_of_words[i-1]
        reverse_list.append (last_word)
        i-=1
        if i == 0:
            reverse_string = " ".join(reverse_list)
            return reverse_string


def almost_there(n):
    if (abs (100-n) < 11) or (abs (200-n) < 11):
        return True
    else:
        return False
    
def has_33(nums):
    i=0
    for item in nums:
        if ((i+1)< len (nums)) and (nums[i+1]==item) and (item==3):
            i+=1
            return True
        else:
            if (i+1)< len (nums):
                i+=1
            else:
                return False

def paper_doll(text):
    mylist = list(text)
    i=0
    for letter in mylist:
        mylist[i]=3*mylist[i]
        i+=1
    string = "".join(mylist)
    return string

def blackjack(a,b,c):
    if ((a+b+c) < 22):
        return (a+b+c)
    elif ((a+b+c) > 21) and ((a==11)or (b==11)or (c==11))and ((a+b+c-10)<22) :
        return (a+b+c-10)
    elif ((a+b+c) > 21) and ((a==11)or (b==11)or (c==11))and ((a+b+c-10)>21) :
        return "BUST"
    else:
        return "BUST"

def sublist (letter,lst):
    '''
    finds a letter on a list and returns a sublist after the letter (and including) the letter found 
    '''
    i=0
    sublist_tmp=[]
    for a in lst:
        if a == letter:
            sublist_tmp.append (lst[i::])
            return sublist_tmp[0]
        else:
            i+=1
    return None

def extract_69s (lst):
    i=0
    temp_list=[]
    temp_list_1st_half=[]
    temp_list_2nd_half=[]
    for num in lst:
        temp_list_1st_half.append (num)
        if num==6:
            temp_list=sublist (num,lst)
            for a in temp_list:
                temp_list_2nd_half.append(a)
                if a == 9:
                    temp_list_2nd_half = sublist (a,temp_list)
                    temp_list_2nd_half.remove(a)

            print (temp_list)
    pass
#extract_69s ([1,2,3,4,5,6,7,8,9])

def summer_69(arr):
    temp_list=arr
    temp_list_1st_half=[]
    temp_list_2nd_half=[]
    i=0
    print (temp_list.index (6),temp_list.index (9))
    try: 
        while ((temp_list.index (6)<temp_list.index (9))): 
                print (f"caiu no while round {i}")
                temp_list_1st_half = temp_list[:temp_list.index (6):]
                temp_list_2nd_half = temp_list[temp_list.index (9)+1::]
                temp_list=temp_list_1st_half+temp_list_2nd_half
                print (f"temp_list_full_without69 is now : {temp_list}")
                i+=1
    except ValueError:
                print ("caiu na execao")
                return sum (temp_list)
    return sum (temp_list)

print (summer_69([9,6,9]))
#nok print (summer_69([1,2,3,4,5,9,7,8,6,9,10]))
#ok print (summer_69([6,9]))
#ok print (summer_69([1,2,3,4,5,6,7,8,9,10]))
#ok print (summer_69([1,2,3,4,5,9,7,8,6,10]))
#ok print (summer_69([6,2,3,4,5,6,7,8,9,9]))
#ok print (summer_69([6,6,6,9,6,9,9,9]))
#ok print (summer_69([6,9,6,1,2,3,9,6,7,8,9]))
#ok print (summer_69([6,9,6,9,6,9]))


    

    