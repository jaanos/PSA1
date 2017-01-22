# -*- coding: utf-8 -*-
from itertools import *

class StackRecord:
    """Vnos v skladu"""
    def __init__(self, x = None, next = None):
        """
        Inicializacija vnosa v skladu.
        Časovna zahtevnost: O(1)
        """
        self.x = x
        self.next = next

    def __repr__(self):
        """
        Znakovna predstavitev vnosa v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.next is None:
            return "|]"
        return "|%s|<" % repr(self.x)

class Stack:
    """Sklad (LIFO)"""
    def __init__(self):
        """
        Inicializacija sklada.
        Časovna zahtevnost: O(1)
        """
        self.clear()

    def __len__(self):
        """
        Velikost sklada.
        Časovna zahtevnost: O(1)
        """
        return self.len

    def __repr__(self):
        """
        Znakovna predstavitev sklada.
        Časovna zahtevnost: O(n)
        """
        if self.len == 0:
            return "<|]"
        cur = self.top
        out = "<| %s" % repr(cur.x)
        cur = cur.next
        while cur.next is not None:
            out += " <- %s" % repr(cur.x)
            cur = cur.next
        return "%s |]" % out

    def clear(self):
        """
        Izprazni sklad.
        Časovna zahtevnost: O(1)
        """
        self.top = StackRecord()
        self.len = 0

    def peek(self):
        """
        Vrni vrhnji element v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.top.next is None:
            raise IndexError('peek on an empty stack')
        return self.top.x

    def pop(self):
        """
        Odstrani in vrni vrhnji element v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.top.next is None:
            raise IndexError('pop from an empty stack')
        top = self.top
        self.top = top.next
        self.len -= 1
        return top.x

    def push(self, x):
        """
        Dodaj element na vrh sklada.
        Časovna zahtevnost: O(1)
        """
        self.top = StackRecord(x, self.top)
        self.len += 1

class QueueRecord:
    """Vnos v vrsti"""
    def __init__(self, x = None, prev = None, next = None):
        """
        Inicializacija vnosa v vrsti.
        Časovna zahtevnost: O(1)
        """
        self.x = x
        if prev is not None and next is None:
            next = prev.next
        elif prev is None and next is not None:
            prev = next.prev
        if prev is not None:
            prev.next = self
        if next is not None:
            next.prev = self
        self.prev = prev
        self.next = next

    def __repr__(self):
        """
        Znakovna predstavitev vnosa v vrsti.
        Časovna zahtevnost: O(1)
        """
        if self.prev is None:
            return ">|"
        if self.next is None:
            return "|>"
        return ">|%s|>" % repr(self.x)

class Queue:
    """Vrsta (FIFO)"""
    def __init__(self):
        """
        Inicializacija vrste.
        Časovna zahtevnost: O(1)
        """
        self.start = QueueRecord()
        self.end = QueueRecord(prev = self.start)
        self.len = 0

    def __len__(self):
        """
        Dolžina vrste.
        Časovna zahtevnost: O(1)
        """
        return self.len

    def __repr__(self):
        """
        Znakovna predstavitev vrste.
        Časovna zahtevnost: O(n)
        """
        if self.len == 0:
            return ">|>"
        cur = self.start.next
        out = ">| %s" % repr(cur.x)
        cur = cur.next
        while cur.next is not None:
            out += " -> %s" % repr(cur.x)
            cur = cur.next
        return "%s |>" % out

    def clear(self):
        """
        Izprazni vrsto.
        Časovna zahtevnost: O(1)
        """
        self.start.next = self.end
        self.end.prev = self.start
        self.len = 0

    def dequeue(self):
        """
        Odstrani in vrni prednji element vrste.
        Časovna zahtevnost: O(1)
        """
        last = self.end.prev
        if last.prev is None:
            raise IndexError('dequeue from an empty queue')
        self.end.prev = last.prev
        last.prev.next = self.end
        self.len -= 1
        return last.x

    def enqueue(self, x):
        """
        Dodaj element na konec vrste.
        Časovna zahtevnost: O(1)
        """
        QueueRecord(x, prev = self.start)
        self.len += 1

    def peek(self):
        """
        Vrni prednji element vrste.
        Časovna zahtevnost: O(1)
        """
        last = self.end.prev
        if last.prev is None:
            raise IndexError('peek on an empty queue')
        return last.x

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
        sosedi = G[u][2].copy()
        if G[u][1] is not None:
            sosedi.append(G[u][1])
        for w in sosedi:
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

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
