# -*- coding: utf-8 -*-

def cheapestLimitedPath(G, u, v, T):
    """
    Poišče najkrajšo pot od u do v v usmerjenem acikličnem grafu G,
    katere trajanje ne preseže T.

    Oznake povezav v grafu G so pari (cena, trajanje).

    Časovna zahtevnost: O(nT)
    """
    inf = float('inf')
    top = topoOrder(G)
    s = {(w, 0): (0 if w == u else inf, 0, None) for w in range(len(G))}
    for w in top[top.index(u):top.index(v)]:
        for i in range(T):
            if (w, i) not in s:
                s[w, i] = s[w, i-1]
            p, d = s[w, i][:2]
            for x, (c, t) in G[w].items():
                j = i+t
                if j > T:
                    continue
                c += p
                if (x, j) not in s or c < s[x, j][0]:
                    s[x, j] = (c, d+t, w)
    while T >= 0:
        if (v, T) in s:
            break
        T -= 1
    p, d, w = s[v, T]
    if p == inf:
        return None
    pot = [v]
    i = T
    while w is not None:
        j = i - G[w][v][1]
        pot.append(w)
        i, v, w = j, w, s[w, j][2]
    return (p, d, list(reversed(pot)))

def floydWarshall(G):
    """
    Floyd-Warshallov algoritem za iskanje najkrajših poti
    med vsemi pari vozlišč grafa G.

    Vrne tak seznam seznamov p,
    da je za vozlišči u in v element p[u][v] par,
    ki vsebuje razdaljo med u in v ter vozlišče na najkrajši poti med njima,
    oziroma None, če tega ni.

    Časovna zahtevnost: O(n^3)
    """
    n = len(G)
    s = {}
    inf = float('inf')
    S = [[(0 if u == v else inf, -1) for v in range(n)] for u in range(n)]
    T = [[None for v in range(n)] for u in range(n)]
    for u, a in enumerate(G):
        for v, t in a.items():
            S[u][v] = (t, -1)
    for w in range(n):
        S, T = T, S
        for u in range(n):
            for v in range(n):
               S[u][v] = min(T[u][v], (T[u][w][0] + T[w][v][0], w))
    return S

def floydWarshallPath(p, u, v):
    """
    Iz izhoda Floyd-Warshallovega algoritma
    rekonstruira najkrajšo pot od u do v.

    Časovna zahtevnost: O(n),
    """
    def pot(x, y):
        """
        Sestavi pot od vključno x do izključno y.

        Časovna zahtevnost: O(p(x, y)),
        kjer je p število povezav v najkrajši poti od x do y
        """
        z = p[x][y][1]
        return [x] if z == -1 else (pot(x, z) + pot(z, y))
    d = p[u][v][0]
    return None if d == float('inf') \
                else (d, pot(u, v) + ([] if u == v else [v]))
