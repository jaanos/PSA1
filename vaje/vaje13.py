# -*- coding: utf-8 -*-
from vaje8 import BFS

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

class PartialCover:
    """
    Razred za hranjenje podatkov pri računanju delnega pokritja drevesa.

    Vrednost V[u, b, i, j, t] = (x, k), kjer:
    - x je največje število pokritih povezav v poddrevesih s koreni T[u][i:j]
      (vključno s povezavami od u do korenov),
      če je skupna teža izbranih vozlišč največ t
      in b določa, ali je vozlišče u izbrano (ne šteje v težo!);
    - če je i = j+1, k določa, ali je vozlišče T[u][i] izbrano;
    - če je i < j+1, k določa največjo težo izbranih vozlišč
      v poddrevesih s koreni T[u][i:(i+j)//2]
    """

    def __init__(self, T, w):
        """
        Inicializira objekt za dano drevo in teže vozlišč.

        Z iskanjem v širino določi starša za vsako vozlišče.

        Časovna zahtevnost: O(n)
        """
        n = len(T)
        assert n > 0
        assert n == len(w)
        assert all(x == int(x) and x > 0 for x in w)
        self.T = T
        self.w = w
        self.V = {}
        self.p = [None] * n
        def visit(u, v):
            """
            Zabeleži prednika vozlišča u in njegov vrstni red obiskanja.

            Časovna zahtevnost: O(1)
            """
            self.p[u] = v
            return True
        BFS(T, 0, visit = visit)

    def interval(self, u, b, i, j, t):
        """
        Poišče množico vozlišč s težo največ t
        v poddrevesih s koreni v T[u][i:j],
        ki maksimizira število pokritih povezav.
        Parameter b določa, ali je vozlišče u pokrito,
        njegova teža pa ni všteta v težo t.

        Časovna zahtevnost: O(r t^2) ob prvem klicu in O(1) sicer,
        kjer je r število vozlišč v poddrevesih
        """
        # Preverimo, ali že imamo poračunano rešitev
        if (u, b, i, j, t) not in self.V:
            if i+1 == j:
                # Smo na povezavi do v
                v = self.T[u][i]
                if self.p[u] == v:
                    # Če smo na povezavi do starša, jo ignoriramo
                    x, k = 0, None
                elif t == 0:
                    # Če je omejitev 0, štejemo povezavo samo, če je u izbran
                    x, k = int(b), None
                else:
                    # Prva možnost: v ni izbran
                    l = [(self.interval(v, False, 0, len(self.T[v]), t)[0] + b,
                          False)]
                    # Druga možnost: v je izbran, zmanjšamo omejitev
                    if self.w[v] <= t:
                        l.append((self.interval(v, True, 0, len(self.T[v]),
                                                t - self.w[v])[0] + 1, True))
                    # Vzamemo boljšo od obeh možnosti
                    x, k = max(l)
            else:
                # Imamo širši interval, razdelimo ga na dva dela
                h = (i + j) // 2
                # Pregledamo razdelitev omejitev med oba dela
                x, k = max((self.interval(u, b, i, h, s)[0] +
                            self.interval(u, b, h, j, t-s)[0], s)
                           for s in range(t+1))
            # Shranimo rešitev
            self.V[u, b, i, j, t] = (x, k)
        return self.V[u, b, i, j, t]

    def solution(self, u, b, i, j, t, S):
        """
        Sestavi seznam vozlišč iz poddreves s koreni T[u][i:j]
        v delnem pokritju.

        Časovna zahtevnost: O(r),
        kjer je r število vozlišč v poddrevesih
        """
        if t == 0:
            return
        x, k = self.V[u, b, i, j, t]
        if i+1 == j:
            v = self.T[u][i]
            if self.p[u] == v:
                return
            if k:
                S.append(v)
                t -= self.w[v]
            self.solution(v, k, 0, len(self.T[v]), t, S)
        else:
            h = (i + j) // 2
            self.solution(u, b, i, h, k, S)
            self.solution(u, b, h, j, t-k, S)

def maximalPartialCover(T, w, W):
    """
    Poišče množico vozlišč v drevesu T s skupno težo največ W,
    ki maksimizira število pokritih povezav.

    Časovna zahtevnost: O(n W^2)
    """
    assert W >= 0
    n = len(T)
    assert len(w) == n
    if n == 0 or W == 0:
        return (0, 0, [])
    C = PartialCover(T, w)
    m = len(T[0])
    # Prva možnost: koren ni izbran
    l = [(C.interval(0, False, 0, m, W)[0], False)]
    # Druga možnost: koren je izbran, zmanjšamo omejitev
    if w[0] <= W:
        l.append((C.interval(0, True, 0, m, W - w[0])[0], True))
    # Vzamemo boljšo od obeh možnosti
    x, k = max(l)
    S = []
    if k:
        S.append(0)
        W -= w[0]
    C.solution(0, k, 0, m, W, S)
    return (sum(w[u] for u in S), x, S)

def lightestPartialCover(T, w, a):
    """
    Poišče najlažjo množico vozlišč v drevesu T,
    ki pokrije vsaj a povezav.

    Časovna zahtevnost: O(n W^2),
    kjer je W teža optimalne rešitve
    """
    n = len(T)
    assert len(w) == n
    assert a < n
    if a <= 0:
        return (0, 0, set())
    C = PartialCover(T, w)
    m = len(T[0])
    W, x = 0, 0
    # Ponavljamo, dokler ne dosežemo želenega števila povezav
    while x < a:
        # Povečamo skupno omejitev
        W += 1
        # Prva možnost: koren ni izbran
        l = [(C.interval(0, False, 0, m, W)[0], False)]
        # Druga možnost: koren je izbran, zmanjšamo omejitev
        if w[0] <= W:
            l.append((C.interval(0, True, 0, m, W - w[0])[0], True))
        # Vzamemo boljšo od obeh možnosti
        x, k = max(l)
    S = []
    if k:
        S.append(0)
        W -= w[0]
    C.solution(0, k, 0, m, W, S)
    return (sum(w[u] for u in S), x, S)

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
