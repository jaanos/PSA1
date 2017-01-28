# -*- coding: utf-8 -*-
from .pripomocki import *
import itertools

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

    D = pripraviDrevo(T,k)

    memo = {}

    def soseda(i,v):
        if i[0] == v[0] and i[1] in T[v[1]]:
            return True
        if i[1] == v[1] and ((i[0] - v[0])%k == 1 or (v[0] - i[0])%k == 1):
            return True
        return False

    def postvisit(u, v=None):
        memo[u] = {}
        mn, stars, otroci = D[u]
        if len(otroci) == 0: #leaf
            v = mn.copy().pop()
            memo[u][frozenset()] = (0, [])
            memo[u][frozenset([v])] = (w[v[0]][v[1]], [v])
        elif len(otroci) == 1:
            ot = otroci[0]
            mn1, stars1, otroci1 = D[ot]
            if len(mn1) < len(mn): #introduce node
                v = (mn - mn1).pop()
                for x in powerset(mn1):
                    x = frozenset(x)
                    memo[u][x] = memo[ot][x]
                    flag = True
                    for i in x:
                        if soseda(i,v):
                            memo[u][x|frozenset([v])] = (None, [])
                            flag = False
                    if flag:
                        if memo[ot][x][0] is None:
                            memo[u][x|frozenset([v])] = (None, [])
                        else:
                            memo[u][x|frozenset([v])] = (memo[ot][x][0] + w[v[0]][v[1]], memo[ot][x][1] + [v])
            else: #forget node
                v = (mn1 - mn).pop()
                for x in powerset(mn):
                    x = frozenset(x)
                    a, c = memo[ot][x]
                    b, d = memo[ot][x|frozenset([v])]
                    if a is not None and b is not None:
                        if a >= b:
                            memo[u][x] = (a, c)
                        else:
                            memo[u][x] = (b, d)
                    elif a is not None and b is None:
                        memo[u][x] = (a, c)
                    elif a is None and b is not None:
                        memo[u][x] = (b, d)
                    else:
                        memo[u][x] = (None, [])
        else: #join node
            a = otroci[0]
            b = otroci[1]
            for x in powerset(mn):
                x = frozenset(x)
                teza =  0
                for i in x:
                    teza += w[i[0]][i[1]]
                if memo[a][x][0] is not None and memo[b][x][0] is not None:
                    memo[u][x] = (memo[a][x][0] + memo[b][x][0] - teza, list(set(memo[a][x][1] + memo[b][x][1])))
                else:
                    memo[u][x] = (None, [])
                    
        for i in otroci:
            del memo[i]
            
        return True

    DFS(D, [0], previsit=nothing, postvisit=postvisit)
    
    maxi = 0
    rez = 0
    for x, y in memo[0].values():
        if x is not None and x > maxi:
            maxi = x
            rez = (x, sorted(y))
    return rez
    

def treeDecomposition(T, k):
    D = [0]*len(T)

    def visit(u, v = None):
        stars = v
        otroci = []
        for x in T[u]:
            if x != v:
                otroci.append(x)
        mnozica = {(i,u) for i in range(k)}
        if v != None:
            for i in range(k):
                mnozica.add((i,v))
        D[u] = [mnozica, stars, otroci]
        return True
        
    BFS(T, 0, visit)
    return D

def pripraviDrevo(T, k):
    D = treeDecomposition(T,k)
    oznaka = len(D)
    visited = [False]*oznaka

    def niceTreeDecompositionPrva(T,u):
        if visited[u]:
            return
        visited[u] = True
        nonlocal oznaka
        mn, stars, otroci = T[u]
        if len(otroci) > 2:
            c = otroci[0]
            del otroci[0]
            for x in otroci:
                T[x][1] = oznaka
            T[u][2] = [c, oznaka]
            T.append([mn, u, otroci])
            visited.append(False)
            o = oznaka
            oznaka += 1
            niceTreeDecompositionPrva(T,c)
            niceTreeDecompositionPrva(T,o)
        for i in otroci:
            niceTreeDecompositionPrva(T,i)

    niceTreeDecompositionPrva(D,0)

    oznaka = len(D)
    visited = [False]*oznaka

    def niceTreeDecompositionDruga(T,u):
        if visited[u]:
            return
        visited[u] = True
        nonlocal oznaka
        mn, stars, otroci = T[u]
        if len(otroci) == 2:
            a = otroci[0]
            if T[a][0] != mn:
                T.append([mn,u,[a]])
                visited.append(False)
                T[a][1] = oznaka
                otroci[0] = oznaka
                oznaka += 1
            b = otroci[1]
            if T[b][0] != mn:
                T.append([mn,u,[b]])
                visited.append(False)
                T[b][1] = oznaka
                otroci[1] = oznaka
                oznaka += 1
        for i in otroci:
            niceTreeDecompositionDruga(T,i)

    niceTreeDecompositionDruga(D,0)

    oznaka = len(D)
    visited = [False]*oznaka
    
    def niceTreeDecompositionTretja(T,u):
        if visited[u]:
            return
        visited[u] = True
        nonlocal oznaka
        mn, stars, otroci = T[u]
        if len(otroci) == 0 and len(mn) > 1:
            mn1 = mn.copy()
            mn1.pop()
            T.append([mn1,u,[]])
            visited.append(False)
            otroci.append(oznaka)
            oznaka += 1
            
        elif len(otroci) == 1:
            a = otroci[0]
            mn1, stars1, otroci1 = T[a]
            if mn <= mn1:
                if len(mn1) - len(mn) > 1:
                    for x in mn1:
                        if x not in mn:
                            b = x
                            break
                    T.append([mn|{b},u,[a]])
                    visited.append(False)
                    T[a][1] = oznaka
                    otroci[0] = oznaka
                    oznaka += 1
            else:
                for x in mn:
                    if x not in mn1:
                        b = x
                        break
                T.append([mn-{b},u,[a]])
                visited.append(False)
                T[a][1] = oznaka
                otroci[0] = oznaka
                oznaka += 1
            
        for i in otroci:
            niceTreeDecompositionTretja(T,i)
            
            
    niceTreeDecompositionTretja(D,0)     

    return D
        
    








    
