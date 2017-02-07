# -*- coding: utf-8 -*-
import sys
from .otherFunctions import *
sys.setrecursionlimit(100000)

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
    k = len(w)   #k is the len of the cycle
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])
    # raise NotImplementedError("Naredi sam!")

    memo = dict()
    Graf_resitev = set()

    def max_independes_subgorup_of_cycle_and_tree(graf,drev):
        if graf == frozenset():
            return 0
        if drev == frozenset():
            return 0
        if (graf,drev) in memo:
            return memo[(graf,drev)]
        cikel = list(graf)
        drevo = list(drev)
        vozlisceC = cikel[0]
        vozlisceD = drevo[0]
        G_brez = frozenset(cikel[1:])
        G_z = frozenset(cikel[2:-1])
        drevo.pop(0)
        D_brez = frozenset(drevo)
        for i in T[vozlisceD]:
            try:
                drevo.remove(i)
            except:
                pass
        D_z = frozenset(drevo)

        vred_vozl = w[vozlisceC][vozlisceD]

        # prva vrednost je ce se odlocmo vzet vozlisce
        # damo vrednost vozlisca + rekurzivni kilic na drevesu spodi+ sosedni dve brez tega vozlisca v drevesu + preostali del dreves
        A = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_z)
        memo[(frozenset([vozlisceC]),D_z)] = A

        if len(cikel) > 3:
            sosed1 = cikel[1]
            sosed2 = cikel[-1]
            B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
            memo[(frozenset([sosed1]),D_brez)] = B
            C = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed2]),D_brez)
            memo[(frozenset([sosed2]),D_brez)] = C
            D = max_independes_subgorup_of_cycle_and_tree(G_z,drev)
            memo[(G_z,drev)] = D
        elif len(cikel) == 3:
            sosed1 = cikel[1]
            sosed2 = cikel[-1]
            B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
            memo[(frozenset([sosed1]),D_brez)] = B
            C = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed2]),D_brez)
            memo[(frozenset([sosed2]),D_brez)] = C
            D = 0
        elif len(cikel) == 2:
            sosed1 = cikel[1]
            B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
            memo[(frozenset([sosed1]),D_brez)] = B
            C = 0
            D = 0
        else:
            B = 0
            C = 0
            D = 0

        maxtren1 = vred_vozl + A + B + C + D

        #tuki se odlocimo da ne damo vozlisca v nas graf resitve
        #torje moramo rekurzivni klic izvesti na poddrevesu pri fiksenm vozlisce + na vseh ostalih drevesih, pri vseh ostalih ciklih
        if len(cikel) == 1:
            E = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_brez)
            memo[(frozenset([vozlisceC]),D_brez)] = E
            F = 0
        else:
            E = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_brez)
            memo[(frozenset([vozlisceC]),D_brez)] = E
            F = max_independes_subgorup_of_cycle_and_tree(G_brez,drev)
            memo[(G_brez,drev)] = F
        maxtren2 = E + F

        if maxtren1 > maxtren2:
            Graf_resitev.add((vozlisceC,vozlisceD))
            return maxtren1
        return maxtren2

    Vred_res = max_independes_subgorup_of_cycle_and_tree(frozenset(range(k)),frozenset(range(n)))
    print(Vred_res)
    print(Graf_resitev)
    print(list(Graf_resitev))
    res = ([(0, 0), (2, 0), (1, 1), (3, 1), (0, 3), (2, 3), (0, 4), (2, 4), (1, 5), (3, 5), (1, 6), (3, 6), (1, 7), (3, 7), (1, 8), (3, 8), (0, 9), (2, 9), (0, 10), (2, 10), (0, 11), (2, 11), (1, 12), (3, 12), (0, 13), (2, 13)])
    print(res)
    print(list(Graf_resitev)==res)




    ##### DEl tihis part

T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],[3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
     [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],[5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]
maxCycleTreeIndependentSet(T,w)