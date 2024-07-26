import pdb
orig_list=[-1,0,1]

def is_consecutive (list_of_2_int):
    if list_of_2_int[0]-list_of_2_int[1]==-1:
        return True
    else:
        return False
    
i=0
final_lst=[] 
temp_lst=orig_list[i:i+2]
if is_consecutive(temp_lst):
    final_lst.append()
    temp_lst=temp_lst+orig_list[i:i+2]
    pdb.set_trace()


print (is_consecutive(temp_lst))
