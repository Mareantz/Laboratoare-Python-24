# Srieti o functie care primeste ca parametru o expreise matematica cu paranteze rotunde si verifica daca parantezarea este sau nu corecta
# Exemplu 1: "6+8*(5+3/2-1+6/(3+9)-7*(5+7/3))" va returna True
# Exemplu 2: "8-4*(3+7/8+4/(5-9)" va returna False

def check_parentheses(s: str) -> bool:
    counter = 0

    for ch in s:
        if ch == '(':
            counter += 1
        elif ch == ')':
            counter -= 1
        if counter < 0:
            return False
    return counter == 0


print(check_parentheses("6+8*(5+3/2-1+6/(3+9)-7*(5+7/3))"))
print(check_parentheses("8-4*(3+7/8+4/(5-9)"))
