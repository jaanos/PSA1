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

    memo2 = dict()
    
    def find_best(z_v, prejsni_v, tren_v, drevo_i, cikel_i):
        if cikel_i == k:
            return 0, []
        elif (frozenset(z_v), frozenset(prejsni_v), frozenset(tren_v), drevo_i, cikel_i) in memo2:
            return memo2[(frozenset(z_v), frozenset(prejsni_v), frozenset(tren_v), drevo_i, cikel_i)]
        elif drevo_i == len(vrstni_red):
            return find_best(z_v, tren_v, set(), 0, cikel_i + 1)
        else:
            v = vrstni_red[drevo_i]
            if cikel_i == k - 1:
                nova_tren = tren_v.copy()
                best, best_sol = find_best(z_v, prejsni_v, nova_tren, drevo_i + 1, cikel_i)
                if v not in prejsni_v and v not in z_v:
                    znak = True
                    for u in T[v]:
                        if u in tren_v:
                            znak = False
                            break
                    if znak:
                        nova_tren2 = tren_v.copy()
                        nova_tren2.add(v)
                        b2, best_sol2 = find_best(z_v, prejsni_v, nova_tren2, drevo_i + 1, cikel_i)
                        b2 += w[cikel_i][v]
                        if b2 > best:
                            best = b2
                            best_sol = best_sol2 + [[cikel_i, v]]
                memo2[(frozenset(z_v), frozenset(prejsni_v), frozenset(tren_v), drevo_i, cikel_i)] = best, best_sol
                return best, best_sol
            elif cikel_i == 0:
                nova_tren = tren_v.copy()
                nova_zv = z_v.copy()
                best, best_sol = find_best(nova_zv, prejsni_v, nova_tren, drevo_i + 1, cikel_i)
                if v not in prejsni_v:
                    znak = True
                    for u in T[v]:
                        if u in tren_v:
                            znak = False
                            break
                    if znak:
                        nova_tren2 = tren_v.copy()
                        nova_tren2.add(v)
                        nova_zv = z_v.copy()
                        nova_zv.add(v)
                        b2, best_sol2 = find_best(nova_zv, prejsni_v, nova_tren2, drevo_i + 1, cikel_i)
                        b2 += w[cikel_i][v]
                        if b2 > best:
                            best = b2
                            best_sol = best_sol2 + [[cikel_i, v]]
                memo2[(frozenset(z_v), frozenset(prejsni_v), frozenset(tren_v), drevo_i, cikel_i)] = best, best_sol
                return best, best_sol
            else:
                nova_tren = tren_v.copy()
                best, best_sol = find_best(z_v, prejsni_v, nova_tren, drevo_i + 1, cikel_i)
                if v not in prejsni_v:
                    znak = True
                    for u in T[v]:
                        if u in tren_v:
                            znak = False
                            break
                    if znak:
                        nova_tren2 = tren_v.copy()
                        nova_tren2.add(v)
                        b2, best_sol2 = find_best(z_v, prejsni_v, nova_tren2, drevo_i + 1, cikel_i)
                        b2 += w[cikel_i][v]
                        if b2 > best:
                            best = b2
                            best_sol = best_sol2 + [[cikel_i, v]]
                memo2[(frozenset(z_v), frozenset(prejsni_v), frozenset(tren_v), drevo_i, cikel_i)] = best, best_sol
                return best, best_sol

    cas = time()
    resitev = find_best(set(), set(), set(), 0, 0)
    time1 = time() - cas
    cas = time()
    res2 = find_best_set(set(),0,0)
    time2 = time() - cas
    print('Izboljšan algoritem reši nalogo v {0}'.format(time1))
    print(resitev, len(memo2))
    print('Prejsni algoritem resi nalogo v {0}'.format(time2))
    print(res2, len(memo))
    return resitev

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
