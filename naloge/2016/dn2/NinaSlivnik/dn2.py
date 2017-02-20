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

    def dfs_usmerjeno_drevo(T, u = 0):
        "Iz neusmerjenega drevesa T (seznam seznamov) dobimo usmerjeno drevo (slovar oblike oce:[sin1,sin2,...]) s korenom v 0"
        n = len(T)
        slovar_ocetov = {}
        slovar_ocetov[u] = T[u]
        vozlisca = [u]
        def rekurzija(sez, v):
            for voz in T[v]:
                if v in T[voz]:
                    if voz not in sez:
                        sez.append(voz)
                        sinovi = []
                        for kandidat in T[voz]:
                            if kandidat not in vozlisca:
                                sinovi.append(kandidat)
                        slovar_ocetov[voz] = sinovi
                        sez = rekurzija(sez, voz)
            return sez
        vozlisca = rekurzija(vozlisca, u)
        return slovar_ocetov

    def combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)
            
    def vsi_neodvisni_cikli(k):
        "Vrne vse neodvisne podmnozice cikla dolzine k"
        seznam_ciklov = [()]
        for i in range(1,k):
            kombinacije = combinations(range(k),i)
            for komb in kombinacije:
                dodaj = True
                for j in range(len(komb)-1):
                    if abs(komb[j]-komb[j+1]) == 1:
                        dodaj = False
                if (komb[len(komb)-1] == k-1) and (komb[0] == 0):
                    dodaj = False
                if dodaj == True:
                    seznam_ciklov.append(komb)
        return seznam_ciklov

    k = len(w)
    neodvisne_mnozice = vsi_neodvisni_cikli(k)
    
    def dfs(slovar_ocetov, w, u = 0):
        "Opis algoritma: Sprejme usmerjeno drevo (seznam seznamov), tabelo utezi w in vrh drevesa, vrne pa seznam trojic oblike"
        "(teza, podmnozica cikla(ki vsebuje vrh drevesa), mnozica izbranih vozlisc vkljucno s prejsnjo podmnozico)"
        seznam_resitev = []
        for mnozica in neodvisne_mnozice:
            vsota = 0
            for elt in mnozica:
                vsota = vsota + w[elt][u]
            vsi_pari = []
            for elt in mnozica:
                vsi_pari.append((elt,u))
            trojica = (vsota, mnozica, vsi_pari)
            seznam_resitev.append(trojica)
        if slovar_ocetov[u] == []:
            return(seznam_resitev)
        else:
            nov_seznam_resitev = []
            for sin in slovar_ocetov[u]:
                resitve_sina = dfs(slovar_ocetov, w, sin)
                for (vsota_oce, mnozica_oce, vsi_pari_oce) in seznam_resitev:
                    vsota2 = 0
                    for (vsota_sin, mnozica_sin, vsi_pari_sin) in resitve_sina:
                        if len(mnozica_oce + mnozica_sin) == len(list(set(mnozica_oce) | set(mnozica_sin))):
                            if vsota_oce + vsota_sin > vsota2:
                                vsota2 = vsota_oce + vsota_sin
                                najboljsa = (vsota_oce + vsota_sin, mnozica_oce, vsi_pari_oce + vsi_pari_sin)
                    nov_seznam_resitev.append(najboljsa)
                seznam_resitev = nov_seznam_resitev
                nov_seznam_resitev = []
            return seznam_resitev

    najvecji = 0
    resitev = None
    resitve = dfs(dfs_usmerjeno_drevo(T),w)
    for (vsota, mnozica, pari) in resitve:
        if vsota > najvecji:
            najvecji = vsota
            resitev = pari
    return (najvecji, resitev)
