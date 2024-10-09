#Write a function that validates if a number is a palindrome.

def palindrome(input:int) -> bool:
    aux=0
    copy=input
    while(copy>0):
        aux=aux*10+copy%10
        copy=copy//10
    return input==aux