# Cate vocale si consoane sunt intr-un text dat?

def is_vowel(ch: str) -> bool:
    return ch in 'aeiou'


text = """Acesta este un text mai lung
impartit pe mai multe
linii"""

text = text.lower()
vowel_count = 0
consonant_count = 0

for c in text:
    if is_vowel(c):
        vowel_count += 1
    else:
        consonant_count += 1

print(vowel_count)
print(consonant_count)
