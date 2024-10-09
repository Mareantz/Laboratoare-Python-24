#Write a function that counts how many words exists in a text. A text is considered to be form out of words that are separated by only ONE space. For example: "I have Python exam" has 4 words.

def count_words(s:str) -> int:
    s=s.replace('\n',' ')
    s=' '.join(s.split())
    if len(s)==0:
        return 0
    return s.count(' ')+1

text= """I    do     exercies for 
Python    lab
soon.     I'm almost done"""

print(count_words(text))