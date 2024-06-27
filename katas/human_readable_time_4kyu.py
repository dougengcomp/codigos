'''
Your task in order to complete this Kata is to write a function which formats a duration, given as a number of seconds, in a human-friendly way.

The function must accept a non-negative integer. If it is zero, it just returns "now". Otherwise, the duration is expressed as a combination of years, days, hours, minutes and seconds.

It is much easier to understand with an example:

* For seconds = 62, your function should return 
    "1 minute and 2 seconds"
* For seconds = 3662, your function should return
    "1 hour, 1 minute and 2 seconds"
'''
def format_duration(seconds):
    # Calculate years and days , hours, minutes, and seconds
    years=seconds // 31536000   
    days= (seconds % 31536000) // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    return format_time(years,days,hours,minutes,seconds)

def format_time(years=0, days=0, hours=0, minutes=0, seconds=0):
    parts = []
    
    if years > 0:
        parts.append(f"{years} year" + ("s" if years > 1 else ""))
    if days > 0:
        parts.append(f"{days} day" + ("s" if days > 1 else ""))
    if hours > 0:
        parts.append(f"{hours} hour" + ("s" if hours > 1 else ""))
    if minutes > 0:
        parts.append(f"{minutes} minute" + ("s" if minutes > 1 else ""))
    if seconds > 0:
        parts.append(f"{seconds} second" + ("s" if seconds > 1 else ""))
    
    return ', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1] if parts else 'now'

#8 years, 12 days, 13 hours, 41 minutes and 1 second
print (format_duration(253374061)) 