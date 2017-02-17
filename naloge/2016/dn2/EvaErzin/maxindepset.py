# -*- coding: utf-8 -*-
from .DFS import DFS, nothing


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


    def independentCycleSubsets(k):

        """ Vrne neodvisne podmnožice cikla s k elementi predstavljene v binarnem zapisu. """


        subsets = []
        ind = 0
        for i in range(2**k):
            curr = bin(i)[2:]
            curr = '0' * (k - len(curr)) + curr
            if curr[0] == '1' and curr[-1] == '1' : continue
            flag = True
            for j in range(k-1):
                if curr[j] == '1' and curr[j+1] == '1' : flag = False
            if flag:
                subsets.append((curr, i))
                ind += 1
        return subsets

    def compatibleDict(subsets):

        """ Vrne slovar, ki vsebuje sezname kompatibilnih neodvisnih množic za vsako izmed množic v seznamu"""

        compatibles = {}
        for (i,set) in subsets:
            compatibles[i] = []
            for (j, subset) in subsets:
                if set[1] & subset[1] == 0:
                    compatibles[i].append(j)
        return compatibles

    def setWeight(set, m):

        """ Vrne težo neodvisne podmnožice v ciklu, ki je v produktu na m-tem mestu v drevesu."""

        weight = 0
        for i in range(len(set)):
            if set[i] == '1': weight += w[i][m]
        return weight


    ## Najprej ustvarimo seznam vseh možnih neodvisnih podmnožic cikla s k elementi, ga oštevilčimo in nato iz tega
    ## generiramo še slovar vseh kompatibilnih podmnožic za vsako izmed njih
    sets = independentCycleSubsets(k)
    sets = list(enumerate(sets))
    n_sets = len(sets)
    compatibles = compatibleDict(sets)

    ## Slovar, ki za vsak element drevesa T vsebuje slovar, ki nam pove maksimalno ceno,
    ## ki jo lahko dosežemo z uporabo vsake izmed neodvisnih podmnožic na tem mestu in podmnožice,
    ## ki smo jih za to porabili na prejšnjih nivojih
    max_weights = {v: {i: (- float('inf'), []) for i in range(n_sets)} for v in range(n)}

    def postvisit(u, v):
        for (i, sub) in sets:
            weight = setWeight(sub[0], u)
            used_children = []
            for t in T[u]:
                if t == v:
                    continue
                maxi = -1 * float('inf')
                children = []
                for j in compatibles[i]:
                    w = max_weights[t][j][0]
                    if w > maxi:
                        maxi = w
                        children = max_weights[t][j][1]
                used_children += children
                weight += maxi
            max_weights[u][i] = (weight, [(u, i)] + used_children)
        return True


    DFS(T, postvisit=postvisit)

## Sestavimo končno množico

    final_set = []

    max_weight, sez = max(max_weights[0][k] for k in range(n_sets))

    for (u, i) in sez:
        set = sets[i][1][0]
        for j in range(k):
            if set[j] == '1':
                final_set.append((j, u))

    return (max_weight, final_set)



