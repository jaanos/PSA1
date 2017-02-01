# -*- coding: utf-8 -*-

def maxCycleTreeIndependentSet(T, w):
    T = [[1, 2], [0], [0]]
    w = [[1, 1, 1, 1],
         [2, 2, 2, 2],
         [3, 3, 3, 3],
         [4, 4, 4, 4]]
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
    print("nekaj dela in ljubljana je najlepse mesto")

    # pripravimo si graf (oz matriko sosedov, kjer i-ti stolpec
    # in j-ta vrstica predstavljata seznam sosedov i-tega
    # elementa v drevesu in j -tega elementa v ciklu),
    # zadnja vrednost pa pove, če je element v grafu ali ne

    celotenGraf = []
    for nadstropje in range(k):
        vozlisca = []
        for vozlisce in range(n):
            a = (nadstropje + 1) % k
            b = (nadstropje - 1) % k
            sosedje = [(vozlisce, a, 1)]
            sosedje += [(vozlisce, b, 1)]
            for sosed in T[vozlisce]:
                sosedje += [(sosed, nadstropje, 1)]
            vozlisca += [sosedje]
        celotenGraf += [vozlisca]

    return "Eva"

