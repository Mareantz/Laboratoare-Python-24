# extrageti si afisati primul si ultimul caracter (impreuna ca si cum ar fi cuvinte diferite, separate de cate 1 spatiu) de la toate cuvintele dintr-o propozitie data

def first_last_ch(s: str) -> str:
    output = ""
    words = s.split()
    for word in words:
        output = output + word[0] + " " + word[-1] + " "
    return output
