
import numpy as np

def determinant(matrix):
    return round(np.linalg.det(matrix))
    

m1 = [[4, 6], [3,8]]
m5 = [[2,4,2],[3,1,1],[1,2,0]]

print(determinant([[5]]))#, 5, "print(determinant of a 1 x 1 matrix yields the value of the one element")
print(determinant(m1))#, 14, "Should return 4*8 - 3*6, i.e. 14")
print(determinant(m5))#, 10, "Should return the determinant of [[2,4,2],[3,1,1],[1,2,0]], i.e. 10")


