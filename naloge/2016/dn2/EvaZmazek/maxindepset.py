# -*- coding: utf-8 -*-

def maxCycleTreeIndependentSet(T, w):
    T = [[1, 2], [0], [0]]
    w = [[1, 1, 1],
         [2, 2, 2],
         [3, 3, 3],
         [4, 4, 4]]
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
        # časovna zahtevnost: eksponentna v k
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
        for i in vzorciZaCikel(k - 3)[0]:
            vzorci += [[1, 0] + i + [0]]
        for j in vzorciZaCikel(k - 1)[0]:
            vzorci += [[0] + j]
        for i in vzorciZaCikel(k - 3)[1]:
            stevilo += [2 ** (k - 1) + i * 2]
        for j in vzorciZaCikel(k - 1)[1]:
            stevilo += [j]
        return vzorci, stevilo


    def vsotaVzorca(vzorec, u):  # dolzina vzorca = k (zapisanjega v obliki vzorca, ta je v obliki stevilke)
        vzorcek = []
        for i in range(k):
            vzorcek += [(vzorec // (2 ** (i))) % 2]
        vsota = 0
        for i in range(k):
            if vzorcek[i] == 1:
                vsota += w[k - i - 1][u]
        return vsota

        #    print(vzorciZaCikel(7))


    def slovarZdruzljivih(vzorci):
        slovar = dict()
        for vzorec in vzorci:
            slovar[vzorec] = [j for j in vzorci if vzorec & j == 0]
        return slovar

        #    print(slovarZdruzljivih(vzorciZaCikel(6)[1]))


    def nothing(u, v=None):
        """
        Previsit/postvisit funkcija, ki ne naredi nič.
        Časovna zahtevnost: O(1)
        """
        return True


    vrednostiVozlisc = [[(None, None)] * n for i in range(k)]
    vrednostiVozliscSedem = [[None] * len(vzorciZaCikel(k)[1]) for i in range(n)]
    globinaDrevesa = [None] * n


    #    print(vrednostiVozliscSedem)

    def postvisit(u, v):
        for cikel in range(k):
            potomciPotomcev = 0
            potomci = 0
            for sin in T[u]:
                if sin == v:
                    continue
                print("vrednostiVozlisc:", vrednostiVozlisc[cikel][sin])
                if max(vrednostiVozlisc[cikel][sin][0], vrednostiVozlisc[cikel][sin][1]) > 0:
                    potomci += max(vrednostiVozlisc[cikel][sin][0], vrednostiVozlisc[cikel][sin][1])
                for vnuk in T[sin]:
                    if vnuk == u:
                        continue
                    if max(vrednostiVozlisc[cikel][vnuk][0], vrednostiVozlisc[cikel][vnuk][1]) > 0:
                        potomciPotomcev += max(vrednostiVozlisc[cikel][vnuk][0], vrednostiVozlisc[cikel][vnuk][1])

            vrednostiVozlisc[cikel][u] = (potomciPotomcev + w[cikel][u], potomci)
            print(vrednostiVozlisc)
        return True


    def postvisitSedem(u, v):
        vzorci = vzorciZaCikel(k)[1]
        l = len(vzorci)
        ##        print("stevilo vzorcev:", l)
        for indexVzorca in range(l):
            vzorec = vzorci[indexVzorca]
            vsota = vsotaVzorca(vzorec, u)
            ##            print(vsota)
            vrednostiVozliscSedem[u][indexVzorca] = vsota
            for sin in T[u]:
                if sin == v:
                    continue
                vrednostiVzorcev = []
                maximum = 0
                for indexMoznega in range(l):
                    if vzorci[indexMoznega] in slovarZdruzljivih(vzorci)[vzorec]:
                        vrednostiVzorcev += [indexMoznega, vrednostiVozliscSedem[sin][indexMoznega]]
                        if vrednostiVozliscSedem[sin][indexMoznega] > maximum:
                            maximum = vrednostiVozliscSedem[sin][indexMoznega]
                        print("mozni:", vzorci[indexMoznega], vrednostiVozliscSedem[sin][indexMoznega])
                print("vrednostiVzorcev:", vrednostiVzorcev)
                vrednostiVozliscSedem[u][indexVzorca] += maximum
        # vrednostiVozliscSedem[u] = (max ce vzamemo prvi vzorec, max ce vzamemo drugi vzorec, max ce vzamemo tretji vzorec, ..., max ce vzamemo zadnji vzorec)

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


    def celotenGrafzVrednostmi(T, w):
        # pripravimo si graf (oz matriko sosedov, kjer i-ti stolpec
        # in j-ta vrstica predstavljata seznam sosedov i-tega
        # elementa v drevesu in j -tega elementa v ciklu),
        # zadnja vrednost pa pove, če je element v grafu ali ne

        n = len(T)
        k = len(w)
        celotenGraf = []
        for nadstropje in range(k):
            vozlisca = []
            for vozlisce in range(n):
                sosedje = dict()
                a = (nadstropje + 1) % k
                b = (nadstropje - 1) % k
                sosedje[(vozlisce, a)] = 1
                sosedje[(vozlisce, b)] = 1
                for sosed in T[vozlisce]:
                    sosedje[(sosed, nadstropje)] = 1
                vozlisca += [sosedje]
            celotenGraf += [vozlisca]
        return celotenGraf


    def celotenGraf(T, w):
        # pripravimo si graf (oz matriko sosedov, kjer i-ti stolpec
        # in j-ta vrstica predstavljata seznam sosedov i-tega
        # elementa v drevesu in j -tega elementa v ciklu),
        # zadnja vrednost pa pove, če je element v grafu ali ne

        n = len(T)
        k = len(w)
        celotenGraf = []
        for nadstropje in range(k):
            vozlisca = []
            for vozlisce in range(n):
                sosedje = []
                a = (nadstropje + 1) % k
                b = (nadstropje - 1) % k
                sosedje += [(vozlisce, a)]
                sosedje += [(vozlisce, b)]
                for sosed in T[vozlisce]:
                    sosedje += [(sosed, nadstropje)]
                vozlisca += [sosedje]
            celotenGraf += [vozlisca]
        return celotenGraf


    print(DFS(T, roots=None, previsit=nothing, postvisit=postvisitSedem))

    print(celotenGraf(T, w))

    print(vsotaVzorca(18, 0))
    
    return max(vrednostiVozliscSedem[0][k] for k in range(len(vzorciZaCikel(k)[0])))


        # print("nekaj dela in ljubljana je najlepse mesto")
    #
    # # pripravimo si graf (oz matriko sosedov, kjer i-ti stolpec
    # # in j-ta vrstica predstavljata seznam sosedov i-tega
    # # elementa v drevesu in j -tega elementa v ciklu),
    # # zadnja vrednost pa pove, če je element v grafu ali ne
    #
    #
    # seznamTock = [[1] * n for i in range(k)]
    # print(seznamTock)
    #
    # celotenGraf = []
    # for nadstropje in range(k):
    #     vozlisca = []
    #     for vozlisce in range(n):
    #         sosedje = dict()
    #         a = (nadstropje + 1) % k
    #         b = (nadstropje - 1) % k
    #         sosedje[(vozlisce, a)] = 1
    #         sosedje[(vozlisce, b)] = 1
    #         for sosed in T[vozlisce]:
    #             sosedje[(sosed, nadstropje)] = 1
    #         vozlisca += [sosedje]
    #     celotenGraf += [vozlisca]
    # print(celotenGraf)
    #
    # def maxneodvisne(G):
    #
    #     prazen = True
    #
    #     k = len(G)
    #     n = len(G[0])
    #     for i in range(k):
    #         for j in range(n):
    #             if seznamTock[i][j] == 1:
    #                 prazen = False
    #     if prazen:
    #         print(seznamTock)
    #         return 0
    #
    #     print("pripravimo si zeznam točk, ki pove, kateri element še je v grafu:")
    #     print("seznam točk")
    #
    #     maximum1 = 0
    #     maximum2 = 0
    #
    #     for i in range(k):
    #         for j in range(n):
    #             if seznamTock[i][j] == 0:
    #                 print("element:", (i, j), "ni ga v grafu")
    #                 continue
    #             print("element:", (i, j), "je še v grafu")
    #             # če ne vzamemo tega elementa:
    #             # pobrišemo njega in vse povezave z njim
    #             # če ga vzamemo:
    #             # najprej pobrišemo njega, nato še njegove sosede
    #             # pobrišemo vse povezave z njim in z njegovimi sosedi
    #             seznamTock[i][j] = 0  # v vsakem primeru vzamemo vozlišče
    #             print("seznam točk zdaj ijzgleda takole:")
    #             print(seznamTock[i] for i in range(k))
    #             sosedje = G[i][j]  # v vsakem primeru pogledamo sosede
    #             popravimo = []
    #             for sosed in sosedje:
    #                 if seznamTock[sosed[1]][sosed[0]] == 0:
    #                     continue
    #
    #                 # ga vzamemo:
    #                 seznamTock[sosed[1]][sosed[0]] = 0
    #                 popravimo += [[sosed[1], sosed[0]]]
    #             print("v tem koraku smo izbrisali sosede in ''na novo izbrisane'' dodali v seznam popravimo:")
    #             print("seznamTock:", seznamTock)
    #             print("popravimo:", popravimo)
    #
    #             if seznamTock[i][j] is not o:
    #                 maximum1 = maxneodvisne(G) + w[i][j]
    #             else:
    #                 maximum1 = maxneodvisne(G)
    #             # dodamo nazaj sosede, ki so prej bili tam
    #             print("nepopravljenSeznamToc:", seznamTock)
    #             for popravek in popravimo:
    #                 print(popravek)
    #                 seznamTock[popravek[0]][popravek[1]] = 1
    #             print(maximum1)
    #             print("popravljenSeznamTock:", seznamTock)
    #
    #             # zdaj imamo pripravljeno za izračun v primeru, ko elementa ne vzamemo
    #             maximum2 = maxneodvisne(G)
    #
    #             seznamTock[i][j] = 1
    #             print(seznamTock)
    #
    #             return max(maximum1, maximum2)
    #
    # maximumumum = maxneodvisne(celotenGraf)
    # print(maximumumum)
    #
    # return "Eva"

