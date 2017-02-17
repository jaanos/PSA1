# -*- coding: utf-8 -*-

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
