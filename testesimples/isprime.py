import time
def is_prime (num):
    if num < 2:
        return False
    mylistuptonum = list (range(2,num+1))
    for x in mylistuptonum:
        if (num % x == 0) and not(x==num):
            return False
    return True       
        
start_time = time.time()
print (is_prime (1))
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")