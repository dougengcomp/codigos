"count number of prime numbers up to input"
import time
def isprime (num):
    mylistuptonum = list (range(2,num+1))
    for x in mylistuptonum:
        if (num % x == 0) and not(x==num):
            #print (f"{num} mod {x} == {num % x}")
            return False
        
    return True       
    


def count_primes(num):
    mylistuptonum = list (range(2,num+1))
    numofprimes =0
    for x in mylistuptonum:
        if isprime (x):
            numofprimes+=1
    return numofprimes

start_time = time.time()
print (count_primes (100000))
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")