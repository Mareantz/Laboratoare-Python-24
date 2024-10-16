# Write a function that receives as a parameter a variable number of lists and a whole number x. Return a list
# containing the items that appear exactly x times in the incoming lists. Example: For the [1,2,3], [2,3,4],[4,5,6],
# [4,1, "test"] and x = 2 lists [1,2,3 ] # 1 is in list 1 and 4, 2 is in list 1 and 2, 3 is in lists 1 and 2.

def appear_x_times(x: int, *lists) -> list:
    combined_list = []
    for i in lists:
        combined_list.extend(i)
    result = []
    for i in set(combined_list):
        if combined_list.count(i) == x:
            result.append(i)
    return result


a = appear_x_times(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"])
print(a)
