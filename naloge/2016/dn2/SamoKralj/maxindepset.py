# -*- coding: utf-8 -*-
from time import time

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

    vrstni_red = uredi_po_plasteh(T)

    def find_best_set(prepovedani, cikel, drevo):
        if cikel == k:
            return 0, []
        elif (frozenset(prepovedani), cikel, drevo) in memo:
            return memo[frozenset(prepovedani), cikel, drevo]
        elif drevo == len(vrstni_red):
            return find_best_set(prepovedani, cikel + 1, 0)
        else:
            v = vrstni_red[drevo]
            nova_prep = prepovedani.copy()
            nova_prep.add((cikel, drevo))
            best, best_solution = find_best_set(nova_prep, cikel, drevo + 1)
            if (cikel, v) not in prepovedani:
                nova_prep = prepovedani.copy()
                nova_prep.add((cikel, v))
                for u in T[v]:
                    nova_prep.add((cikel, u))
                nova_prep.add(((cikel-1) % k, v))
                nova_prep.add(((cikel+1) % k, v))
                S, vozlisca = find_best_set(nova_prep, cikel, drevo + 1)
                if w[cikel][v] + S > best:
                    best = w[cikel][v] + S
                    best_solution = [(cikel, v)]
                    for par in vozlisca:
                        best_solution.append(par)
            memo[(frozenset(prepovedani), cikel, drevo)] = best, best_solution
            return best, best_solution
    cas = time()
    res2 = find_best_set(set(),0,0)
    time2 = time() - cas
    print('Prejsni algoritem resi nalogo v {0}'.format(time2))
    return res2

def maxCycleTreeIndependentSet2(T, w):
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

    vrstni_red = uredi_po_plasteh(T)

    def find_max(koren, indeks_vozlisca):
        if (koren, indeks_vozlisca) in memo:
            return memo[koren, indeks_vozlisca]
        else:
            maksimum = 0
            vozlisca = tuple()
            v = vrstni_red[indeks_vozlisca]
            for vzorec in mask[koren]:
                teza, vozl = vrednost(vzorec, w, k, v)
                for i in range(indeks_vozlisca + 1, len(vrstni_red)):
                    if vrstni_red[i] in T[v]:
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

def uredi_po_plasteh(T):

    ozina = len(T)*[None]
    ozina[0] = 0
    obiskani = len(T) - 1

    iskanje = [0]
    while obiskani > 0:
        nova_plast = []
        for v in iskanje:
            for u in T[v]:
                if ozina[u] is None:
                    ozina[u] = ozina[v] + 1
                    nova_plast.append(u)
                    obiskani -= 1
        iskanje = nova_plast

    vrstni_red = [(k, i) for i,k in enumerate(ozina)]
    vrstni_red.sort()
    vrstni_red = [i for k,i in vrstni_red]
    return vrstni_red
        
    
    


























    
