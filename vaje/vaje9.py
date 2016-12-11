# -*- coding: utf-8 -*-
"""
Funkcije na grafih.

V ocenah časovne zahtevnosti je n število vozlišč v grafu,
m število povezav v grafu, d(u) pa število sosedov vozlišča u.
Pri tem predpostavljamo, da velja n = O(m)
(graf ima O(1) povezanih komponent).
"""

from kopica import BinaryHeap
from vaje6 import toporder

def dijkstra(G, s, t = None, PriorityQueue = BinaryHeap):
    """
    Poišče najkrajše razdalje od vozlišča s do ostalih vozlišč.

    Časovna zahtevnost: O(m) sprememb vrednosti v vrsti +
                        O(n) pobiranj iz vrste
    """
    assert all(all(l >= 0 for l in a.values()) for a in G), \
        "V grafu so negativne povezave!"
    inf = float('inf')
    n = len(G)
    Q = PriorityQueue({v: 0 if v == s else inf for v in range(n)})
    razdalje = [None] * n
    p = [None] * n
    while len(Q) > 0:
        v, d = Q.pop()
        razdalje[v] = d
        if v == t:
            break
        for w, l in G[v].items():
            if razdalje[w] is not None:
                continue
            r = d + l
            if r < Q[w]:
                Q[w] = r
                p[w] = v
    return razdalje, p

def shortestPath(G, s, t, PriorityQueue = BinaryHeap):
    """
    Poišče najkrajšo pot od vozlišča s do vozlišča t.

    Za G sprejme bodisi graf ali pa izhod funkcije dijkstra.

    Časovna zahtevnost za graf na vhodu: O(m) sprememb vrednosti v vrsti +
                                         O(n) pobiranj iz vrste
    Časovna zahtevnost za par na vhodu:  O(n)
    """
    if isinstance(G, tuple):
        r, p = G
    else:
        r, p = dijkstra(G, s, t, PriorityQueue = BinaryHeap)
    pot = []
    d = r[t]
    while t is not None:
        pot.append(t)
        t = p[t]
    return (d, list(reversed(pot)))

def najkrajsePoti(G, T, s):
    """
    Preveri, ali je dano usmerjeno drevo drevo najkrajših poti
    usmerjenega grafa G z (morda negativnimi) utežmi.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    assert n == len(T), "Grafa imata različno število vozlišč!"
    assert all(all(v in G[u] for v in a) for u, a in enumerate(T)), \
        "Podano drevo ni podgraf podanega grafa!"
    top = toporder(T)
    assert top[0] == s, "Podano vozlišče ni koren drevesa!"
    razdalje = [None] * n
    razdalje[s] = 0
    for v in top:
        assert razdalje[v] is not None, "Podani graf ni krepko povezan!"
        for u in T[v]:
            assert razdalje[u] is None, "Podani graf ni usmerjeno drevo!"
            razdalje[u] = razdalje[v] + G[v][u]
    for v in range(n):
        for u in G[v]:
            if G[v][u] < razdalje[u] - razdalje[v]:
                return False
    return True

def enolicneNajkrajsePoti(G, s, PriorityQueue = BinaryHeap):
    """
    Za vsako vozlišče odloči,
    ali zanj obstaja enolično določena najkrajša pot od s.

    Časovna zahtevnost: O(m) sprememb vrednosti v vrsti +
                        O(n) pobiranj iz vrste
    """
    assert all(all(l > 0 for l in a.values()) for a in G), \
        "V grafu so negativne ali ničelne povezave!"
    inf = float('inf')
    n = len(G)
    Q = PriorityQueue({v: 0 if v == s else inf for v in range(n)})
    sez = [True] * n
    while len(Q) > 0:
        v, d = Q.pop()
        for u, l in G[v].items():
            if u not in Q:
                continue
            r = d + l
            if r < Q[u]:
                Q[u] = r
                sez[u] = sez[v]
            elif r == Q[u]:
                sez[u] = False
    return sez
