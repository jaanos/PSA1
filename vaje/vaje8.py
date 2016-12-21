# -*- coding: utf-8 -*-
"""
Funkcije na grafih.

V ocenah časovne zahtevnosti je n število vozlišč v grafu,
m število povezav v grafu, d(u) pa število sosedov vozlišča u.
Pri tem predpostavljamo, da velja n = O(m)
(graf ima O(1) povezanih komponent).
"""
from vaje3 import Queue
from vaje5 import nothing

def BFS(G, root, visit = nothing):
    """
    Iskanje v širino iz vozlišča root.

    Spremenljivka visit določa funkcijo,
    ki se izvede ob obisku posameznega vozlišča.
    Kot vhod dobi trenutno vozlišče in njegovega predhodnika
    (oziroma None, če tega ni).
    Da se algoritem nadaljuje, mora vrniti True;
    če vrne False, se funkcija prekine in vrne False.
    Če iskanje pride do konca, funkcija vrne True.

    Časovna zahtevnost: O(m) + O(n) klicev funkcije visit
    """
    q = Queue()
    q.enqueue((root, None))
    visited = [False] * len(G)
    visited[root] = True
    while len(q) > 0:
        u, v = q.dequeue()
        if not visit(u, v):
            return False
        for w in G[u]:
            if visited[w]:
                continue
            visited[w] = True
            q.enqueue((w, u))
    return True

def dvodelen(G):
    """
    Če je graf G dvodelen, vrne 2-barvanje grafa.
    V nasprotnem primeru vrne False.
    Za barvanje uporablja iskanje v širino.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    sez = [None] * n
    def visit(u, v):
        if v is None:
            sez[u] = True
        else:
            sez[u] = not sez[v]
        for w in G[u]:
            if sez[w] is sez[u]:
                return False
            return True
    for u in range(n):
        if sez[u] is None:
            if not BFS(G, u, visit = visit):
                return False
    return sez

def stPoti(G, x, y):
    """
    Določi število najkrajših poti od x do y v grafu G.

    Časovna zahtevnost: O(m)
    """
    n = len(G)
    S = [0] * n
    nivo = [None] * n
    S[x], nivo[x] = 1, 0
    def visit(u, v):
        """
        Prišteje število poti do vozlišča u njegovim naslednikom.

        Ustavi iskanje, ko naleti na vozlišče y.

        Časovna zahtevnost: O(d(u))
        """
        if u == y:
            return False
        for w in G[u]:
            if nivo[w] is None:
                nivo[w] = nivo[u] + 1
            if nivo[w] > nivo[u]:
                S[w] += S[u]
        return True
    BFS(G, x, visit = visit)
    return S[y]

def girth(G):
    """
    Določi ožino grafa G, tj. dolžino najkrajšega cikla.

    Za vsako vozlišče naredi iskanje v širino,
    pri čemer se ustavi pri največji globini,
    ki bi še lahko dala krajši cikel od nazadnje najdenega.

    Časovna zahtevnost: O(mn)
    """
    n = len(G)
    najkrajsi = n + 1
    for u in range(len(G)):
        nivo = {u}
        dosezena = {u}
        globina = 1
        while 2*globina <= najkrajsi:
            naslednji = set()
            for v in nivo:
                for w in G[v]:
                    if w < u:
                        continue
                    if w not in dosezena:
                        dosezena.add(w)
                        naslednji.add(w)
                    elif w in nivo:
                        najkrajsi = 2*globina - 1
                        break
                    elif w in naslednji:
                        najkrajsi = 2*globina
                if najkrajsi == 2*globina - 1:
                    break
            nivo = naslednji
            globina += 1
    if najkrajsi > n:
        return float('inf')
    return najkrajsi
