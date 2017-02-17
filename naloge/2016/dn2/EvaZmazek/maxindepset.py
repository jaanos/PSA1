# -*- coding: utf-8 -*-
from functools import lru_cache

def maxCycleTreeIndependentSet(T, w):
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).
    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), \
        "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
        "Podani graf ni neusmerjen!"
    k = len(w)
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])

    @lru_cache(maxsize=None)
    def vzorciZaPot(k):
        if vsi_vzorci_za_pot[k] is not None:
            return vsi_vzorci_za_pot[k]
        if k == 0:
            return [], []
        if k == 1:
            return [[0], [1]], [0, 1]
        if k == 2:
            return [[0, 0], [0, 1], [1, 0]], [0, 1, 2]
        if k == 3:
            return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 1]], [0, 1, 2, 4, 5]
        vzorci = []
        stevilo = []
        for i in vzorciZaPot(k - 2)[0]:
            vzorci += [[1, 0] + i]
        for j in vzorciZaPot(k - 1)[0]:
            vzorci += [[0] + j]
        for i in vzorciZaPot(k - 2)[1]:
            stevilo += [2 ** (k - 1) + i]
        for j in vzorciZaPot(k - 1)[1]:
            stevilo += [j]
        vsi_vzorci_za_pot[k] = vzorci, stevilo
        return vzorci, stevilo

    vsi_vzorci_za_pot = [None for j in range(max(k+1, 4))]
    for j in range(4):
        vsi_vzorci_za_pot[j] = vzorciZaPot(j)
    vzorciZaPot(k)

    def vzorciZaCikel(k):
        """
        Opis funkcije:
        časovna zahtevnost: eksponentna v k
        Prostorska zahtevnost:
        """
        if k == 0:
            return [], []
        if k == 1:
            return [[0], [1]], [0, 1]
        if k == 2:
            return [[0, 0], [0, 1], [1, 0]], [0, 1, 2]
        if k == 3:
            return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], [0, 1, 2, 4]
        vzorci = []
        stevilo = []
        for i in vsi_vzorci_za_pot[k - 3][0]:
            vzorci += [[1, 0] + i + [0]]
            vzorci += [[0] + i + [0, 1]]
        for j in vsi_vzorci_za_pot[k - 2][0]:
            vzorci += [[0] + j + [0]]
        for i in vsi_vzorci_za_pot[k - 3][1]:
            stevilo += [2 ** (k - 1) + i * 2, i * 4 + 1]
        for j in vsi_vzorci_za_pot[k - 2][1]:
            stevilo += [j * 2]
        return vzorci, stevilo

    vzorciZaCikel_sez = vzorciZaCikel(k)
    vsi_vzorci_za_cikel = vzorciZaCikel_sez[0]

    def vsotaVzorca(indexVzorca, u):
        """
        Opis funkcije:
        dolzina vzorca = k (zapisanjega v obliki vzorca, ta je v obliki stevilke)
        Časovna zahtevnost:
        Prostorska zahtevnost:
        """
        vsota = 0
        vzorcek = vsi_vzorci_za_cikel[indexVzorca]
        for i in range(k):
            if vzorcek[i] == 1:
                vsota += w[i][u]
        return vsota

    def slovarZdruzljivih(vzorci):
        """
        za množico vzorcev ustvari slovar združljivih vzorcev (vzorci so podani s tevili, ki jih vzorci
        predstavljajo, če na njih gledamo kot na dvojiški zapis števila).
        Časovna zahtevnost:
        Prostorska zahtevnost:
        """
        slovar = dict()
        for vzorec in vzorci:
            slovar[vzorec] = [indeks for indeks, j in enumerate(vzorci) if vzorec&j == 0]
        return slovar

    def nothing(u, v=None):
        """
        Previsit/postvisit funkcija, ki ne naredi nič.
        Časovna zahtevnost: O(1)
        """
        return True

    vzorci = vzorciZaCikel_sez[1]
    vrednostiVozliscSedem = [[None]*len(vzorci) for i in range(n)]

    zdruzljivi = slovarZdruzljivih(vzorciZaCikel_sez[1])

    range_l = range(len(vzorci))

    def postvisitSedem(u,v):
        for indexVzorca in range_l:
            vzorec = vzorci[indexVzorca]
            vsota = vsotaVzorca(indexVzorca, u)
            vrednostiVozliscSedem[u][indexVzorca] = (vsota, [(u, indexVzorca)])
            for sin in T[u]:
                if sin == v:
                    continue
                maximum = 0
                sezna = []
                for indexMoznega in zdruzljivi[vzorec]:
                        if vrednostiVozliscSedem[sin][indexMoznega][0] > maximum:
                            maximum = vrednostiVozliscSedem[sin][indexMoznega][0]
                            sezna = vrednostiVozliscSedem[sin][indexMoznega][1]
                vrednost, seznamcek = vrednostiVozliscSedem[u][indexVzorca]
                vrednost += maximum
                seznamcek += sezna
                vrednostiVozliscSedem[u][indexVzorca] = (vrednost, sorted(seznamcek))
        return True


    def DFS(G, roots=None, previsit=nothing, postvisit=nothing):
        """
        Rekurzivno iskanje v globino.
        Graf G je podan kot seznam seznamov sosedov za vsako vozlišče.
        Seznam roots določa vozlišča, iz katerih se začne iskanje
        - privzeto so to vsa vozlišča v grafu.
        Spremenljivki previsit in postvisit določata funkciji,
        ki se izvedeta ob prvem oziroma zadnjem obisku posameznega vozlišča.
        Kot vhod dobita trenutno vozlišče in njegovega predhodnika
        (oziroma None, če tega ni).
        Da se algoritem nadaljuje, morata vrniti True;
        če vrneta False, se funkcija prekine in vrne False.
        Če iskanje pride do konca, funkcija vrne True.
        Časovna zahtevnost: O(m) + O(n) klicev funkcij previsit in postvisit
        """

        def explore(u, v=None):
            """
            Obišče vozlišče u, če še ni bilo obiskano,
            in se rekurzivno kliče na njegovih sosedih.
            Časovna zahtevnost: O(d(u)) + klica funkcij previsit in postvisit
            """
            if visited[u]:
                return True
            visited[u] = True
            if not previsit(u, v):
                return False
            for w in G[u]:
                if not explore(w, u):
                    return False
            return postvisit(u, v)

        n = len(G)
        visited = [False] * n
        if roots is None:
            roots = range(n)
        for u in roots:
            if not explore(u):
                return False
        return True

    DFS(T, roots=None, previsit=nothing, postvisit=postvisitSedem)

    vrednost, seznamVzorcevZaVsakoVozlisceTree = max(vrednostiVozliscSedem[0][k] for k in range(len(vzorciZaCikel_sez[0])))

    uporabljeneTocke = []
    for vozlisceDrevesa, indexVzorec in seznamVzorcevZaVsakoVozlisceTree:
        vzorcek = vzorciZaCikel(k)[0][indexVzorec]
        for i in range(k):
            if vzorcek[i] == 1:
                uporabljeneTocke += [(i, vozlisceDrevesa)]

    return (vrednost, uporabljeneTocke)


T = [[1, 46, 47, 48], [0, 2, 28, 40, 44], [1, 3, 21, 25, 27], [2, 4, 20], [3, 5, 6, 12, 16, 18, 19], [4], [4, 7, 8, 9],
     [6], [6], [6, 10], [9, 11], [10], [4, 13], [12, 14], [13, 15], [14], [4, 17], [16], [4], [4],
    [3], [2, 22], [21, 23], [22, 24], [23], [2, 26], [25], [2], [1, 29, 33], [28, 30, 31], [29], [29, 32], [31],
    [28, 34, 36, 38, 39], [33, 35], [34], [33, 37], [36], [33], [33], [1, 41, 42], [40], [40, 43], [42], [1, 45],
    [44], [0], [0], [0]]
w = [[4, 6, 0, 5, 15, 17, 18, 19, 10, 13, 6, 3, 1, 6, 0, 7, 18, 0, 7, 11, 6, 18, 11, 12, 3, 16, 4, 20, 0, 12, 7, 20,
    14, 5, 14, 20, 2, 19, 6, 17, 11, 11, 5, 5, 10, 17, 18, 12, 19],
    [17, 17, 14, 9, 15, 12, 5, 19, 13, 9, 2, 6, 0, 18, 10, 13, 10, 20, 5, 6, 12, 16, 19, 14, 14, 8, 12, 19, 18, 13,
    18, 17, 19, 15, 11, 17, 18, 13, 10, 18, 2, 7, 2, 7, 11, 13, 17, 12, 4],
    [15, 13, 17, 13, 8, 16, 8, 18, 8, 0, 4, 7, 17, 11, 9, 9, 11, 18, 13, 15, 8, 16, 5, 4, 9, 8, 11, 16, 6, 9, 0,
    13, 6, 3, 16, 14, 4, 7, 13, 16, 17, 12, 18, 11, 16, 10, 18, 5, 0],
    [18, 0, 1, 4, 20, 8, 7, 17, 19, 20, 13, 15, 4, 7, 9, 0, 10, 9, 2, 0, 5, 5, 15, 5, 9, 6, 0, 7, 11, 3, 7, 0, 1,
    20, 17, 6, 0, 16, 0, 13, 16, 17, 12, 18, 0, 15, 19, 19, 20],
    [12, 9, 15, 3, 17, 19, 2, 3, 0, 11, 10, 11, 4, 16, 19, 3, 17, 1, 19, 16, 13, 4, 1, 14, 10, 13, 4, 16, 19, 15,
    16, 10, 17, 10, 2, 2, 9, 3, 19, 3, 5, 3, 11, 17, 11, 8, 19, 5, 10],
    [1, 15, 18, 5, 0, 17, 17, 17, 13, 0, 17, 7, 11, 18, 14, 14, 5, 11, 14, 15, 18, 18, 3, 5, 20, 10, 12, 6, 20, 13,
    1, 14, 20, 17, 0, 13, 17, 12, 12, 19, 13, 19, 9, 20, 13, 1, 9, 4, 10],
    [16, 20, 12, 6, 18, 12, 9, 17, 8, 20, 0, 18, 0, 19, 0, 17, 6, 14, 16, 3, 1, 19, 8, 19, 12, 19, 17, 17, 0, 11,
    15, 13, 8, 13, 17, 0, 20, 9, 10, 7, 1, 8, 8, 17, 18, 12, 13, 15, 8],
    [15, 11, 13, 7, 10, 14, 0, 17, 18, 6, 16, 19, 10, 3, 20, 11, 2, 14, 8, 8, 15, 16, 19, 11, 5, 3, 18, 19, 5, 4,
    7, 3, 18, 2, 5, 9, 12, 13, 3, 13, 14, 3, 16, 7, 18, 14, 9, 8, 15],
    [17, 18, 15, 10, 0, 19, 0, 16, 17, 1, 4, 13, 17, 3, 13, 9, 16, 20, 1, 3, 8, 12, 13, 6, 5, 19, 12, 13, 4, 4, 1,
    4, 6, 9, 9, 5, 20, 0, 13, 9, 10, 13, 17, 15, 4, 11, 11, 20, 2],
    [9, 9, 2, 19, 2, 15, 7, 6, 17, 19, 10, 3, 19, 0, 1, 11, 17, 3, 17, 10, 4, 4, 17, 19, 16, 11, 14, 17, 20, 10, 9,
    11, 10, 16, 8, 0, 19, 5, 9, 7, 9, 7, 2, 1, 15, 0, 9, 11, 17]]

vsota = 0
for u,j in maxCycleTreeIndependentSet(T,w)[1]:
    vsota += w[u][j]

print(vsota == maxCycleTreeIndependentSet(T, w)[0], maxCycleTreeIndependentSet(T, w)[0])
