def unique_list(lst):
    for a in lst:
        try:
            while (lst.index(a) > -1):
                firstindex=lst.index(a)
                print (lst[firstindex+1::])
                for b in lst[firstindex+1::]:
                    try:
                        secondlist = lst[firstindex+1::]
                        secondindex=secondlist.index(b)
                        while (secondlist.index(b) > -1):
                            print (secondlist)
                            secondlist.pop(secondindex)
                    except ValueError:
                        pass
                
        except ValueError:
            pass
    print (lst)
unique_list([1,1,1,1,2,2,3,3,3,3,4,5])

