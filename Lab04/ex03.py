# Compare two dictionaries without using the operator "==" returning True or False. (Attention, dictionaries must be
# recursively covered because they can contain other containers, such as dictionaries, lists, sets, etc.)

def compare_dictionaries(dict1: dict, dict2: dict) -> bool:
    if len(dict1) != len(dict2):
        return False
    for key in dict1:
        if key not in dict2:
            return False
        if type(dict1[key]) is not type(dict2[key]):
            return False
        if type(dict1[key]) is dict:
            if not compare_dictionaries(dict1[key], dict2[key]):
                return False
        elif type(dict1[key]) is list or type(dict1[key]) is set:
            if set(dict1[key]) != set(dict2[key]):
                return False
        else:
            if dict1[key] != dict2[key]:
                return False
    return True


dictionary1 = {'a': 3, 's': 2, '.': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 2, ' ': 2, 'A': 1, 'n': 1}
dictionary2 = {'a': 3, 's': 2, '.': 2, 'e': 1, 'h': 1, 'l': 1, 'p': 2, ' ': 2, 'A': 1, 'n': 1}

print(compare_dictionaries(dictionary1, dictionary2))
