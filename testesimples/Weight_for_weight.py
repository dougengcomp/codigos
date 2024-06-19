def order_weight(strng):
    def sum_of_digits(a):
        my_list_of_digits = [int(num) for num in str(a)]
        return sum(my_list_of_digits)
    
    orig_weights = strng.split()
    new_weights = [(sum_of_digits(item), int(item)) for item in orig_weights]
    ab_sorted = sorted(new_weights, key=lambda x: (x[0], str(x[1])))
    sorted_weights = [str(item[1]) for item in ab_sorted]
    return ' '.join(sorted_weights)

# Test the function
print(order_weight("2000 10003 1234000 44444444 9999 11 11 22 123"))
