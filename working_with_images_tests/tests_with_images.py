from PIL import Image
'''
#cropping, copying, pasting, resizing images
mac = Image.open('example.jpg')
#cropping
x=880
y=845
w=1140
h=1200

computer=mac.crop((x,y,w,h)) #this crops and copies
#pasting
mac.paste(im=computer,box=(0,0))
mac.paste(im=computer,box=(796,0))
#resizing
h,w = mac.size
new_h = int(h/3)
new_w = int(w/3)
macpequeno=mac.resize((new_h,new_w))
macpequeno.show()
'''

#mac.crop((x,y,w,h)).show()


''' 
In the crop method of the Pillow library, the coordinates should be provided as a tuple of the form (left, upper, right, lower), where:
left is the x-coordinate of the left edge of the cropping box.
upper is the y-coordinate of the top edge of the cropping box.
right is the x-coordinate of the right edge of the cropping box.
lower is the y-coordinate of the bottom edge of the cropping box.
'''
#print (type(mac)) 
#print (mac.size) #(1993, 1257)
#print (mac.filename)
#print (mac.format_description)

'''
#pencils = Image.open("pencils.jpg")
#pencils.show()
#pencils.show()
#print (pencils.size)
# Start at top corner (0,0)
#x = 0
#y = 0
# Grab about 10% in y direction , and about 30% in x direction
#w = 1950/3
#h = 1300/10
#pencils.crop((x,y,w,h)).show()
x= 0 
y = 1100
w = 1950
h = 1300
pencils.crop((x,y,w,h)).show()
'''
wordmatrix_orig = Image.open("word_matrix.png")
wordmatrix_orig.putalpha(128)
mask_orig=Image.open("mask.png")
mask_rightsize=mask_orig.resize((1015,559))
mask_rightsize.putalpha(128)
mask_rightsize.paste(wordmatrix_orig,box=(0,0),mask=wordmatrix_orig)
mask_rightsize.show()


