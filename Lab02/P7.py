#Write a function that counts how many bits with value 1 a number has. For example for number 24, the binary format is 00011000, meaning 2 bits with value "1"

def count_bits(input:int) -> int:
    return bin(input).count('1')
