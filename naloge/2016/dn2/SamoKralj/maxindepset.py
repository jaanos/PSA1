# -*- coding: utf-8 -*-
from time import time
from random import randint

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

    memo = dict()

    mask = generiraj_bitmask(k)

    def find_max(koren, indeks_vozlisca):
        if (koren, indeks_vozlisca) in memo:
            return memo[koren, indeks_vozlisca]
        else:
            maksimum = 0
            vozlisca = tuple()
            v = indeks_vozlisca
            for vzorec in mask[koren]:
                teza, vozl = vrednost(vzorec, w, k, v)
                for i in range(indeks_vozlisca + 1, len(T)):
                    if i in T[v]:
                        teza_dodaj, vozl_dodaj = find_max(vzorec, i)
                        teza += teza_dodaj
                        vozl += vozl_dodaj
                if teza > maksimum:
                    maksimum = teza
                    vozlisca = vozl
                if teza == maksimum and len(vozl) > len(vozlisca):
                    maksimum = teza
                    vozlisca = vozl
            memo[koren, indeks_vozlisca] = (maksimum,vozlisca)
            return maksimum, vozlisca
    return find_max(0,0)

def generiraj_bitmask(k):
    """
    Vrne vse bitmaske dolžine k, za katera velja, da nobeni dve enici
    nista sosednji.
    """
    assert k >= 2, 'Cikel mora biti dolžine vsaj 2.'
    mask = []
    for i in range(2**k):
        zapis = binarno(i, k)
        zapis = zapis
        flag = True
        for j in range(len(zapis) - 1):
            if zapis[j] == 1 and zapis[j+1] == 1:
                flag = False
                break
        if zapis[0] == 1 and zapis[-1] == 1:
            flag = False
        if flag:
            mask.append(i)

    povezave = {i : [k for k in mask if (i & k) == 0] for i in mask}
    return povezave

def binarno(n, k):
    """
    Vrne binaren zapis na k mest.
    """
    assert n < 2**k, 'Število je preveliko'
    vrni = []
    while n > 0:
        vrni.append(n%2)
        n = n//2
    return [0]*(k - len(vrni)) + list(reversed(vrni))

def vrednost(mask, w, k, vozlisce):
    """
    Vrne tezo cikla na vozliscu drevesa vozlisce in bitmasko mask.
    """
    zapis = binarno(mask, k)
    teza = 0
    vozlisca_grafa = tuple()
    for i in range(k):
        teza += zapis[i]*w[i][vozlisce]
        if zapis[i] == 1:
            vozlisca_grafa += ((i, vozlisce),)
    return teza, vozlisca_grafa

def generateTreeGraph(nodes, oznaka_start):
    """
    Generira povezave drevesa z nodes + 1 vozlisci
    """
    if nodes == 0:
        return []
    else:
        povezave = []
        dodaj = oznaka_start + 1
        while nodes > 0:
            u = randint(1, nodes)
            povezave.append([oznaka_start, dodaj])
            povezave.extend(generateTreeGraph(u - 1, dodaj))
            dodaj += u
            nodes -= u
        return povezave

def generateTree(stevilo_vozlisc):
    """
    Generira drevo z stevilo_vozlisc vozlisci.
    """
    povezave = generateTreeGraph(stevilo_vozlisc - 1, 0)
    G = [[] for i in range(stevilo_vozlisc)]
    for u, v in povezave:
        G[u].append(v)
        G[v].append(u)
    return G
        
    
    


























    
