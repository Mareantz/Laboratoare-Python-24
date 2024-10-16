# Write a function that receives a number x, default value equal to 1, a list of strings, and a boolean flag set to
# True. For each string, generate a list containing the characters that have the ASCII code divisible by x if the
# flag is set to True, otherwise it should contain characters that have the ASCII code not divisible by x.
# Example: x = 2, ["test", "hello", "lab002"], flag = False will return (["e", "s"], ["e","o"], ["a"]).
# Note: The function must return list of lists.

def ascii_divisible(strings: list[str], x=1, flag=True):
    result = []
    for string in strings:
        word = []
        for ch in string:
            if (ord(ch) % x == 0) == flag:
                word += ch
        result.append(word)
    return result


print(ascii_divisible(["test", "hello", "lab002"], 2, False))
