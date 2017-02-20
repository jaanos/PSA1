# -*- coding: utf-8 -*-
"""
Funkcije na grafih.

V ocenah časovne zahtevnosti je n število vozlišč v grafu,
m število povezav v grafu, d(u) pa število sosedov vozlišča u.
Pri tem predpostavljamo, da velja n = O(m)
(graf ima O(1) povezanih komponent).
"""
from vaje3 import Stack

def nothing(u, v = None):
    """
    Previsit/postvisit funkcija, ki ne naredi nič.

    Časovna zahtevnost: O(1)
    """
    return True

def DFS(G, roots = None, previsit = nothing, postvisit = nothing):
    """
    Rekurzivno iskanje v globino.

    Graf G je podan kot seznam seznamov sosedov za vsako vozlišče.
    Seznam roots določa vozlišča, iz katerih se začne iskanje
    - privzeto so to vsa vozlišča v grafu.
    Spremenljivki previsit in postvisit določata funkciji,
    ki se izvedeta ob prvem oziroma zadnjem obisku posameznega vozlišča.
    Kot vhod dobita trenutno vozlišče in njegovega predhodnika
    (oziroma None, če tega ni).
    Da se algoritem nadaljuje, morata vrniti True;
    če vrneta False, se funkcija prekine in vrne False.
    Če iskanje pride do konca, funkcija vrne True.

    Časovna zahtevnost: O(m) + O(n) klicev funkcij previsit in postvisit
    """
    def explore(u, v = None):
        """
        Obišče vozlišče u, če še ni bilo obiskano,
        in se rekurzivno kliče na njegovih sosedih.

        Časovna zahtevnost: O(d(u)) + klica funkcij previsit in postvisit
        """
        if visited[u]:
            return True
        visited[u] = True
        if not previsit(u, v):
            return False
        for w in G[u]:
            if not explore(w, u):
                return False
        return postvisit(u, v)

    n = len(G)
    visited = [False] * n
    if roots is None:
        roots = range(n)
    for u in roots:
        if not explore(u):
            return False
    return True

def iterDFS(G, roots = None, previsit = nothing, postvisit = nothing):
    """
    Rekurzivno iskanje v globino.

    Argumenti so enaki kot pri funkciji DFS.

    Časovna zahtevnost: O(m) + O(n) klicev funkcij previsit in postvisit
    """
    s = Stack()
    n = len(G)
    visited = [False] * n
    if roots is None:
        roots = range(n)
    v, it = None, iter(roots)
    while True:
        try:
            u = next(it)
        except StopIteration:
            if v is None:
                return True
            u = v
            v, it = s.pop()
            if not postvisit(u, v):
                return False
            continue
        if visited[u]:
            continue
        visited[u] = True
        if not previsit(u, v):
            return False
        s.push((v, it))
        v, it = u, iter(G[u])

def dvodelen(G, DFS = DFS):
    """
    Če je graf G dvodelen, vrne 2-barvanje grafa.
    V nasprotnem primeru vrne None.

    Časovna zahtevnost: O(m)
    """
    barva = [None] * len(G)
    def previsit(u, v):
        """
        Pobarva vozlišče z drugačno barvo kot predhodnik,
        nato pa preveri, ali ima kak sosed že isto barvo.

        Časovna zahtevnost: O(d(u))
        """
        if v is None:
            barva[u] = 0
        else:
            barva[u] = 1 - barva[v]
        return all(barva[w] != barva[u] for w in G[u] if barva[w] is not None)
    if not DFS(G, previsit = previsit):
        return False
    return barva

def treeMax(T, r, x, DFS = DFS):
    """
    Za drevo T s korenom r vrne seznam,
    ki za vsako vozlišče u poda največjo vrednost iz seznama x,
    ki ustreza kakemu vozlišču iz poddrevesa s korenom u.

    Časovna zahtevnost: O(n)
    """
    assert len(T) == len(x)
    z = [None] * len(T)
    def postvisit(u, v):
        """
        Nastavi vrednost za trenutno vozlišče
        kot maksimum znanih vrednosti sosedov in x[u].

        Časovna zahtevnost: O(d(u))
        """
        z[u] = max([z[w] for w in T[u] if w != v] + [x[u]])
        return True
    DFS(T, roots = [r], postvisit = postvisit)
    return z

def edgeCycle(G, x, y, DFS = DFS):
    """
    Preveri, ali povezava xy v grafu G leži na kakem ciklu.

    Časovna zahtevnost: O(m)
    """
    assert x in G[y] and y in G[x]
    pody = False
    cikel = False
    def previsit(u, v):
        """
        Če sreča vozlišče y, preveri, ali je njegov predhodnik x.
        Če je bilo vozlišče y že obiskano, preveri,
        ali je trenutno vozlišče sosedno vozlišču x.

        Časovna zahtevnost: O(d(u))
        """
        nonlocal pody, cikel
        if u == y:
            if v != x:
                cikel = True
                return False
            pody = True
        elif pody:
            if x in G[u]:
                cikel = True
                return False
        return True
    def postvisit(u, v):
        """
        Če sreča vozlišče y, prekine iskanje.

        Časovna zahtevnost: O(1)
        """
        return u != y
    DFS(G, roots = [x], previsit = previsit, postvisit = postvisit)
    return cikel

def ancestorLabel(T, r, l, DFS = DFS):
    """
    Za drevo T s korenom r vrne seznam,
    ki za vsako vozlišče u poda vrednost iz seznama l,
    ki ustreza l[u]-predhodniku vozlišča u
    (tj., vozlišču, ki je za l[u] stopenj višje od u na poti do r,
    pri čemer za predhodnika korena r vzamemo kar sam r).

    Časovna zahtevnost: O(n)
    """
    assert len(T) == len(l)
    assert all(x >= 0 for x in l)
    z = [None] * len(T)
    s = []
    def previsit(u, v = None):
        """
        Doda vozlišče na sklad in mu nastavi novo oznako.

        Časovna zahtevnost: O(1)
        """
        s.append(u)
        z[u] = l[s[-(1 + l[u])]] if l[u] < len(s) else l[r]
        return True
    def postvisit(u, v = None):
        """
        Odstrani vozlišče s sklada.

        Časovna zahtevnost: O(1)
        """
        s.pop()
        return True
    DFS(T, roots = [r], previsit = previsit, postvisit = postvisit)
    return z
