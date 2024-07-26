
'''
Write a function called sumIntervals/sum_intervals that accepts an array of intervals, and returns the sum of all the interval lengths. Overlapping intervals should only be counted once.
Intervals
Intervals are represented by a pair of integers in the form of an array. The first value of the interval will always be less than the second value. Interval example: [1, 5] is an interval from 1 to 5. The length of this interval is 4.
'''
#not yet finished...
import pdb

def generate_range(range_list):
    start, end = range_list
    return list(range(start, end + 1))

def merge_ordered_lists(list1, list2):
    """Merge two ordered lists into a single ordered list without duplicates."""
    merged_list = []
    i, j = 0, 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            if not merged_list or merged_list[-1] != list1[i]:
                merged_list.append(list1[i])
            i += 1
        elif list1[i] > list2[j]:
            if not merged_list or merged_list[-1] != list2[j]:
                merged_list.append(list2[j])
            j += 1
        else:
            if not merged_list or merged_list[-1] != list1[i]:
                merged_list.append(list1[i])
            i += 1
            j += 1
    
    while i < len(list1):
        if not merged_list or merged_list[-1] != list1[i]:
            merged_list.append(list1[i])
        i += 1
    
    while j < len(list2):
        if not merged_list or merged_list[-1] != list2[j]:
            merged_list.append(list2[j])
        j += 1
    
    return merged_list


def sum_of_intervals(intervals):
    i=2
    temp_interval1=generate_range(intervals[0])
    temp_interval2=generate_range(intervals[1])
    merged_interval=merge_ordered_lists(temp_interval1,temp_interval2)
    for item in intervals[2:]:
        pdb.set_trace()
        merged_interval=merged_interval+generate_range(intervals[i])
        i+=1
        print (merged_interval)
             

#print(generate_range([-1, 4]))
sum_of_intervals([[-1,4],[7,10]])