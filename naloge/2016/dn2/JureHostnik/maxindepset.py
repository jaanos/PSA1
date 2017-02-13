# -*- coding: utf-8 -*-
T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],
     [3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
     [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],
     [5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]

def maxCycleIndependentSet(w, index = None, k = None):
    if k is None:
        k = len(w)
    if index is None:
        index = range(k)
    if len(w) == 1:
##        c = max(w)
##        s = [(index[w.index(c)], 0)]
##        return (c[0], s)
        return (w[0][0], [(index[0], 0)])
    else:
        r = []
        for i in index:
            c = w[index.index(i)][0]
            s = [(i, 0)]
            o = []
            ind = []
            for j in index:
                if (j-i)%k != 1 and (j-i)%k != k-1 and i != j:
                    o.append(w[index.index(j)])
                    ind.append(j)
            p = maxCycleIndependentSet(o, ind, k)
            r.append((c + p[0], s + p[1]))
        return max(r) if r != [] else (0, [])
        
##        return [
##            [w[i][0] + maxCycleIndependentSet([w[j] for j in range(k) if (j-i)%k != 1 and (j-i)%k != 3 and i != j])[0],
##             [(w.index(w[i]), 0)] + maxCycleIndependentSet([w[j] for j in range(k) if (j-i)%k != 1 and (j-i)%k != 3 and i != j])[1]] for i in range(k)]

def maxTreeIndependentSet(T, w):
    if n == 0:
        return (0, [])
    elif n == 1:
        return (w[0][0], [(0, 0)])
    else:
        return max(
            w[0][0] + maxTreeIndependentSet(T, w)
            )

def independentSets(k, index = None, n = None):
    if n is None:
        n = k // 2
    if index is None:
        index = range(k)
    s = []
    if k <= 0:
        return [[]]
    elif k == 1:
        return [[0], [1]]
    elif k == 2:
        return [[0, 0], [0, 1], [1, 0]]
    else:
        for m in independentSets(k-1, index = None, n = None):
            s.append([0] + m)
        for m in independentSets(k-2, index = None, n = None):
            s.append([1, 0] + m)
        return s

def cycleIndependentSets(k, index = None, n = None):
    if n is None:
        n = k // 2
    if index is None:
        index = range(k)
    s = []
    if k <= 0:
        return [[]]
    if k == 1:
        return [[0], [1]]
    elif k == 2:
        return [[0, 0], [0, 1], [1, 0]]
    elif k == 3:
        return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]]
    else:
        for m in independentSets(k-1, index = None, n = None):
            s.append([0] + m)
        for m in independentSets(k-3, index = None, n = None):
            s.append([1, 0] + m + [0])
        return s

def odstejEna(T):
##    [i-1 for i in s if i != 0] for j, s in enumerate(T[1:]) if s != [0] else [j]
##    D = []
##    for j, s in enumerate(T[1:]):
##        if s != [0]:
##            D.append([i-1 for i in s if i != 0])
##        else:
##            D.append([j])
    return [[i-1 for i in s if i != 0] if s != [0] else [j] for j, s in enumerate(T[1:])]
    
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
##    raise NotImplementedError("Naredi sam!")
    
    elif n == 1:
        return maxCycleIndependentSet(w)
    else:
        max()
