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

