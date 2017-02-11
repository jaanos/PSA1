# -*- coding: utf-8 -*-

def nothing(u, v = None):
    """
    Previsit/postvisit funkcija, ki ne naredi nič.

    Časovna zahtevnost: O(1)
    """
    return True


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
