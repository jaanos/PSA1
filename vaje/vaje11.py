# -*- coding: utf-8 -*-

def sahovnica(S):
    n = len(S)
    st = (0, 1, 2, 4, 5, 8, 9, 10)
    z = {i: [j for j in st if (i & j) == 0] for i in st}
    c = lambda r, j: sum(r[i] * ((j >> i) & 1) for i in range(4))
    v = {(0, j): c(S[0], j) for j in st}
    for i in range(1, n):
        for j in st:
            v[i, j] = max(v[i-1, k] for k in z[j]) + c(S[i], j)
    return max(v[n-1, j] for j in st)

def magma(M, op, s, a):
    n = len(s)
    v = {(i, i+1, x): None for i, x in enumerate(s)}
    for j in range(2, n+1):
        for i in range(n-j+1):
            for y in M:
                for z in M:
                    x = op(y, z)
                    try:
                        v[i, i+j, x] = next(k for k in range(i+1, i+j)
                                            if (i, k, y) in v
                                            and (k, i+j, z) in v)
                    except StopIteration:
                        pass
    return (0, n, a) in v
