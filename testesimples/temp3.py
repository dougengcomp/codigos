import math

def circleIntersection(a, b, r):
    # Calculate squared distance between centers
    d_squared = (a[0] - b[0])**2 + (a[1] - b[1])**2
    
    # Case 1: Identical circles
    if d_squared == 0 and r == 0:
        return int(r**2 * math.pi)
    
    # Calculate distance between the two circles
    d = math.sqrt(d_squared)
    
    # Case 2: Non-intersecting circles
    if d >= 2 * r:
        return 0
    
    # Case 3: One circle completely inside another
    if d <= abs(r - r):
        return int(min(r**2, ((a[0] - b[0])**2 + (a[1] - b[1])**2)) * math.pi)
    
    # Case 4: Partial intersection
    # Calculate intersection area using trigonometry
    alpha = 2 * math.acos(d / (2 * r))
    intersection_area = r**2 * (alpha - math.sin(alpha))
    
    return int(intersection_area)

# Test cases
print(circleIntersection([0, 0], [7, 0], 5))        # should return 14
print(circleIntersection([0, 0], [0, 10], 10))     # should return 314 (approximately)
print(circleIntersection([5, 6], [5, 6], 3))       # should return 28
print(circleIntersection([-5, 0], [5, 0], 3))      # should return 0
print(circleIntersection([10, 20], [-5, -15], 20)) # should return 7 (approximately)
print(circleIntersection([-7, 13], [-25, -5], 17)) # should return 66 (approximately)
print(circleIntersection([-20, -4], [-40, 29], 7)) # should return 0
print(circleIntersection([38, -18], [46, -29], 10))# should return 32
print(circleIntersection([-29, 33], [-8, 13], 15)) # should return 2
print(circleIntersection([-12, 20], [43, -49], 23))# should return 0

# Test cases
print(circleIntersection([0, 0], [7, 0], 5))        # should return 14
print(circleIntersection([0, 0], [0, 10], 10))     # should return 314 (approximately)
print(circleIntersection([5, 6], [5, 6], 3))       # should return 28
print(circleIntersection([-5, 0], [5, 0], 3))      # should return 0
print(circleIntersection([10, 20], [-5, -15], 20)) # should return 7 (approximately)
print(circleIntersection([-7, 13], [-25, -5], 17)) # should return 66 (approximately)
print(circleIntersection([-20, -4], [-40, 29], 7)) # should return 0
print(circleIntersection([38, -18], [46, -29], 10))# should return 32
print(circleIntersection([-29, 33], [-8, 13], 15)) # should return 2
print(circleIntersection([-12, 20], [43, -49], 23))# should return 0

# Test cases
print(circleIntersection([0, 0], [7, 0], 5))        # should return 14
print(circleIntersection([0, 0], [0, 10], 10))     # should return 122
print(circleIntersection([5, 6], [5, 6], 3))       # should return 28
print(circleIntersection([-5, 0], [5, 0], 3))      # should return 0
print(circleIntersection([10, 20], [-5, -15], 20)) # should return 15
print(circleIntersection([-7, 13], [-25, -5], 17)) # should return 132
print(circleIntersection([-20, -4], [-40, 29], 7)) # should return 0
print(circleIntersection([38, -18], [46, -29], 10))# should return 64
print(circleIntersection([-29, 33], [-8, 13], 15)) # should return 5
print(circleIntersection([-12, 20], [43, -49], 23))# should return 0
