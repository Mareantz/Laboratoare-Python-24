# Write a function that receives as a parameter a list and returns a tuple (a, b), a representing the number of
# unique elements in the list, and b representing the number of duplicate elements in the list (use sets to achieve
# this objective).

def count_unique_duplicate(lst: list) -> tuple:
    return len(set(lst)), len(lst) - len(set(lst))


lst1 = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6]
print(count_unique_duplicate(lst1))
