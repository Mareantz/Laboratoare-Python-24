# The validate_dict function that receives as a parameter a set of tuples ( that represents validation rules for a
# dictionary that has strings as keys and values) and a dictionary. A rule is defined as follows: (key, "prefix",
# "middle", "suffix"). A value is considered valid if it starts with "prefix", "middle" is inside the value (not at
# the beginning or end) and ends with "suffix". The function will return True if the given dictionary matches all the
# rules, False otherwise. Example: the rules s={("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
# and d= {"key1": "come inside, it's too cold out", "key3": "this is not valid"} => False because although the rules
# are respected for "key1" and "key2" "key3" that does not appear in the rules.

def validate_dictionary(rules: set, dictionary: dict) -> bool:
    for key, prefix, middle, suffix in rules:
        if key not in dictionary:
            return False
        if not dictionary[key].startswith(prefix):
            return False
        if middle not in dictionary[key]:
            return False
        if not dictionary[key].endswith(suffix):
            return False
    return True


rules1 = {("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
d1 = {"key1": "come inside, it's too cold out", "key2": "starting in the middle of the winter"}
d2 = {"key1": "come inside, it's too cold, out", "key3": "this is not valid"}

print(validate_dictionary(rules1, d1))
print(validate_dictionary(rules1, d2))
