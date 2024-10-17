# pentru caracterele 'A'-'Z' generati o lista de tuple de genul: [('A', 65, 25), ('B', 66, 24), ...., ('Z', 90,
# 0)] unde primul element din tuplu este caracterul in sine, al 2-lea element este codul ascii in baza 10,
# iar al 3-lea element este un index invers in range-ul (0,..,25) Construiti lista cu o singura linie de cod

lst = [(chr(i), i, 25 - (i - 65)) for i in range(65, 91)]
print(lst)
