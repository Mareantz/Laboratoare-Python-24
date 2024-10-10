# Srieti o functie care primeste ca parametru urmatoarea propozitie:
# "A fost, de asemenea, Remarcabil pentru Razboaiele persane si Pentru razboaiele Dintre orasele-state Grecesti."
# Functia va returna numarul de caractere scrise cu majuscula

def capital_count(s: str) -> int:
    count = 0
    for ch in s:
        if ch.isupper():
            count += 1
    return count


print(capital_count(
    "A fost, de asemenea, Remarcabil pentru Razboaiele persane si Pentru razboaiele Dintre orasele-state Grecesti."))
