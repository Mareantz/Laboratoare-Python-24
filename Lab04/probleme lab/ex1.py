# 1. calculati al 2000-lea numar fibonacci, stiind ca primele 2 sunt [0, 1]
# F(2k) = F(k) * [2 * F(k+1) - F(k)]
# F(2k+1) = F(k+1)^2 + F(k)^2

def fibonacci_efficient(n):
    if n == 0:
        return 0, 1
    else:
        a, b = fibonacci_efficient(n >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if n % 2 == 1:
            return d, c + d
        else:
            return c, d


fibonacci_2000, _ = fibonacci_efficient(2000)
print(fibonacci_2000)
