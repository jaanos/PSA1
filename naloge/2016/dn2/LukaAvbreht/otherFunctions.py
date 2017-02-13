

def primeren_otrok(parent,child):
    """It returns true if the ciycle child can ba a neighbour cycle of parent (input is in string in binary)"""
    k = len(parent)
    assert k == len(child), \
        "Parent and child must be of same size"
    for i in range(k):
        if parent[i] == child[i] == 1:
            return False
    return True

def list_primernih_otrok(parent):
    """Returns the list of all valid children of a parent as a list of binary numbers(strings)"""
    assert valid_cycle(parent) == True, "Parent is not the valid cycle"
    if parent[0] == '1':
        res = ['0']
        k = 1
    else:
        res = ['1','0']
        k = 2
    for i in parent[1:]:
        tren = list()
        if i =='1':
            for j in range(k):
                tren.append(res[j]+'0')
        else:
            dif = 0
            for j in range(k):
                if res[j][-1]=='1':
                    tren.append(res[j]+'0')
                    dif += 1
                else:
                    tren.append(res[j]+'1')
                    tren.append(res[j]+'0')
            k = k*2-dif
        res = tren
    tren = list()
    for i in res:
        if valid_cycle(i):
            tren.append(i)
    return tren

def valid_cycle(cycle):
    """Returns True if a cycle is valid and False othervise (Cycle is valid ifi it has an independent subgroup of ones)"""
    for i in range(len(cycle)-1):
        if cycle[i] == '1':
            if cycle[i-1] != '0' or cycle[i+1] != '0':
                return False
    return True

def are_neighbours(a,b,T):  # aLso returns false if you compere by
    """Returns True if two nodes are neighbours, otherwise returns False"""
    x,u = a[0],a[1]
    y,v = b[0],b[1]
    Cikelsos = abs((x-y)%k)
    if u == v and Cikelsos <= 1:
        return True
    Drevosos = u in T[v]
    if Cikelsos == 0 and Drevosos:
        return True
    return False

def all_valid_cycles(n):
    """
    Returns the dictonary, with all posible paterns of length n as:

    Patern : list(all posible children of that kind of patern)

    """
    keys = list_primernih_otrok('0'*n)
    res = dict()
    for i in keys:
        res[i] = list_primernih_otrok(i)
    return res

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



def directet_tree(T, DFS = iterDFS):
    n = len(T)
    res = [None]*n

    def nothing(u, v = None):
        """
        Previsit/postvisit funkcija, ki ne naredi nič.

        Časovna zahtevnost: O(1)
        """
        return True

    def previsit(u,v = None):
        res[u] = T[u][:]
        try:
            res[u].remove(v)
        except:
            pass
        return True

    if not DFS(T, roots = [0] ,previsit = previsit,postvisit = nothing):
        return False
    return res


