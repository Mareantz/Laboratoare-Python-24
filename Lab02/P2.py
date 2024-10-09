#Write a script that calculates how many vowels are in a string.

def is_vowel(ch: str) ->bool:
    return ch in 'aeiou'

def vowel_count(input: str) -> int:
    count=0
    for i in input:
        if is_vowel(i):
            count+=1