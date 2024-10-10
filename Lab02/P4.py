#Write a script that converts a string of characters written in UpperCamelCase into lowercase_with_underscores.

def lowercase_underscore(s: str) -> str:
    result = ""
    for char in s:
        if char.isupper() and result:
            result += "_" + char.lower()
        else:
            result += char.lower()
    return result
