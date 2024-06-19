
def array_diff(a, b):
    clean_list=a
    for search in b:
        clean_list = [item for item in clean_list if item != search]
    return clean_list


a=[1,2,2,2,3,3,4]
b=[1,2,3]
print (array_diff(a,b))