# Scrieti o functie care converteste un numar din baza 10 in baza 16
# Functia va primi ca parametru numarul in baza 10 si va returna reprezentarea string in baza 16
# Numerele convertite in baza 16 vor avea la inceput prefixul "0x"
# Nu este permisa utilizarea conversiilor din python

def dec_to_hex(nr: int) -> str:
    hex_chars = "0123456789ABCDEF"
    output = ""

    if nr == 0:
        return "0"

    while nr:
        rest = nr % 16
        output = hex_chars[rest] + output
        nr //= 16
    return output


print(dec_to_hex(36251))
