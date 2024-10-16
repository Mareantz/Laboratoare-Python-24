# Write a function that receives as parameters two lists a and b and returns: (a intersected with b, a reunited with
# b, a - b, b - a)

def ab_operations(a: set, b: set):
    intersect = a & b
    uni = a | b
    diff_a_b = a - b
    diff_b_a = b - a
    return intersect, uni, diff_a_b, diff_b_a


x = {1, 2, 3, 4}
y = {3, 4, 5, 6}
intersection, union, difference_a_b, difference_b_a = ab_operations(x, y)

print("Intersection:", intersection)
print("Union:", union)
print("Difference (a - b):", difference_a_b)
print("Difference (b - a):", difference_b_a)
