# -*- coding: utf-8 -*-


minusNeskoncno = float("-inf")
cikel = 0




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

    raise NotImplementedError("Naredi sam!")


    memo = {}   #memo[sin] = (teza, cikli sina in njegovih pozomcev )

    #oce ali pa sin,ded = (položaj, vključena vozlišča v ciklu )

    def rekurzija(drevo, utezi, sidro, ded = None):



        sinovi2D = nasledniki(drevo, sidro, ded)


        for sinDrevo in sinovi2D:
            for sin in sinDrevo:
                if sin in memo:
                    continue

                elif sinJeList(drevo, sin, sidro):
                    memo[sin] = ustavitev(drevo, utezi, sin, sidro)

                else:
                    memo[sin] = rekurzija(drevo, utezi, sin, sidro)


        vsota = teza(utezi, sidro)
        cikliPotomcev = []
        for sinDrevo in sinovi2D:
            c = (minusNeskoncno,cikel)
            najboljsi = None
            for sin in sinDrevo:
                if memo[sin][0] > c[0]:
                    c = memo[sin]
                    najboljsi = sin
            vsota += c[0]
            cikliPotomcev += [najboljsi]
        memo[sidro] = (vsota, cikliPotomcev)

        return memo(sidro)


    def ustavitev(drevo, utezi, sidro, oce):
        pass

    def teza(utezi, sidro):
        k = len(utezi[0])
        (polozaj, cikel) = sidro
        vsota = 0
        for i in range(k):
            if cikel % 2 == 1:
                vsota += utezi[polozaj][i]
            cikel = cikel // 2

        return vsota

    def nasledniki(sidro, ded):
        pass


    def sinJeList(drevo, sin, sidro):
        pass

    def kombinacije(sidro):
        pass