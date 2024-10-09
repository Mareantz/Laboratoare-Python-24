#Write a function that extract a number from a text (for example if the text is "An apple is 123 USD", this function will return 123, or if the text is "abc123abc" the function will extract 123). The function will extract only the first number that is found.

def extract_first_number(s: str) -> int:
    number = ""
    for char in s:
        if char.isdigit(): 
            number += char
        elif number:
            break
    return number

print(extract_first_number("An apple is 123 USD 521521"))
print(extract_first_number("abc123abc12"))