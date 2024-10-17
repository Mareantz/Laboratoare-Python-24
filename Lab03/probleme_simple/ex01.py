# pentru un paragraf citit dintr-un fisier, calculati frecventa caracterelor (case insensitive)
# generati un grafic text pe care sa il scrieti intr-un fisier, caracterele folosite pentru grafic vor fi 'o'

def character_freq(read_file, write_file):
    paragraphs = open(read_file, "r").read()
    char_freq = {}
    for char in paragraphs:
        if char.isalnum():
            if char.lower() not in char_freq:
                char_freq[char.lower()] = 0
            char_freq[char.lower()] += 1
    height = max(char_freq.values())
    histogram = []
    for i in range(height):
        line = []
        for value in char_freq.values():
            if value <= i:
                line.append('o')
            else:
                line.append(' ')
            histogram.append(line)
        histogram.append(char_freq.keys())
    open(write_file, 'w').write('\n'.join(''.join(line) for line in histogram))


character_freq('Studenti.txt', 'Output.txt')
