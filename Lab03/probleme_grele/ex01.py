# Se da fisierul JSON care contine o lista de studenti cu notele luate in timpul semestrului la o materie.
# https://pastebin.com/6jet8F8q Fisierul JSON are urmatorul format: Nume student, 13 note la seminarii (intre 1 si
# 10), o nota la un test partial (maxim 100p), o nota la testul de curs (maxim 100p), o nota la un proiect (maxim
# 70p). Cele 13 note in total valoreaza 20% din nota finala Notele la cele 2 teste valoreaza fiecare cate 30% din
# nota finala Proiectul valoreaza 20% din nota finala Un student trace daca per total cumuleaza 45% din totalul de
# puncte Cati studenti au trecut si cati studenti au picat materia?

import json
import numpy


def ex1hard(jsonfile):
    data = json.load(open(jsonfile, 'r'))
    count = 0
    for elev, details in data.items():
        print(elev)
        print(details)
        seminariimean = numpy.mean(details['seminarii'])
        projectgrade = (details['proiect'] / 7)
        finalgrade = 0.3 * details['partial'] / 10 + 0.3 * details[
            'curs'] / 10 + seminariimean * 0.2 + projectgrade * 0.2
        if finalgrade >= 4.5:
            count += 1
    return count

print(ex1hard('studenti.json'))