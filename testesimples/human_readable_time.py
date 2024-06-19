'''
Write a function, which takes a non-negative integer (seconds) as input and returns the time in a human-readable format (HH:MM:SS)

HH = hours, padded to 2 digits, range: 00 - 99
MM = minutes, padded to 2 digits, range: 00 - 59
SS = seconds, padded to 2 digits, range: 00 - 59
The maximum time never exceeds 359999 (99:59:59)

You can find some examples in the test fixtures.
'''
import math

def make_readable(seconds):
    # Calculate hours, minutes, and seconds
    hours = seconds // 3600
    print ((seconds % 3600))
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    # Format and return the result as HH:MM:SS
    return f"{hours:02}:{minutes:02}:{seconds:02}"

print (make_readable(357720)) 