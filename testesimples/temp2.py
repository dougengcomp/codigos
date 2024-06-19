secret = "whatisup"
triplets = [
  ['t','u','p'],
  ['w','h','i'],
  ['t','s','u'],
  ['a','t','s'],
  ['h','a','p'],
  ['t','i','s'],
  ['w','h','s']
]
new_list = [item for sublist in triplets for item in sublist]
myset=set(new_list)

from itertools import permutations

def generate_unique_strings(letters_set, length):
    # Convert the set to a sorted list to ensure consistent order
    sorted_letters = sorted(letters_set)
    
    # Generate all permutations of letters of the given length
    all_permutations = permutations(sorted_letters, length)
    
    # Join each permutation into a string and collect them in a list
    result = [''.join(perm) for perm in all_permutations]
    
    return result

# Example usage:
letters_set = {'w', 'h', 't', 's', 'u', 'p', 'a', 'i'}
string_length = len (letters_set)
result = generate_unique_strings(letters_set, string_length)

# Print the result (first few elements for demonstration)
print(len(result))  
