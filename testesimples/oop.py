class Line:

    def __init__(self,tup_a,tup_b):
        self.tup_a=tup_a
        self.tup_b=tup_b
        print (f"Line has been created with coordinates{self.tup_a} and {self.tup_b}")
    
    def distance (self):
        return ((((self.tup_a[0]-self.tup_b[0])**2)+((self.tup_a[1]-self.tup_b[1])**2))**0.5)
    
    def slope (self):
        return ((self.tup_a[1]-self.tup_b[1])/(self.tup_a[0]-self.tup_b[0]))
    
#myline=Line ((3,2),(8,10))
#print (myline.distance())
#print (myline.slope())

class Cylinder:
    pi=3.1415
    def __init__(self, r, h):
        self.radius=r
        self.height=h
        print (f"Cylinder has been created with radius {self.radius} and height {self.height}")
    def volume (self):
        return (self.height)*(self.pi)*(self.radius)**2 
        
    def surface (self):
        return (2*self.pi*(self.radius)**2)+(2*self.pi*self.radius*self.height)

mycylinder=Cylinder(3,2)
print (f"your cylinder volume is {mycylinder.volume()}, and the surface is {mycylinder.surface()}")