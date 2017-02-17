def vsiNeodPodCik (k):
#Vrne vse neodvisne podmnožice vozlišč za cikelj dolžine k
    def NeodPodCik(s):
        # preveri da je dana podmnožica res neodvisna
        temp = set([])
        for x in s:
            if x in temp:
                return False
            if x == 0:
                temp |= {k-1,1}
            elif x == k-1:
                temp |= {0,k-2}
            else:
                temp |= {x+1, x-1}
        return True

    lukas = [ {i} for i in range(k)]
    start = 0
    stop = k

    for dolzina in range(1,k//2):
        for i in range(start,stop-1):
            for m in range(i+1,stop):
                if NeodPodCik(lukas[i] | lukas[m]):
                    lukas.append(lukas[i] | lukas[m])
            start, stop = stop, len(lukas)

    return [set()] + lukas

def potencialni_rekurzivci(k):
    lukas = vsiNeodPodCik(k)
    L = len(lukas) #oziroma k-to Lukasovo število
    return  ({i:[j for j in range(L) if lukas[i].isdisjoint(lukas[j])] for i in range(L)}, {i:list(lukas[i])for i in range(L)})

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
