
'''
mplement a function that receives two IPv4 addresses, and returns the number of addresses between them (including the first one, excluding the last one).

All inputs will be valid IPv4 addresses in the form of strings. The last address will always be greater than the first one.

Examples
* With input "10.0.0.0", "10.0.0.50"  => return   50 
* With input "10.0.0.0", "10.0.1.0"   => return  256 
* With input "20.0.0.10", "20.0.1.0"  => return  246
'''
import re
import numpy as np
     
def ips_between(start, end):
    def make_ip_binary(ip):
        return np.int64(int(''.join([f"0b{num:08b}" for num in ip]).replace('0b', ''), 2)) 
    pattern=r'\b(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b'
    matches_end = [int(x) for x in re.findall(pattern, end)]
    matches_start=[int(x) for x in re.findall(pattern, start)]
    diff= (make_ip_binary(matches_end)-make_ip_binary(matches_start))   
    return diff
    

s="10.0.0.0"
e="10.0.1.0"
print (ips_between(s,e))
