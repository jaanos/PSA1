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

    celotenGraf = [[]*n]*k
    for nadstropje in range(k):
        for vozlisce in range(n):
            for sosed in T[vozlisce]:
                celotenGraf[nadstropje][vozlisce] += [(sosed, nadstropje)]
            a = (nadstropje + 1) % k
            b = (nadstropje -1 ) % k
            celotenGraf[nadstropje][vozlisce] += [(vozlisce, a)]
            celotenGraf[nadstropje][vozlisce] += [(vozlisce, b)]
    print(celotenGraf)

    return "Eva"

