# Generati permutarea 218553019 a cuvantului format din 6 caractere folosind alfabetul "AEGIJLNOPSUVbdefhimnoprstuvwxy". Primul cuvant este "AAAAAA" iar ultimul este "yyyyyy"
# Care este cuvantul?
# Descrieti 3 mecanisme si sortati-le crescator in ordinea performantei pentru a gasi indexul oricarui cuvant dat

def transform(x, alphabet):
    rest = 0
    word = ""
    while x:
        rest = x % len(alphabet)
        x = x // len(alphabet)
        word = str(alphabet[rest]) + word
    return word


print(transform(218553019, "AEGIJLNOPSUVbdefhimnoprstuvwxy"))
