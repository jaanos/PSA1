# -*- coding: utf-8 -*-

from time import clock

def independentSets(k):
    """
    Vrne seznam vseh neodvisnih množic dolžine k.
    """
    s = []
    if k <= 0:
        return [[]]
    elif k == 1:
        return [[0], [1]]
    elif k == 2:
        return [[0, 0], [0, 1], [1, 0]]
    else:
        for m in independentSets(k-1):
            s.append([0] + m)
        for m in independentSets(k-2):
            s.append([1, 0] + m)
        return s

##def independentSets1(k):
##    """
##    Vrne seznam vseh neodvisnih množic dolžine k.
##    """
##    a = [[]]
##    b = [[0], [1]]
##    c = [[0, 0], [0, 1], [1, 0]]
##    if k <= 0:
##        return a
##    elif k == 1:
##        return b
##    elif k == 2:
##        return c
##    while k > 2:
##        s = []
##        for m in c:
##            s.append([0] + m)
##        for m in b:
##            s.append([1, 0] + m)
##        a, b, c = b, c, s
##        k -= 1
##    return c

def cycleIndependentSets(k):
    """
    Vrne seznam vseh neodvisnih množic v ciklu dolžine k.
    """
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
        for m in independentSets(k-1):
            s.append([0] + m)
        for m in independentSets(k-3):
            s.append([1, 0] + m + [0])
        return s

def independentNeighbours(s):
    """
    Vrne seznam vseh neodvisnih množic v ciklu dolžine k,
    ki so hkrati neodvisne od s.
    """
    k = len(s)
    n = []
    for i in cycleIndependentSets(k):
        for j, e in enumerate(i):
            if e*s[j] == 1:
                break
        else:
            n.append(i)
    return n

def decimate(T):
    """
    Vrne graf, ki ga dobimo, če grafu T odstranimo ničto vozlišče.
    """
    return [[i-1 for i in s if i != 0] if s != [0] else [j] for j, s in enumerate(T[1:])]

def subtrees(T, I = None):
    """
    Vrne seznam vseh poddreves drevesa T, ki imajo za koren sina korena T
    in dva seznama indeksov.
    """
    if len(T) == 1:
        return [], [], []
    s = [[] for b in T[0]]
    i = [[] for c in T[0]]
    for j, m in enumerate(decimate(T)):
        if j == 0:
            s[0].append(m)
            i[0].append(0)
        else:
            for k, t in enumerate([z for z in s if z != []]):
                for u in t:
                    if j in u:
                        t.append(m)
                        i[k].append(j)
                        break
                else:
                    try:
                        if s[k+1] == []:
                            s[k+1].append(m)
                            i[k+1].append(j)
                    except IndexError:
                        pass
    if I is None:
        I = [[v+1 for v in w] for w in i]
    else:
        I = [[I[v+1] for v in w] for w in i]
    return ([[[i[a].index(z) for z in y] for y in x] for a, x in enumerate(s)],
            [[v+1 for v in w] for w in i],
            I)
    
def maxCycleTreeIndependentSet(T, w, z = 0, i = None, I = None):
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
    else:
        m = []
        if i is None:
            i = cycleIndependentSets(k)
        S, A, I = subtrees(T, I)
        for s in i:
            c = 0
            v = []
            for j, e in enumerate(s):
                if e == 1:
                    c += w[j][0]
                    v.append((j, z))
            for y, t in enumerate(S):
                a = maxCycleTreeIndependentSet(t,
                                               [[u[v] for v in A[y]] for u in w],
                                               z = I[y][0],
                                               i = independentNeighbours(s),
                                               I = I[y])
                c += a[0]
                v += a[1]
            m.append((c, v))
        return max(m)

def test(T, w):
    t0 = clock()
    h = maxCycleTreeIndependentSet(T, w)
    t = clock()
    return t-t0
