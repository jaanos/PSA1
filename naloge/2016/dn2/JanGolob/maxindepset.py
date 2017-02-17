# -*- coding: utf-8 -*-
from .pomozne_funkcije import potencialni_rekurzivci, DFS, nothing

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

    sl_kompat, legenda = potencialni_rekurzivci(k)
    maxIndependSet = {}

    def w_podCikla(x, p):
        temp_t = 0
        for l in legenda[p]:
            temp_t += (w[l][x])
        return temp_t

    def maxNodeDrevesa(u,v):
        for l in legenda: # gremo po možnih izbirah neodvisnih podmnožic v ciklu
            temp_weight =  w_podCikla(u,l)
            izbraniOtroci = {}
            for y in DFSpotomci[u]: #prištejemo vsoto maximalnih vrednosti, ki jih lahko dobimo
                temp = max(maxIndependSet[y, l_komp] for l_komp in sl_kompat[l])
                temp_weight += temp[0]
                izbraniOtroci.update(temp[2])
                izbraniOtroci[y] = temp[1]
            maxIndependSet[(u,l)] = (temp_weight,l,izbraniOtroci)
        return True

    DFSpotomci = {i:[] for i in range(n)}
    def pripravidrevo(u, v):
        if v is not None:
            DFSpotomci[v].append(u)
        return True

    DFS(T,[0],pripravidrevo,maxNodeDrevesa)

    (c,L0,razpored) = max([maxIndependSet[0,l] for l in legenda])
    s = [(l,0) for l in legenda[L0]]
    for drevo in razpored:
        for cikelj in legenda[razpored[drevo]]:
            s.append((cikelj, drevo))
    return (c,s)