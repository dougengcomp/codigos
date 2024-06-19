from random import randint
ballot = randint (1,100)
guess = int (input ("What is your guess from 1 to 100?"))
right_choice = False
tries=int (0)

while not right_choice:
    tries += 1
    if guess==ballot:
        print (f"Congrats!! You're guess is {guess} and the ballot was {ballot}. Number of Tries was {tries}")
        right_choice=True
    elif not (100 > guess > 1):
        print ("OUT OF BONDS")
    elif ( (abs (ballot - guess)) <= 10):
        print ("WARM")
    else:
        print ("COLD")



print ("original ballot and guess were: ",ballot,guess)