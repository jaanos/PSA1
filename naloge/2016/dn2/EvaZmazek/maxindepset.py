# -*- coding: utf-8 -*-
from functools import lru_cache

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

    @lru_cache(maxsize=None)
    def vzorciZaPot(k):
        """
        opis funkcije:
        časovna zahtevnost: k = 0, 1, 2, 3: T(k) = O(1)
        sicer : T(k) = T(k-2) + T(k-1) + O(1) = 2*T(k-2) + T(k-3) + O(1) = 3*T(k-3) + 2*T(k-2) +O(1) = ... = O(2^k)
        prostorska zahtevnost: P(k) = O(k)
        """
        if vsi_vzorci_za_pot[k] is not None:
            return vsi_vzorci_za_pot[k]
        if k == 0:
            return [], []
        if k == 1:
            return [[0], [1]], [0, 1]
        if k == 2:
            return [[0, 0], [0, 1], [1, 0]], [0, 1, 2]
        if k == 3:
            return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 1]], [0, 1, 2, 4, 5]
        vzorci = []
        stevilo = []
        prviVzorci = vzorciZaPot(k-1)
        drugiVzorci = vzorciZaPot(k-2)
        for i in drugiVzorci[0]:
            vzorci += [[1, 0] + i]
        for j in prviVzorci[0]:
            vzorci += [[0] + j]
        for i in drugiVzorci[1]:
            stevilo += [2 ** (k - 1) + i]
        for j in prviVzorci[1]:
            stevilo += [j]
        vsi_vzorci_za_pot[k] = vzorci, stevilo
        return vzorci, stevilo

    vsi_vzorci_za_pot = [None for j in range(max(k+1, 4))]
    for j in range(4):
        vsi_vzorci_za_pot[j] = vzorciZaPot(j)
    vzorciZaPot(k)

    def vzorciZaCikel(k):
        """
        Opis funkcije:
        časovna zahtevnost: T(k) = O(n^(k-2)) + O(n^(k-3)) = O(n^(k-3)*(n+1)) = O(n^(k-3)*n)
        Prostorska zahtevnost: P(k) = 2 * k * število vzorcev = 2 * k * (1 + sqrt(5))/2
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
        prviVzorci = vsi_vzorci_za_pot[k-2]
        drugiVzorci = vsi_vzorci_za_pot[k-3]
        for i in drugiVzorci[0]:
            vzorci += [[1, 0] + i + [0]]
            vzorci += [[0] + i + [0, 1]]
        for j in prviVzorci[0]:
            vzorci += [[0] + j + [0]]
        for i in drugiVzorci[1]:
            stevilo += [2 ** (k - 1) + i * 2, i * 4 + 1]
        for j in prviVzorci[1]:
            stevilo += [j * 2]
        return vzorci, stevilo

    vzorciZaCikel_sez = vzorciZaCikel(k) #dodaten prostor 2 * k * število vzorcev za cikel dolžine k
    vsi_vzorci_za_cikel = vzorciZaCikel_sez[0] #dodaten prostor k * število vzorcev za cike dolžine k

    def vsotaVzorca(indexVzorca, u):
        """
        Opis funkcije: izračuna vsoto, ki jo dobimo, če seštejemo uteži na vozliščih, ki ležijo n vozlišču u v drevesu
        in v ciklu na točkah, ki ga prestavlja vzorec cikla z indeksom indexVzorca.
        Časovna zahtevnost: V tej funkciji se sprehodimo skozi vzorec dolžine k, zato je časovna zahtevnost enaka O(k).
        Prostorska zahtevnost: Shranjujemo si le vrednost vsota, zato je prostorska zahtevnost enaka O(1).
        """
        vsota = 0
        vzorcek = vsi_vzorci_za_cikel[indexVzorca]
        for i in range(k):
            if vzorcek[i] == 1:
                vsota += w[i][u]
        return vsota

    def slovarZdruzljivih(vzorci):
        """
        za množico vzorcev ustvari slovar združljivih vzorcev (vzorci so podani s števili, ki jih vzorci
        predstavljajo, če na njih gledamo kot na dvojiški zapis števila). Za vsak vzorec nam poda indekse vzorcev,
        ki so združljivi z našim vzorcem.
        Časovna zahtevnost: v prvi zanki V(k)-krat izvedemo zanko, katere časovna zahtevnost je enaka O(V(k)).
         Skupna časovna zahtevnost je torej enaka O(V(k)^(2)) = O(((1+sqrt(5))/2)^(2)).
        Prostorska zahtevnost: V slovarju za vsak vzorec shranimo indekse vzorcev, ki so z njim združljivi, torej
        je prostorska zahtevnost navzgor omejena z O(V(k)^(2)).
        """
        slovar = dict()
        for vzorec in vzorci:
            slovar[vzorec] = [indeks for indeks, j in enumerate(vzorci) if vzorec&j == 0]
        return slovar

    def nothing(u, v=None):
        """
        Previsit/postvisit funkcija, ki ne naredi nič.
        Časovna zahtevnost: O(1)
        """
        return True

    vzorci = vzorciZaCikel_sez[1]
    vrednostiVozliscSedem = [[None]*len(vzorci) for i in range(n)]
    print(vrednostiVozliscSedem)

    zdruzljivi = slovarZdruzljivih(vzorciZaCikel_sez[1])

    range_l = range(len(vzorci)) #prostorska in časovna zahtevnost O(1)

    def postvisitSedem(u,v):
        for indexVzorca in range_l:
            vzorec = vzorci[indexVzorca]
            vsota = vsotaVzorca(indexVzorca, u)
            vrednostiVozliscSedem[u][indexVzorca] = (vsota, [(u, indexVzorca)])
            for sin in T[u]:
                if sin == v:
                    continue
                maximum = 0
                sezna = []
                for indexMoznega in zdruzljivi[vzorec]:
                        if vrednostiVozliscSedem[sin][indexMoznega][0] > maximum:
                            maximum = vrednostiVozliscSedem[sin][indexMoznega][0]
                            sezna = vrednostiVozliscSedem[sin][indexMoznega][1]
                vrednost, seznamcek = vrednostiVozliscSedem[u][indexVzorca]
                vrednost += maximum # vrednosti doseženi z vzorcem na vozlišču u dodamo največjo možno  doseženo vrednost z vzorci na sinu sin
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

    vrednost, seznamVzorcevZaVsakoVozlisceTree = max(vrednostiVozliscSedem[0][k] for k in range(len(vzorciZaCikel_sez[0])))

    uporabljeneTocke = []
    for vozlisceDrevesa, indexVzorec in seznamVzorcevZaVsakoVozlisceTree:
        vzorcek = vzorciZaCikel(k)[0][indexVzorec]
        for i in range(k):
            if vzorcek[i] == 1:
                uporabljeneTocke += [(i, vozlisceDrevesa)]

    return (vrednost, uporabljeneTocke)