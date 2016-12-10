# -*- coding: utf-8 -*-
"""
Funkcije na grafih.

V ocenah časovne zahtevnosti je n število vozlišč v grafu,
m število povezav v grafu, d(u) pa število sosedov vozlišča u.
Pri tem predpostavljamo, da velja n = O(m)
(graf ima O(1) povezanih komponent).
"""

from kopica import BinaryHeap

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
