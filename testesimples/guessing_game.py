from random import randint
ballot = randint (1,100)
right_choice = False
tries=int (0)
old_distance=0
print (f"original ballot :{ballot} ")
while not right_choice:
    guess = int (input ("What is your guess from 1 to 100?"))
    tries += 1
    new_distance = int (abs (ballot-guess))
    if guess==ballot:
        print (f"Congrats!! You're guess is {guess} and the ballot was {ballot}. Number of Tries was {tries}")
        right_choice=True
    elif not (101 > guess > 0):
        print ("OUT OF BONDS")
    elif (tries == 1):
        if ( (abs (ballot - guess)) <= 10):
            print ("WARM")
            old_distance=new_distance
        else:
            print ("COLD")
            old_distance=new_distance
    elif (tries >1):
        if (old_distance < new_distance):
            print (f"COLDER!, olddist={old_distance} newdist= {new_distance}")
            old_distance=new_distance
        else:
            print (f"WARMER!, olddist={old_distance} newdist= {new_distance}")
            old_distance=new_distance




