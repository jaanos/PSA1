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
from vaje6 import decompose, toporder

def oddCycle(G, DFS = DFS):
    """
    Poišče lih cikel v usmerjenem grafu.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    l = [None] * n
    x, y, z = None, None, None
    def previsit(u, v):
        """
        Označi vozlišče v trenutni poti in preveri za lihe cikle.

        Oznaka vozlišča u vsebuje naslednje elemente:
        - predhodno vozlišče vozlišča u pri iskanju v globino,
        - globina, pri kateri je doseženo vozlišče u,
        - najvišje vozlišče v ciklu z vozliščem u,
        - potomec vozlišča u s povezavo do najvišjega vozlišča v ciklu,
        - naslednik vozlišča u v ciklu z najvišjim vozliščem,
        - informacija o tem, ali je vozlišče u predhodnik trenutnega vozlišča.

        Če funkcija najde povratno povezavo iz u,
        najprej preveri, ali gre za lih cikel.
        V nasprotnem primeru posodobi informacijo
        o najvišjem predhodniku vozlišča u, s katerim je v ciklu.
        Če funkcija najde prečno povezavo do vozlišča,
        katerega najvišji predhodnik v (sodem) ciklu je predhodnik u,
        preveri, ali imamo morda sedaj lih cikel.

        Časovna zahtevnost: O(d(u))
        """
        nonlocal x, y, z
        b = 0 if v is None else l[v][1] + 1
        l[u] = [v, b, None, u, None, True]
        for w in G[u]:
            if l[w] is not None:
                d, r, s, q, t = l[w][1:]
                if t:
                    if (d - b) % 2 == 0:
                        x, y, z = w, u, u
                        return False
                    elif l[u][2] is None or d < l[l[u][2]][1]:
                        l[u][2] = w
                elif r is not None and l[r][5] and (d - b) % 2 == 0:
                    l[u][4] = w
                    x, y, z = r, u, s
                    return False
        return True
    def postvisit(u, v):
        """
        Posodobi oznako vozlišča ob vračanju.

        Po izteku funkcije vozlišče u ni več predhodnik trenutnega vozlišča,
        prav tako se posodobijo informacije o vsebujočem ciklu,
        če kateri od potomcev leži na ciklu
        z višjim vozliščem od trenutno zabeleženega.

        Časovna zahtevnost: O(d(u))
        """
        l[u][5] = False
        for w in G[u]:
            r, s = l[w][2:4]
            if r is not None and (l[u][2] is None or l[r][1] < l[l[u][2]][1]):
                l[u][2:5] = r, s, w
        return True
    if DFS(G, previsit = previsit, postvisit = postvisit):
        return False
    c = []
    s = Stack()
    w = y
    while w != z:
        c.append(w)
        w = l[w][4]
    c.append(z)
    if x != z:
        while y != x:
            y = l[y][0]
            s.push(y)
        while len(s) > 0:
            c.append(s.pop())
    return c

def countPaths(G, s, t):
    """
    Prešteje poti od s do t v usmerjenem acikličnem grafu G.

    Časovna zahtevnost: O(m)
    """
    sez = toporder(G)
    poti = [0] * len(G)
    poti[s] = 1
    for v in sez[sez.index(s):sez.index(t)]:
        for u in G[v]:
            poti[u] += poti[v]
    return poti[t]

def hamiltonianPath(G):
    """
    Poišče Hamiltonovo pot v usmerjenem acikličnem grafu, če ta obstaja.

    Časovna zahtevnost: O(m)
    """
    sez = toporder(G)
    for i in range(1, len(sez)):
        if sez[i] not in G[sez[i-1]]:
            return False
    return sez

def cheapestReachable(G, p, DFS = DFS):
    """
    Za dani seznam cen vozlišč vrne seznam cen najcenejšega vozlišča,
    ki je dosegljivo iz posameznega vozlišča usmerjenega grafa G.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    assert n == len(p)
    komp, GL = decompose(G, DFS = DFS)
    seznam = [min(p[u] for u in k) for k in komp]
    for u in range(len(GL)):
        for s in GL[u]:
            if seznam[s] < seznam[u]:
                seznam[u] = seznam[s]
    c = [None] * n
    for k in range(len(komp)):
        cena = seznam[k]
        for v in komp[k]:
            c[v] = cena
    return c
