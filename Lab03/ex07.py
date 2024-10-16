# Write a function that receives as parameter a list of numbers (integers) and will return a tuple with 2 elements.
# The first element of the tuple will be the number of palindrome numbers found in the list and the second element
# will be the greatest palindrome number.

def is_palindrome(a: int) -> bool:
    return str(a) == str(a)[::-1]


def palindrome_tuple(a: list) -> tuple:
    palindrome_list = [n for n in a if is_palindrome(n)]
    return len(palindrome_list), max(palindrome_list)


numbers = [121, 343, 456, 789, 11, 898, 101]

result = palindrome_tuple(numbers)
print(result)
