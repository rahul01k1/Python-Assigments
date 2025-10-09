# Que : Write a Python program to concatenate two tuples.

# Define two tuples with multiple data types
tuple1 = (1, 2, 3)
tuple2 = ('a', 'b', 'c')

# Concatenate tuples using + operator
concatenated_tuple = tuple1 + tuple2

# Print the concatenated tuple
print("Concatenated Tuple:", concatenated_tuple)


# Other ways to concatenate tuples

# 1. Using += operator to extend a tuple variable:

tuple1 += tuple2
print("Tuple after += :", tuple1)

# 2.Using itertools.chain() for efficient concatenation:

import itertools

tuple3 = tuple(itertools.chain(tuple1, tuple2))
print("Concatenated using itertools.chain:", tuple3)


# 3. Using unpacking with * operator:

tuple4 = (*tuple1, *tuple2)
print("Concatenated using unpacking:", tuple4)
