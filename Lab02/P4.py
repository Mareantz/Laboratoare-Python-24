#Write a script that converts a string of characters written in UpperCamelCase into lowercase_with_underscores.

def lowercase_underscore(s:str) ->str:
    return s.lower().replace(" ","_")