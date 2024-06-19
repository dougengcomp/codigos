from datetime import datetime
import time

# Get the current date and time
t1 = datetime.now()

# Introduce a very short delay (e.g., 1 millisecond)
time.sleep(0.001)

# Get the current date and time again
t2 = datetime.now()

# Calculate the time difference
time_difference = t2 - t1

# Convert to total microseconds for higher precision
total_microseconds = time_difference.total_seconds() * 1_000

print(f'shift is: {total_microseconds} milisec')
