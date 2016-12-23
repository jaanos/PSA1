# -*- coding: utf-8 -*-

def sahovnica(S):
    """
    Izbira nesosednjih polj šahovnice velikosti n × 4 z največjo vsoto.

    Časovna zahtevnost: O(n)
    """
    n = len(S)
    st = (0, 1, 2, 4, 5, 8, 9, 10)
    z = {i: [j for j in st if (i & j) == 0] for i in st}
    c = lambda r, j: sum(r[i] * ((j >> i) & 1) for i in range(4))
    v = {(0, j): (c(S[0], j), None) for j in st}
    for i in range(1, n):
        for j in st:
            s, p = max((v[i-1, k][0], k) for k in z[j])
            v[i, j] = (s + c(S[i], j), p)
    s, p = max((v[n-1, j][0], j) for j in st)
    res = []
    for i in reversed(range(n)):
        for j in reversed(range(4)):
            if (p & (1 << j)) != 0:
                res.append((i, j))
        p = v[i, p][1]
    return s, list(reversed(res))

def magma(M, op, s, a):
    """
    Za niz s elementov magme M z operacijo op postavi oklepaje tako,
    da je vrednost dobljenega niza enaka a.

    Časovna zahtevnost: O(n^3 |M|^2) + O(n^2 |M|^2) klicev funkcije op
    """
    assert a in M
    n = len(s)
    v = {(i, i+1, x): None for i, x in enumerate(s)}
    for j in range(2, n+1):
        for i in range(n-j+1):
            for y in M:
                for z in M:
                    x = op(y, z)
                    try:
                        v[i, i+j, x] = (next(k for k in range(i+1, i+j)
                                             if (i, k, y) in v
                                             and (k, i+j, z) in v), y, z)
                    except StopIteration:
                        pass
    if (0, n, a) not in v:
        return False
    def split(i, j, x):
        """
        Rekurzivno razdeli podniz s[i:j]
        glede na izračunane pozicije oklepajev.

        Časovna zahtevnost: O(j-i)
        """
        if j - i == 1:
            return s[i]
        h, y, z = v[i, j, x]
        return (split(i, h, y), split(h, j, z))
    return split(0, n, a)
