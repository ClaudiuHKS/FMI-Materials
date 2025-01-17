import cProfile, random
from queue import Queue, LifoQueue
from collections import Counter, deque


"""
ncalls: numărul de apeluri
tottime: timpul total (agregat) în care a fost executată funcția curentă
percall: Raportul dintre timpul total și numărul de apeluri (cât a durat în medie o executare a acelei funcții\
cumtime: Timpul cumulat al executării funcției, împreună cu funcțiile apelate de către ea
percall: Se referă la al doilea percall din raport. Reprezintă raportul dintre timpul cumulat (cumtime) și numărul de apeluri (ncalls)
filename_lineno(function): Punctual din program, care a fost evaluat ( de exemplu un număr de linie din program sau un apel de funcție).


"""

"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii/stivei până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada/stiva și input()

De asemenea, apelurile algoritmilor sunt la final. Este doar unul dintre ele decomentat. Voi trebuie sa comentati/decomentati apelurile în funcție de ce vă interesează sa rulați.
"""


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, id, info, parinte):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print("->".join(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        # return infoNodNou in self.obtineDrum()
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += ")"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri = noduri
        self.matrice = matrice
        self.nrNoduri = len(matrice)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent)
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
# noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
#
# m = [
#     [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
# ]
#
# start = "a"
# scopuri = ["f", "j"]
# gr = Graph(noduri, m, start, scopuri)


#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix) prin urmare vom folosi o variabilă numită nrSolutiiCautate
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii

def breadth_first(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None)]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        lSuccesori = gr.genereazaSuccesori(nodCurent)

        c.extend(lSuccesori)

        for i in lSuccesori:
            if gr.testeaza_scop(i):
                print("Solutie:")
                i.afisDrum()
                print("\n----------------\n")
                input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return


def breadth_first_queue(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    coada = Queue()
    coada.put(NodParcurgere(gr.noduri.index(gr.start), gr.start, None))
    while not coada.empty():
        print("Coada actuala: ")
        for nod in list(coada.queue):
            print(nod, end=" ")

        nodCurent = coada.get()

        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for i in lSuccesori:
            if gr.testeaza_scop(i):
                print("Solutie:")
                i.afisDrum()
                print("\n----------------\n")
                input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            coada.put(i)


def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate)


def df(nodCurent, nrSolutiiCautate):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    input()

    if gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)

    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            print("Nodul expandat:" + str(nodCurent))
            nrSolutiiCautate = df(sc, nrSolutiiCautate)

    print("se intoarce -> " + str(nodCurent))
    return nrSolutiiCautate


# df(a)->df(b)->df(c)
#############################################

def dfs_nerecursiv_lista(nodCurent, nrSolutiiCautate):
    stiva = []
    vizitat = []
    stiva.append(nodCurent)
    while len(stiva) > 0:
        print("Stiva actuala: " + "->".join(stiva[-1].obtineDrum()))
        for i in gr.genereazaSuccesori(stiva[-1]):
            if i.info not in vizitat:
                vizitat.append(i.info)
                stiva.append(i)
                break # se da break cand se adauga un nod nou
        else: # daca n-am gasit niciun succesor
            if gr.testeaza_scop(stiva[-1]):
                print("Solutie: ", end="")
                stiva[-1].afisDrum()
                print("\n----------------\n")
                # input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return nrSolutiiCautate
            while len(vizitat) > 0 and vizitat[-1] != stiva[-1].info:
                # scoate din vizitat copiii nodului pe care il scoatem acum, doar ca nu si nodul actual
                # pentru ca e la randul lui copilul altui nod
                vizitat.pop()
            stiva.pop()

def dfs_nerecursiv_deque(nodCurent, nrSolutiiCautate):
    stiva = deque()
    vizitat = []
    stiva.append(nodCurent)
    while len(stiva) > 0:
        print("Stiva actuala: " + "->".join(stiva[-1].obtineDrum()))
        for i in gr.genereazaSuccesori(stiva[-1]):
            if i.info not in vizitat:
                vizitat.append(i.info)
                stiva.append(i)
                break
        else: # daca n-am gasit niciun succesor
            if gr.testeaza_scop(stiva[-1]):
                print("Solutie: ", end="")
                stiva[-1].afisDrum()
                print("\n----------------\n")
                # input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return nrSolutiiCautate
            while len(vizitat) > 0 and vizitat[-1] != stiva[-1].info:
                # scoate din vizitat copiii nodului pe care il scoatem acum, doar ca nu si nodul actual
                # pentru ca e la randul lui copilul altui nod
                vizitat.pop()
            stiva.pop()

def dfs_nerecursiv_lifo_queue(nodCurent, nrSolutiiCautate):
    stiva = LifoQueue()
    vizitat = []
    stiva.put(nodCurent)
    while not stiva.empty():
        print("Stiva actuala: " + "->".join(stiva.queue[-1].obtineDrum()))
        for i in gr.genereazaSuccesori(stiva.queue[-1]):
            if i.info not in vizitat:
                vizitat.append(i.info)
                stiva.put(i)
                break
        else: # daca n-am gasit niciun succesor
            if gr.testeaza_scop(stiva.queue[-1]):
                print("Solutie: ", end="")
                stiva.queue[-1].afisDrum()
                print("\n----------------\n")
                # input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return nrSolutiiCautate
            while len(vizitat) > 0 and vizitat[-1] != stiva.queue[-1].info:
                # scoate din vizitat copiii nodului pe care il scoatem acum, doar ca nu si nodul actual
                # pentru ca e la randul lui copilul altui nod
                vizitat.pop()
            stiva.get()

def dfi(nodCurent, adancime, nrSolutiiCautate, dict):
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    # input()
    if adancime == 1 and gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        # input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        print("Nodul expandat:" + str(nodCurent))
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                dict.append(nodCurent.info)
                # dict[nodCurent.id] += 1
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate, dict)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    dict = []
    # dict = [0] * gr.nrNoduri
    for i in range(1, gr.nrNoduri + 1):
        if nrSolutiiCautate == 0:
            var = Counter(dict)
            for j in noduri:
                if j not in dict:
                    var[j] = 0
            print(var)

            return

        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), i, nrSolutiiCautate, dict)


"""
Mai jos puteti comenta si decomenta apelurile catre algoritmi. Pentru moment e apelat doar breadth-first
"""

# breadth_first(gr, nrSolutiiCautate=4)
# breadth_first_queue(gr, nrSolutiiCautate=4)
# cProfile.run("breadth_first(gr, nrSolutiiCautate=4)")
# cProfile.run("breadth_first_queue(gr, nrSolutiiCautate=4)")
####################################################


# depth_first(gr, nrSolutiiCautate=5)


# dfs_nerecursiv_lista(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_lista(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")

# dfs_nerecursiv_deque(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_deque(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")

# dfs_nerecursiv_lifo_queue(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_lifo_queue(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")



# cProfile.run("depth_first(gr, nrSolutiiCautate=5)")
##################################################

# depth_first_iterativ(gr, nrSolutiiCautate=4)

n = 20
nodes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]

adjacency_matrix = [[0 for i in range(n)] for i in range(n)]
m = 200

for i in range(m):
    a = random.randint(0,n-1)
    b = random.randint(0,n-1)
    adjacency_matrix[a][b] = adjacency_matrix[b][a] = 1

print("Matricea de adiacenta:")
for i in range(n):
    print(adjacency_matrix[i])

print("\nNoduri scope:")

scopes = []

for i in range(5):
    scope = random.choice(nodes)
    scopes.append(scope)

print(scopes, "\n")

gr = Graph(nodes, adjacency_matrix, "a", scopes)

# dfs_nerecursiv_lista(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_lista(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")

# dfs_nerecursiv_deque(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_deque(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")

# dfs_nerecursiv_lifo_queue(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)
# cProfile.run("dfs_nerecursiv_lifo_queue(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate=5)")