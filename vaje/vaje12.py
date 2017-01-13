# -*- coding: utf-8 -*-

def longestCommonSubstring(x, y):
    """
    Najdaljši skupni podniz v nizih x in y.

    Časovna zahtevnost: O(|x| |y|)
    """
    n = len(x)
    m = len(y)
    V = {}
    for i in range(n):
        V[i, 0] = 0
    for j in range(m):
        V[0, j] = 0
    for i in range(n):
        for j in range(m):
            if x[i] == y[j]:
                V[i+1, j+1] = V[i, j] + 1
            else:
                V[i+1, j+1] = 0
    return max((k, i-k, j-k) for (i, j), k in V.items())

def longestCommonSubsequence(x, y):
    """
    Najdaljše skupno podzaporedje v nizih x in y.

    Časovna zahtevnost: O(|x| |y|)
    """
    n = len(x)
    m = len(y)
    V = {}
    for i in range(n+1):
        V[i, 0] = (0, False, None, None)
    for j in range(m+1):
        V[0, j] = (0, False, None, None)
    for i in range(n):
        for j in range(m):
            if x[i] == y[j]:
                v, c, p, q = V[i, j]
                if c:
                    p, q = i, j
                V[i+1, j+1] = (v+1, True, p, q)
            else:
                (v, c, p, q), ii, jj = max((V[i, j+1], i, j+1),
                                           (V[i+1, j], i+1, j))
                if c:
                    p, q = ii, jj
                V[i+1, j+1] = (v, False, p, q)
    sx, sy = [], []
    v, c, p, q = V[n, m]
    if c:
        sx.append(n-1)
        sy.append(m-1)
    while p is not None:
        sx.append(p-1)
        sy.append(q-1)
        p, q = V[p, q][2:]
    return (v, list(reversed(sx)), list(reversed(sy)))

def matrike(m, st = lambda a, b, c: a*b*c):
    """
    Optimalni vrstni red množenja matrik A[0], A[1], ... A[n-1],
    kjer ima matrika A[i] dimenzije m[i] × m[i+1].

    Zahtevnost množenja matrik dimenzij a × b in b × c
    je podana s funkcijo st(a, b, c).

    Časovna zahtevnost: O(n^3) klicev funkcije st
    """
    n = len(m) - 1
    v = {(i, i+1): (0, None) for i in range(n)}
    for i in range(2, n+1):
        for j in range(n-i+1):
            v[j, j+i] = min((v[j, k][0] + v[k, j+i][0] +
                             st(m[j], m[k], m[j+i]), k)
                            for k in range(j+1, j+i))
    def oklepaji(i, j):
        """
        Postavitev oklepajev za optimalno množenje matrik
        A[i], A[i+1], ..., A[j-1].

        Časovna zahtevnost: O(j-i)
        """
        if i == j-1:
            return i
        k = v[i, j][1]
        return [oklepaji(i, k), oklepaji(k, j)]
    return (v[0, n][0], oklepaji(0, n))
