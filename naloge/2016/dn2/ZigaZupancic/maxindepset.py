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

    def getSubsets(k):
        """ Vrne vse možne podmnožice k elementov, predstavljene v binarnem zapisu, kjer '1' na j-tem mestu predstavlja
        da je element na j-tem mestu v množici. Izloči množice, kjer sta dve '1'-ki sosednji ali na prvem in zadnjem
        mestu. """
        subsets = []
        for i in range(2**k):
            binary = bin(i)[2:]
            if len(binary) < k:
                binary = '0' * (k - len(binary)) + binary
            first = binary[0]
            last = binary[-1]
            if first == '1' and last == '1':
                continue
            prev = first
            subset_ok = True
            for b in binary[1:]:
                if prev == '1' and prev == b:
                    subset_ok = False
                    break
                else:
                    prev = b
            if subset_ok:
                subsets.append(i)
        return subsets

    def getCompatibileSubsets(subsets):
        """ Vrne slovar kompatibilnih podmnožic za vsako izmed podmnožic. """
        compatible = dict()
        for subset in subsets:
            compatible[subset] = []
            for s in subsets:
                if subset & s == 0:
                    compatible[subset].append(s)
        return compatible

    subsets = getSubsets(k)
    compatible = getCompatibileSubsets(subsets)
