# Write a function that receives a variable number of sets and returns a dictionary with the following operations
# from all sets two by two: reunion, intersection, a-b, b-a. The key will have the following form: "a op b",
# where a and b are two sets, and op is the applied operator: |, &, -. Ex:
# {1,2}, {2, 3} =>
# {
#     "{1, 2} | {2, 3}":  {1, 2, 3},
#     "{1, 2} & {2, 3}":  { 2 },
#     "{1, 2} - {2, 3}":  { 1 },
#     ...
# }

def set_operations(*args) -> dict:
    result = {}
    for i in range(len(args)):
        for j in range(i + 1, len(args)):
            result[f"{args[i]} | {args[j]}"] = args[i] | args[j]
            result[f"{args[i]} & {args[j]}"] = args[i] & args[j]
            result[f"{args[i]} - {args[j]}"] = args[i] - args[j]
            result[f"{args[j]} - {args[i]}"] = args[j] - args[i]
    return result


set1 = {1, 2, 3, 4, 5}
set2 = {3, 4, 5, 6, 7}
set3 = {5, 6, 7, 8, 9}
result1 = set_operations(set1, set2, set3)
for key, value in result1.items():
    print(f"{key}: {value}")
