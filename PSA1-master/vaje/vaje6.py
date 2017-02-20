# -*- coding: utf-8 -*-
"""
Funkcije na usmerjenih grafih.

V ocenah časovne zahtevnosti je n število vozlišč v grafu,
m število povezav v grafu, d(u) pa število sosedov vozlišča u.
Pri tem predpostavljamo, da velja n = O(m)
(graf ima O(1) povezanih komponent).
"""
from vaje3 import Stack
from vaje5 import DFS

def reverse(G):
    """
    Vrne graf, katerega povezave so ravno nasprotne povezavam iz G.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    V = [[] for i in range(n)]
    for i in range(n):
        for j in G[i]:
            V[j].append(i)
    return V

def decompose(G, DFS = DFS):
    """
    Vrne seznam krepko povezanih komponent (seznam seznamov vozlišč)
    in metagraf usmerjenega grafa G (vozlišča ustrezajo vrnjenim komponentam).
    Komponente so podane v obratni topološki ureditvi glede na metagraf.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    R = reverse(G)
    post = []
    def postorder(u, v):
        """
        Doda vozlišče v seznam ob njegovem zadnjem obisku.

        Časovna zahtevnost: O(1)
        """
        post.append(u)
        return True
    DFS(R, postvisit = postorder)
    l = [None] * n
    M = []
    c = 0
    comp = []
    def previsit(u, v):
        """
        Vozlišču dodeli krepko povezano komponento.

        Časovna zahtevnost: O(1)
        """
        if v is None:
            comp.append([])
            M.append(set())
        l[u] = c
        comp[c].append(u)
        return True
    def postvisit(u, v):
        """
        Doda povezave v metagraf.

        Časovna zahtevnost: O(d(u))
        """
        nonlocal c
        for w in G[u]:
            if l[w] != c:
                M[c].add(l[w])
        if v is None:
            c += 1
        return True
    DFS(G, roots = reversed(post), previsit = previsit, postvisit = postvisit)
    return (comp, [list(s) for s in M])

def toporder(G):
    """
    Topološko urejanje usmerjenega acikličnega grafa z odstranjevanjem izvorov.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    stopnje = [0] * n
    for g in G:
        for v in g:
            stopnje[v] += 1
    s = Stack()
    for i in range(n):
        if stopnje[i] == 0:
            s.push(i)
    topord = []
    while len(s) > 0:
        v = s.pop()
        topord.append(v)
        for u in G[v]:
            stopnje[u] -= 1
            if stopnje[u] == 0:
                s.push(u)
    if len(topord) < n:
        raise ValueError("Graf ima cikle!")
    return topord

def semestri(G):
    """
    Vrne najmanjše število semestrov, potrebnih za dokončanje študija,
    in seznam s prvim semestrom, v katerem lahko opravljamo določen predmet.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    assert n > 0
    s = [1] * n
    for u in toporder(G):
        for v in G[u]:
            if s[v] <= s[u]:
                s[v] = s[u] + 1
    return (max(s), s)
