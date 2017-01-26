# -*- coding: utf-8 -*-

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
    cnt = [0]

    def find_best_set(prepovedani, cikel, drevo):
        if cikel <= 0:
            print(cikel, drevo, len(memo), cnt)
        if cikel == k:
            return 0, []
        elif (frozenset(prepovedani), cikel, drevo) in memo:
            cnt[0] += 1
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

    resitev = find_best_set(set(), 0, 0)
    print(len(memo), cnt)
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
