# -*- coding: utf-8 -*-


minusNeskoncno = float("-inf")


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

    #raise NotImplementedError("Naredi sam!")



    #slovar kamor si bomo shranjevali rezultate za podprobleme P = O(n*2^k)
    memo = {}


    def rekurzija(sidro, ded):
        """za izbrano sidro rekurzivno najdemo vozlišča da bo teža največja. ded potrebujemo da se ne vračamo po drevesu nazaj"""
        #Trekurzija = 2*Tnasledniki + Tnasledniki * Trekurzija + Tteza = O(n*2^k)

        sinovi2D = nasledniki(sidro, ded)

        for sinDrevo in sinovi2D:
            for sin in sinDrevo:
                if sin in memo:
                    continue

                elif sinJeList(sin):
                    memo[sin] = ustavitev(sin)

                else:
                    memo[sin] = rekurzija(sin, sidro)


        vsota = teza(sidro)
        cikliPotomcev = []
        for sinDrevo in sinovi2D:
            c = (minusNeskoncno,None)
            najboljsi = None
            for sin in sinDrevo:
                if memo[sin][0] > c[0]:
                    c = memo[sin]
                    najboljsi = sin
            vsota += c[0]
            cikliPotomcev += [najboljsi]
        memo[sidro] = (vsota, cikliPotomcev)

        return (vsota, cikliPotomcev)

    def ustavitev(sin):
        """če je sin list"""
        #Tustavitev = Tteza = O(k)
        memo[sin] = (teza(sin), None)
        return (teza(sin), None)

    def teza(sidro):
        """izračuna težo izbranih vozliš vozlišč """
        #Tteza = O(k)
        (polozaj, cikel) = sidro
        vsota = 0
        for i in range(k):
            if cikel % 2 == 1:
                vsota += w[i][polozaj]
            cikel = cikel // 2

        return vsota

    def nasledniki(sidro, ded):
        """vrne tabelo tabel(pogrupirani po položajih v drevesu)"""
        #Tnasledniki = n * Tkombinacije = O(n*2^k)
        nasled = []
        for sinDrevo in T[sidro[0]]:
            if sinDrevo == ded[0]:
                pass
            else:
                nasled += [kombinacije(sinDrevo, sidro)]
        return nasled

    def sinJeList(sin):
        """"preveri če je sin list"""
        #TsinJeList = O(1)
        return len(T[sin[0]]) == 1

    def kombinacije(sinDrevo, sidro):
        """vrne vse možne kombinacije ciklov za sinDrevo, ki se prilegajo ciklu od sidra"""
        #Tkombinacije = O(2^k)
        moznih = 2**k
        kombi = []
        for cikel in range(moznih):
            if preveri(cikel, sidro[1]):
                kombi += [(sinDrevo,cikel)]
        return  kombi

    def preveri(sumljivCikel, sidroCikel):
        """preveri izbrana cikla(za sidroCikel privzamemo da je vredu)"""
        #Tpreveri = O(k)
        if sumljivCikel & sidroCikel != 0:
            return False

        else:
            aaa = sumljivCikel
            if (aaa%2 == 1) and (1 == (aaa//(2**(k-1)) %2)):
                return False

            for i in range(k-1):
                tre = aaa%2
                nas = aaa//2%2
                if tre == 1 and nas == 1:
                    return False
                aaa = aaa//2
        return True


    Janez = "haskelHeker"

    #za vse možne cikle na prvem vozlišču v drevesu izračunamo vrednosti in izberemo najboljšo
    #Tnekaj = Tkombinacije = O(2^k)
    haha = (minusNeskoncno, None)
    najKoren = None
    for kombina in kombinacije(0, (-10,0)):
        ha =  rekurzija(kombina, (-10,0))
        if ha[0] > haha[0]:
            haha = ha
            najKoren = kombina

    return memo[najKoren]

    # #za vsako vozlišče v drevesu najdemo cikel, ki pripada vozlišču pri največji teži celotnega drevesa
    # #najKoren =(mesto v drevesu, cikel)
    #
    # def VozliscaSCikli():
    #     """vrne slovar s cikli za vsako vozlišče pri največji teži drevesa"""
    #     vozlisca = {}
    #     neobdelana = [najKoren]
    #
    #     while len(neobdelana)> 0:
    #         tre = neobdelana.pop()  #tre = (mesto, cikel)
    #         vozlisca[tre[0]] = tre[1]
    #         sinovi = memo[tre][1]   #memo[tre] = (teža, [sinovi=(mesto cikel)])
    #         if sinovi != None:
    #             neobdelana += sinovi
    #
    #     return vozlisca
    #
    #
    # def vrednostVozliscaVKartezicnem():
    #     """vrne vrednost in seznam vozlisc v kartezicnem produktu"""
    #     vozcikli = VozliscaSCikli()
    #     tez = memo[najKoren][0]
    #     vozKartezicnem = []
    #     for vozlisce in vozcikli:
    #         (pozicija,cikel) = vozlisce
    #         for i in range(k):
    #             if cikel%2 == 1:
    #                 vozKartezicnem += [(pozicija, i)]
    #             cikel = cikel //2
    #
    #     return (tez, vozKartezicnem)
    #
    #
    # return vrednostVozliscaVKartezicnem()