# Write a function that receives a list of numbers and returns a list of the prime numbers found in it.

def is_prime(a: int) -> bool:
    if a < 2:
        return False
    if a == 2:
        return True
    if a % 2 == 0:
        return False
    for i in range(3, int(a ** 0.5) + 1, 2):
        if a % i == 0:
            return False
    return True


def primes(a: list) -> list:
    return list(filter(lambda x: is_prime(x), a))


print(primes(list(range(1, 101))))
