# -*- coding: utf-8 -*-
from .dfs import DFS
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

    def getSubsets(k):
        """ Vrne vse možne podmnožice k elementov, predstavljene v binarnem zapisu, kjer '1' na j-tem mestu predstavlja
        da je element na j-tem mestu v množici. Izloči množice, kjer sta dve '1'-ki sosednji ali na prvem in zadnjem
        mestu. """
        subsets = []
        for i in range(2**k):
            binary = bin(i)[2:]
            if len(binary) < k:
                binary = '0' * (k - len(binary)) + binary
            first = binary[0]
            last = binary[-1]
            if first == '1' and last == '1':
                continue
            prev = first
            subset_ok = True
            for b in binary[1:]:
                if prev == '1' and prev == b:
                    subset_ok = False
                    break
                else:
                    prev = b
            if subset_ok:
                subsets.append(i)
        return subsets

    def getCompatibileSubsets(subsets):
        """ Vrne slovar kompatibilnih podmnožic za vsako izmed podmnožic. """
        compatible = dict()
        for subset in subsets:
            compatible[subset] = []
            for s in subsets:
                if subset & s == 0:
                    compatible[subset].append(s)
        return compatible

    def getCycleWeight(v, subset):
        """ Vrne vsoto tistih uteži cikla na mestu 'v' v drevesu, kjer je '1' v binarnem zapisu spremenljivke
        'subset'. """
        weight = 0
        binary = bin(subset)[2:]
        if len(binary) < k:
            binary = '0' * (k - len(binary)) + binary
        for i, b in enumerate(binary):
            if b == '1':
                weight += w[i][v]
        return weight

    subsets = getSubsets(k)  # Ustvari vse možne podmnožice
    compatible = getCompatibileSubsets(subsets)  # Ustvari slovar vseh kompatibilnih podmnožic za vse podmnožice
    # Za vsako vozlišče imamo slovar, kjer je ključ neka neodvisna podmnožica cikla in vrednost največje teža, ki jo
    # lahko dobimo s tako podmnožico cikla
    vozlisce_max = []
    for i in range(n):
        vozlisce_max.append(dict())

    def postvisit(u, v=None):
        sinovi_u = T[u][:]      # Kopija povezav iz vozlišča u
        if v is not None:
            sinovi_u.remove(v)  # Če nismo v korenu drevesa, odstranimo očeta, da lahko iteriramo le po sinovih
        for subset in subsets:
            tempWeight = getCycleWeight(u, subset)
            son_used = []  # Katere elemente smo uporabili na ciklu za vsakega sina
            # Za dano neodvisno podmnožico cikla, prištejemo največje vrednosti sinov pri kompatibilnih podmnožicah
            for s in sinovi_u:
                maxSon = - float("inf")
                son = None
                for c in compatible[subset]:
                    maxC = vozlisce_max[s][c][0]
                    if maxC > maxSon:
                        maxSon = maxC
                        son = c
                tempWeight += maxSon
                son_used.append((s, son))
            vozlisce_max[u][subset] = (tempWeight, son_used)
        return True

    # Z DFS-jem in funkcijo postvisit seznam vozlisce_max izpolnjujemo od spodaj navzgor, da imamo potomce trenutnega
    # vozlisca vedno ze izracunane.
    DFS(T, roots=[0], postvisit=postvisit)
    maxWeight = - float("inf")
    rootCycle = None  # Podmnozica cikla v korenu drevesa
    # Preverimo maksimalno tezo za vse ustrezne podmnozice cikla v korenu drevesa in poiscemo najvecjo.
    for subset in vozlisce_max[0].keys():
        weight = vozlisce_max[0][subset][0]
        if weight > maxWeight:
            maxWeight = weight
            rootCycle = subset
    cycles = [None] * n
    cycles[0] = rootCycle
    vertices = []
    # Preberemo katero podmnozico cikla smo uporabili v vsakem vozliscu drevesa
    for v in range(0, n):
        for u, cycle in vozlisce_max[v][cycles[v]][1]:
            cycles[u] = cycle
        binary = bin(cycles[v])[2:]
        if len(binary) < k:
            binary = '0' * (k - len(binary)) + binary
        for i, b in enumerate(binary):
            if b == '1':
                vertices.append((i, v))
    return maxWeight, vertices
