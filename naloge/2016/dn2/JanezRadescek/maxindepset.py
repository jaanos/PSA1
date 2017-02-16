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

    raise NotImplementedError("Naredi sam!")


    memo = {}



    def rekurzija(drevo, utezi, oce, ded = None):

        sinovi = nasledniki(oce, ded)

        for sin in sinovi:
            if sin in memo:
                continue

            elif sinJeList(sin, oce):
                pass

            else:
                memo[sin] = rekurzija(drevo, utezi, sin, oce)





    def nasledniki(oce, ded):
        pass


    def sinJeList(sin, oce):
        pass

    def kombinacije(oce):
        pass