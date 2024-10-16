# Write a function that will order a list of string tuples based on the 3rd character of the 2nd element in the tuple.
# Example: ('abc', 'bcd'), ('abc', 'zza')] ==> [('abc', 'zza'), ('abc', 'bcd')]

def order_tuples(tuples: list[tuple]) -> list[tuple]:
    return sorted(tuples, key=lambda x: x[1][2])


a = [('abc', 'bcd'), ('abc', 'zza')]
result = order_tuples(a)
print(result)
