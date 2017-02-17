# -*- coding: utf-8 -*-
from .pomozne_funkcije import memo_potencialni_rekurzivci, DFS, nothing

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

    sl_kompat, legenda = memo_potencialni_rekurzivci(k)
    maxIndependSet = {}

    def w_podCikla(x, p):
        temp_t = 0
        for l in legenda[p]:
            temp_t += (w[l][x])
        return temp_t

    def maxNodeDrevesa(u,v): #postvisit funkcija
        for l in legenda: # gremo po možnih izbirah neodvisnih podmnožic v ciklu teh je ravno L(k)
            temp_weight =  w_podCikla(u,l) #teža izbire podmnožice l v ciklu
            izbraniOtroci = {}
            for y in DFSpotomci[u]: #prištejemo vsoto maximalnih vrednosti, ki jih lahko dobimo
                temp = max(maxIndependSet[y, l_komp] for l_komp in sl_kompat[l])
                temp_weight += temp[0] #prištejemo maksimalno možno težo potomcev pri taki izbiri (maximum kompatibilnih izbir v potomcih)
                izbraniOtroci.update(temp[2]) #dopišemo katere podmnožice smo izbrali pri vnukih
                izbraniOtroci[y] = temp[1] # in katero pri otrocih
            maxIndependSet[(u,l)] = (temp_weight,l,izbraniOtroci) # (max teža, izbira podmnožice, izbira podmnožic pri potomcih) za dano izbiro podmnožice na danem vozlišču drevesa T
        return True

    DFSpotomci = {i:[] for i in range(n)}
    def pripravidrevo(u, v): #previsit funkcija
        if v is not None:
            DFSpotomci[v].append(u)
        return True

    DFS(T,[0],pripravidrevo,maxNodeDrevesa)

    (c,L0,razpored) = max([maxIndependSet[0,l] for l in legenda]) #iz seznama izbire na korenu in seznamov izbire na potomcih korena samo še izvemo katera vozlišča imamo v naši neodvisni množici vozlišč
    s = [(l,0) for l in legenda[L0]]
    for drevo in razpored:
        for cikelj in legenda[razpored[drevo]]:
            s.append((cikelj, drevo))
    return (c,s)