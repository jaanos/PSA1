# -*- coding: utf-8 -*-

def longestCommonSubstring(x, y):
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
    n = len(x)
    m = len(y)
    V = {}
    for i in range(n+1):
        V[i, 0] = 0
    for j in range(m+1):
        V[0, j] = 0
    for i in range(n):
        for j in range(m):
            if x[i] == y[j]:
                V[i+1, j+1] = V[i, j] + 1
            else:
                V[i+1, j+1] = max(V[i, j+1], V[i+1, j])
    return V[n, m]

def matrike(m, st = lambda a, b, c: a*b*c):
    n = len(m) - 1
    v = {(i, i+1): (0, None) for i in range(n)}
    for i in range(2, n+1):
        for j in range(n-i+1):
            v[j, j+i] = min((v[j, k][0] + v[k, j+i][0] +
                             st(m[j], m[k], m[j+i]), k)
                            for k in range(j+1, j+i))
    def oklepaji(i, j):
        if i == j-1:
            return i
        k = v[i, j][1]
        return [oklepaji(i, k), oklepaji(k, j)]
    return (v[0, n][0], oklepaji(0, n))
