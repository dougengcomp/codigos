'''
Complete the solution so that it strips all text that follows any of a set of comment markers passed in.
Any whitespace at the end of the line should also be stripped out.
Example:
Given an input string of:

apples, pears # and bananas
grapes
bananas !apples
The output expected would be:

apples, pears
grapes
bananas
The code would be called like so:

result = strip_comments("apples, pears # and bananas\ngrapes\nbananas !apples", ["#", "!"])
# result should == "apples, pears\ngrapes\nbananas"

'''

import re
def strip_comments(strng, markers):
    if len (markers)==0:
        return strng
    pattern=fr"{markers[0]}.*"
    x = re.sub(pattern, "", strng)
    markers.pop(0)
    if (len(markers))>0:
        return (strip_comments(x,markers))
    else:
        return x
    

a="bananas !apples\ncherry #coke"
print (strip_comments(a,['!','#']))