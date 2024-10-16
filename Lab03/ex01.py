# Write a function to return a list of the first n numbers in the Fibonacci string.

def fibonacci(n: int):
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    fib = [1, 1]
    for i in range(n - 2):
        fib.append(fib[-1] + fib[-2])
    return fib


print(fibonacci(6))
