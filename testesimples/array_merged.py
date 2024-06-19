def summer_69(arr):
    total = 0
    add = True
    for num in arr:
        while add:
            if num != 6:
                total += num
                print (f"while add num is {num} total is {total} then break")
                break
            else:
                print (f"num is 6 so add set to false, total is {total}")
                add = False
        while not add:
            if num != 9:
                print (f"while not add num is {num} which is diff than 9 so break")
                break
            else:
                print (f"while not add num is {num} so add set to true")
                add = True
                break
    return total


print (summer_69([9,6,6,9]))
