import re

text = "My telephone number is 408-555-1234 514-652-3596"

phone=re.findall(r'\d{3}-\d{3}-\d{4}',text)

print (phone)