def ask ():
    while True:
        
        try:
            a=int (input ("please provide an integer:"))
            print (f"the square of {a} is: {a**2}")
            break
        except:
            print ("invalid input")

ask ()
    