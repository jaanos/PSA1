# -*- coding: utf-8 -*-
T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],
     [3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
     [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],
     [5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]

def maxCycleIndependentSet(w, index = None, k = None, z = 0):
    if k is None:
        k = len(w)
    if index is None:
        index = range(k)
    if len(w) == 1:
##        c = max(w)
##        s = [(index[w.index(c)], 0)]
##        return (c[0], s)
        return (w[0][0], [(index[0], z)])
    else:
        r = []
        for i in index:
            c = w[index.index(i)][0]
            s = [(i, z)]
            o = []
            ind = []
            for j in index:
                if (j-i)%k != 1 and (j-i)%k != k-1 and i != j:
                    o.append(w[index.index(j)])
                    ind.append(j)
            p = maxCycleIndependentSet(o, ind, k, z)
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

def independentNeighbours(s):
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
##    [i-1 for i in s if i != 0] for j, s in enumerate(T[1:]) if s != [0] else [j]
##    D = []
##    for j, s in enumerate(T[1:]):
##        if s != [0]:
##            D.append([i-1 for i in s if i != 0])
##        else:
##            D.append([j])
    return [[i-1 for i in s if i != 0] if s != [0] else [j] for j, s in enumerate(T[1:])]

def subtrees(T, I = None):
##    print(T)
##    print(I)
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
##                if t == []:
##                    l = k
##                    break
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
##    print(i)
##    print('----------------')
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
##    print(I)
##    print('............')
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
    
##    elif n == 1:
##        return maxCycleIndependentSet(w, z = z)
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
            
##            print(T)
##            print(S)
##            print(I)
##            print('-----')
            for y, t in enumerate(S):
##                print(I[y])
                a = maxCycleTreeIndependentSet(t,
                                               [[u[v] for v in A[y]] for u in w],
                                               z = I[y][0],
                                               i = independentNeighbours(s),
                                               I = I[y])
                c += a[0]
                v += a[1]
            m.append((c, v))
##            print(T)
##            print(w)
##            print('-----------------------------------------------------')
        return max(m)
                
                    
