'''
Write a function, persistence, that takes in a positive parameter num and returns its multiplicative persistence, 
which is the number of times you must multiply the digits in num until you reach a single digit.

For example (Input --> Output):

39 --> 3 (because 3*9 = 27, 2*7 = 14, 1*4 = 4 and 4 has only one digit)
999 --> 4 (because 9*9*9 = 729, 7*2*9 = 126, 1*2*6 = 12, and finally 1*2 = 2)
4 --> 0 (because 4 is already a one-digit number)
'''

def persistence(n):
    def product(any_list):
        product=1
        for num in any_list:
            product=product*int(num)
        return product
    current_list=list(str(n)) 
    if (len(current_list))==1:
        return 0
    persistence_value=0
    while len(current_list)>1:
        temp_product=product(current_list)
        current_list=list(str(temp_product)) 
        persistence_value+=1
    return persistence_value

    
print (persistence(39))