# Write a function that will receive a list of words as parameter and will return a list of lists of words,
# grouped by rhyme. Two words rhyme if both of them end with the same 2 letters. Example: group_by_rhyme(['ana',
# 'banana', 'carte', 'arme', 'parte']) will return [['ana', 'banana'], ['carte', 'parte'], ['arme']]

def group_by_rhyme(words: list) -> list[list]:
    rhyme_groups = {}
    for word in words:
        rhyme_key = word[-2:]
        if rhyme_key in rhyme_groups:
            rhyme_groups[rhyme_key].append(word)
        else:
            rhyme_groups[rhyme_key] = [word]

    return list(rhyme_groups.values())


test = ['ana', 'banana', 'carte', 'arme', 'parte']
result = group_by_rhyme(test)
print(result)
