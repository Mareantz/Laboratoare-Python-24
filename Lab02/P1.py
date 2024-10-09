#Find The greatest common divisor of multiple numbers read from the console.
#Read numbers till input is 0

def gcd(a: int, b:int) -> int:
    if a==0:
        return b
    return gcd(b%a,a)

x=int(input())
y=int(input())
result=gcd(x,y)
while(x):
    result=gcd(x,result)
    x=int(input())
print(result)