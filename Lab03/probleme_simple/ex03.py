# afisati continutul unui text, in format hexazecimal pe un tabel cu 17 coloane
# prima coloana va contine indexul hex pe 4 digiti pentru valoarea imediat urmatoare
# celelalte coloane vor contine cate 1 element hex reprezentat pe 2 digiti, aliniat dreapta si umplut cu 0
# prima linie este de asemenea un header cu indexii elementelor de pe fiecare linie (00-0F)
#
# Exemplu:
#        00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
#      +------------------------------------------------
# 0000 | 05 46 9A 5D FF FF 00 00 00 11 19 18 43 44 59 A6
# 0010 | 3D 44 77 78 FF FF FF 00 00 00 00 00 00 00 00 00
# 0020 | 10 10 1D 3B 5A 64

def print_table(text):
    text_to_bytes = text.encode('utf-8')
    header = "          " + " ".join(f"{i:02X}" for i in range(16))
    spacer = "+" + "-" * (len(header) -1)

    print(header)
    print(spacer)

    for index in range(0,len(text_to_bytes),16):
        left = f"{index:04X}"
        partition=text_to_bytes[index:index+16]
        right=" ".join(f"{byte:02X}" for byte in partition)
        print(f"{left} | {right}")

