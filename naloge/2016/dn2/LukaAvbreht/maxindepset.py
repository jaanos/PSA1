# -*- coding: utf-8 -*-
import sys
#from .otherFunctions import *
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

    def vrednost_cikla_na_nivoju(cikel,nivo):
        res = 0
        nivo = int(nivo)
        for i in cikel:
            if i == '1':
                res+= w[int(i)][nivo]
        return res

    vsi_mozni_cikli = all_valid_cycles(n)

    memo = dict()
    Graf_resitev = list()
    Kajsmozbral = set()


    def max_value_of_tree_with_root_0(valid_cycles):
        """Function that Recursivly returns the value of maximal independent sub group of cartesic product od cycle and tree"""

        def recursive_tree_funct(n,cycle_type):
            """Recursive function that calculates the max value of a tree with certain cycle type as a root"""
            if(n,cycle_type) in memo:
                return memo[(n,cycle_type)]

            vrednost_voz = vrednost_cikla_na_nivoju(cycle_type,n)
            racun = (vrednost_voz,frozenset([(n,cycle_type)]))
            if len(T[n]) == 1: # means that n is a leaf of a tree
                memo[(n,cycle_type)] = racun
                return racun
            for i in T[n]:
                if i > n: # So we only look for children :D
                    prim = list_primernih_otrok(cycle_type)
                    maxi = 0
                    izbral = list()
                    for j in prim:
                        trvr = recursive_tree_funct(i,j)
                        if trvr[0] > maxi:
                            maxi = trvr[0]
                            nov = [(i,j)]
                            nov + list(trvr[1])
                            izbral = nov
                    vrednost_voz += maxi
            memo[(n,cycle_type)] = (vrednost_voz,frozenset(izbral))
            return (vrednost_voz,frozenset(izbral))
        maxi = 0
        zbr = None
        for i in valid_cycles:
            trvr = recursive_tree_funct(0,i)
            if trvr[0] > maxi:
                maxi = trvr[0]
                zbr = trvr[1]
        return maxi,zbr

    zacetni = all_valid_cycles(k)
    res = max_value_of_tree_with_root_0(zacetni)
    print(res)
    print(Kajsmozbral)

    graf = [(0, 0), (2, 0), (1, 1), (3, 1), (0, 3), (2, 3), (0, 4), (2, 4), (1, 5), (3, 5), (1, 6), (3, 6), (1, 7), (3, 7), (1, 8), (3, 8), (0, 9), (2, 9), (0, 10), (2, 10), (0, 11), (2, 11), (1, 12), (3, 12), (0, 13), (2, 13)]
    #return res


















    # def max_independes_subgorup_of_cycle_and_tree(graf,drev):
    #     if graf == frozenset():
    #         return 0
    #     if drev == frozenset():
    #         return 0
    #     if (graf,drev) in memo:
    #         return memo[(graf,drev)]
    #     cikel = list(graf)
    #     drevo = list(drev)
    #     vozlisceC = cikel[0]
    #     vozlisceD = drevo[0]
    #     G_brez = frozenset(cikel[1:])
    #     G_z = frozenset(cikel[2:-1])
    #     drevo.pop(0)
    #     D_brez = frozenset(drevo)
    #     for i in T[vozlisceD]:
    #         try:
    #             drevo.remove(i)
    #         except:
    #             pass
    #     D_z = frozenset(drevo)
    #
    #     vred_vozl = w[vozlisceC][vozlisceD]
    #
    #     # prva vrednost je ce se odlocmo vzet vozlisce
    #     # damo vrednost vozlisca + rekurzivni kilic na drevesu spodi+ sosedni dve brez tega vozlisca v drevesu + preostali del dreves
    #     A = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_z)
    #     memo[(frozenset([vozlisceC]),D_z)] = A
    #
    #     if len(cikel) > 3:
    #         sosed1 = cikel[1]
    #         sosed2 = cikel[-1]
    #         B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
    #         memo[(frozenset([sosed1]),D_brez)] = B
    #         C = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed2]),D_brez)
    #         memo[(frozenset([sosed2]),D_brez)] = C
    #         D = max_independes_subgorup_of_cycle_and_tree(G_z,drev)
    #         memo[(G_z,drev)] = D
    #     elif len(cikel) == 3:
    #         sosed1 = cikel[1]
    #         sosed2 = cikel[-1]
    #         B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
    #         memo[(frozenset([sosed1]),D_brez)] = B
    #         C = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed2]),D_brez)
    #         memo[(frozenset([sosed2]),D_brez)] = C
    #         D = 0
    #     elif len(cikel) == 2:
    #         sosed1 = cikel[1]
    #         B = max_independes_subgorup_of_cycle_and_tree(frozenset([sosed1]),D_brez)
    #         memo[(frozenset([sosed1]),D_brez)] = B
    #         C = 0
    #         D = 0
    #     else:
    #         B = 0
    #         C = 0
    #         D = 0
    #
    #     maxtren1 = vred_vozl + A + B + C + D
    #
    #     #tuki se odlocimo da ne damo vozlisca v nas graf resitve
    #     #torje moramo rekurzivni klic izvesti na poddrevesu pri fiksenm vozlisce + na vseh ostalih drevesih, pri vseh ostalih ciklih
    #     if len(cikel) == 1:
    #         E = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_brez)
    #         memo[(frozenset([vozlisceC]),D_brez)] = E
    #         F = 0
    #     else:
    #         E = max_independes_subgorup_of_cycle_and_tree(frozenset([vozlisceC]),D_brez)
    #         memo[(frozenset([vozlisceC]),D_brez)] = E
    #         F = max_independes_subgorup_of_cycle_and_tree(G_brez,drev)
    #         memo[(G_brez,drev)] = F
    #     maxtren2 = E + F
    #
    #     if maxtren1 > maxtren2:
    #         Graf_resitev.add((vozlisceC,vozlisceD))
    #         return maxtren1
    #     return maxtren2
    #
    # Vred_res = max_independes_subgorup_of_cycle_and_tree(frozenset(range(k)),frozenset(range(n)))

    ##### DEl tihis part


def primeren_otrok(parent,child):
    """It returns true if the ciycle child can ba a neighbour cycle of parent (input is in string in binary)"""
    k = len(parent)
    assert k == len(child), \
        "Parent and child must be of same size"
    for i in range(k):
        if parent[i] == child[i] == 1:
            return False
    return True

def list_primernih_otrok(parent):
    """Returns the list of all valid children of a parent as a list of binary numbers(strings)"""
    assert valid_cycle(parent) == True, "Parent is not the valid cycle"
    if parent[0] == '1':
        res = ['0']
        k = 1
    else:
        res = ['1','0']
        k = 2
    for i in parent[1:]:
        tren = list()
        if i =='1':
            for j in range(k):
                tren.append(res[j]+'0')
        else:
            dif = 0
            for j in range(k):
                if res[j][-1]=='1':
                    tren.append(res[j]+'0')
                    dif += 1
                else:
                    tren.append(res[j]+'1')
                    tren.append(res[j]+'0')
            k = k*2-dif
        res = tren
    tren = list()
    for i in res:
        if valid_cycle(i):
            tren.append(i)
    return tren

def valid_cycle(cycle):
    """Returns True if a cycle is valid and False othervise (Cycle is valid ifi it has an independent subgroup of ones)"""
    for i in range(len(cycle)-1):
        if cycle[i] == '1':
            if cycle[i-1] != '0' or cycle[i+1] != '0':
                return False
    return True

def are_neighbours(a,b,T):  # aLso returns false if you compere by
    """Returns True if two nodes are neighbours, otherwise returns False"""
    x,u = a[0],a[1]
    y,v = b[0],b[1]
    Cikelsos = abs((x-y)%k)
    if u == v and Cikelsos <= 1:
        return True
    Drevosos = u in T[v]
    if Cikelsos == 0 and Drevosos:
        return True
    return False

def all_valid_cycles(n):
    """Returns the list of all valid cycles of length n"""
    return list_primernih_otrok('0'*n)

T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],[3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
     [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],[5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]
maxCycleTreeIndependentSet(T,w)