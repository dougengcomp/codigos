"challenging probs"

def spy_game(nums):
    temp_list=nums
    threelevels = [False,False]
    i=0
    for x in temp_list:
        if x==0 and i < 2:
            threelevels[i]=True
            i+=1
        elif (threelevels[0] and threelevels[1] and x==7):
            return True    
        else:
            pass
    return False

print(spy_game([1,0,7,2,0,4,5,0,6,7]))
