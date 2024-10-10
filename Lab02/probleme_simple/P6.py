# Srieti o functie care primeste ca parametru o propozitie si afiseaza pe cate o linie, reprezentarea hex pentru codurile ASCII a caracterelor din fiecare cuvant
# Practic orice cuvant va fi rescris pe o linie nou, dar in format hex (cate 2 digiti per caracter, toti digitii uniti intre ei)
# Exemplu, pentru "abc 012" se va afisa
# 616263
# 303132

def text_to_hex(s: str) -> str:
    output = ""
    for ch in s:
        if ch == " ":
            output += "\n"
        else:
            output += format(ord(ch), 'x')
    return output


print(text_to_hex("abc 012"))
