# -*- coding: utf-8 -*-

def maxCycleTreeIndependentSet(T, w):
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).

    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), \
        "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
        "Podani graf ni neusmerjen!"
    k = len(w)
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])

    def vzorciZaCikel(k):
        """
        Opis funkcije:
        časovna zahtevnost: eksponentna v k
        Prostorska zahtevnost:
        """
        if k == 0:
            return [], []
        if k == 1:
            return [[0], [1]], [0, 1]
        if k == 2:
            return [[0, 0], [0, 1], [1, 0]], [0, 1, 2]
        if k == 3:
            return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]], [0, 1, 2, 4]
        vzorci = []
        stevilo = []
        for i in vzorciZaCikel(k-3)[0]:
            vzorci += [[1,0] + i + [0]]
            vzorci += [[0] + i + [0, 1]]
        for j in vzorciZaCikel(k-2)[0]:
            vzorci += [[0] + j + [0]]
        for i in vzorciZaCikel(k-3)[1]:
            stevilo += [2**(k-1) + i*2, i*4 + 1]
        for j in vzorciZaCikel(k-2)[1]:
            stevilo += [j*2]
        return vzorci, stevilo

    def vsotaVzorca(indexVzorca, u):
        """
        Opis funkcije:
        dolzina vzorca = k (zapisanjega v obliki vzorca, ta je v obliki stevilke)
        Časovna zahtevnost:
        Prostorska zahtevnost:
        """
        vsota = 0
        vzorcek = vzorciZaCikel(k)[0][indexVzorca]
        for i in range(k):
            if vzorcek[i] == 1:
                vsota += w[i][u]
        return vsota

    def slovarZdruzljivih(vzorci):
        """
        za množico vzorcev ustvari slovar združljivih vzorcev (vzorci so podani s tevili, ki jih vzorci
        predstavljajo, če na njih gledamo kot na dvojiški zapis števila).
        Časovna zahtevnost:
        Prostorska zahtevnost:
        """
        slovar = dict()
        for vzorec in vzorci:
            slovar[vzorec] = [j for j in vzorci if vzorec&j == 0]
        return slovar

    def nothing(u, v=None):
        """
        Previsit/postvisit funkcija, ki ne naredi nič.
        Časovna zahtevnost: O(1)
        """
        return True

    vrednostiVozliscSedem = [[None]*len(vzorciZaCikel(k)[1]) for i in range(n)]

    def postvisitSedem(u,v):
        vzorci = vzorciZaCikel(k)[1]
        l = len(vzorci)
        for indexVzorca in range(l):
            vzorec = vzorci[indexVzorca]
            vsota = vsotaVzorca(indexVzorca, u)
            vrednostiVozliscSedem[u][indexVzorca] = (vsota, [(u, indexVzorca)])
            for sin in T[u]:
                if sin == v:
                    continue
                maximum = 0
                sezna = []
                for indexMoznega in range(l):
                    if vzorci[indexMoznega] in slovarZdruzljivih(vzorci)[vzorec]:
                        if vrednostiVozliscSedem[sin][indexMoznega][0] > maximum:
                            maximum = vrednostiVozliscSedem[sin][indexMoznega][0]
                            sezna = vrednostiVozliscSedem[sin][indexMoznega][1]
                vrednost, seznamcek = vrednostiVozliscSedem[u][indexVzorca]
                vrednost += maximum
                seznamcek += sezna
                vrednostiVozliscSedem[u][indexVzorca] = (vrednost, sorted(seznamcek))

        return True


    def DFS(G, roots=None, previsit=nothing, postvisit=nothing):
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

        def explore(u, v=None):
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


    DFS(T, roots=None, previsit=nothing, postvisit=postvisitSedem)

    vrednost, seznamVzorcevZaVsakoVozlisceTree = max(vrednostiVozliscSedem[0][k] for k in range(len(vzorciZaCikel(k)[0])))

    print(vzorciZaCikel(4))

    uporabljeneTocke = []
    print(seznamVzorcevZaVsakoVozlisceTree)
    for vozlisceDrevesa, indexVzorec in seznamVzorcevZaVsakoVozlisceTree:
        vzorcek = vzorciZaCikel(k)[0][indexVzorec]
        for i in range(k):
            if vzorcek[i] == 1:
                uporabljeneTocke += [(i, vozlisceDrevesa)]

    return (vrednost, uporabljeneTocke)