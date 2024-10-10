# rescrieti cuvintele unei propozitii, in ordine inversa

def reverse(s: str) -> str:
    s = s.strip()
    word = ""
    reversed_text = ""
    for char in reversed(s):
        if char == " ":
            if word:
                reversed_text += word + " "
                word = ""
        else:
            word = char + word

    if word:
        reversed_text += word

    return reversed_text.strip()


print(reverse("I want to reverse the order of these words"))
