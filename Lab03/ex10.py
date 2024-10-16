# Write a function that receives a variable number of lists and returns a list of tuples as follows: the first tuple
# contains the first items in the lists, the second element contains the items on the position 2 in the lists,
# etc. Example: for lists [1,2,3], [5,6,7], ["a", "b", "c"] return: [(1, 5, "a ") ,(2, 6, "b"), (3,7, "c")]. Note: If
# input lists do not have the same number of items, missing items will be replaced with None to be able to generate
# max ([len(x) for x in input_lists]) tuples.

def tuple_lists(*lists) -> list[tuple]:
    max_length = max(len(sublist) for sublist in lists)
    result = []
    for i in range(max_length):
        current_tuple = tuple(sublist[i] if i < len(sublist) else None for sublist in lists)
        result.append(current_tuple)
    return result


a = [1, 2, 3]
b = [5, 6, 7]
c = "abc"

print(tuple_lists(a, b, c))
