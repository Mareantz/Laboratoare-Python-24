#Write a script that receives two strings and prints the number of occurrences of the first string in the second.

def no_of_occurences(s1: str, s2:str) ->int:
    return s2.count(s1)