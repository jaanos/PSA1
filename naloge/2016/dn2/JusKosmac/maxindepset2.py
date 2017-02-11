# -*- coding: utf-8 -*-
from .pripomocki import *

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
    
    #slovar vseh moznosti za izbiro podmnozice na ciklu
    slovar_moznosti = {}
    #slovar vseh moznih izbir podmnozic, ki se ujemajo med sabo
    slovar_ujemanj = {}
    
    for i in range(2 ** k):
        #pretvorimo stevilo v binarni zapis dolzine k (po potrebi na koncu dodamo nicle)
        niz = bin(i)[2:].zfill(k)
        #moznost je seznam enic in nicel, ki ustrezajo izbranim oz. ne izbranim elementom s cikla
        moznost = list(map(int, niz))
        ustreza = True
        #preveriti moramo, da nismo izbrali sosednjih elementov na ciklu (upostevati moramo tudi zadnji in prvi element)
        for j in range(k - 1, -1, -1):
            if moznost[j] * moznost[j - 1] == 1:
                ustreza = False
                break
        if not ustreza:
            continue
        #ce moznost ustreza zahtevam, jo dodamo v slovar_moznosti (kljuc je pripadajoce stevilo)
        else:
            slovar_moznosti[i] = moznost

    #za vsako moznost poiscemo vse preostale moznosti, ki se z njo ujemajo (to pomeni, da nimajo enice na istem mestu)
    #ujemanja shranimo v slovar_ujemanj
    for i in slovar_moznosti:
        ujemanja = set()
        for j in slovar_moznosti:
            if j & i == 0:
                ujemanja.add(j)
        slovar_ujemanj[i] = ujemanja

    #funkcija, ki nam za dano vozlisce drevesa in dano izbiro podmnozice vrne njeno tezo in pripadajoca vozlisca s cikla
    def teza(u, moznost):
        vsota = 0
        vozlisca = []
        for i in range(k):
            #ce naletimo na enico, pomeni da smo izbrali to vozlisce s cikla: povecamo skupno tezo in ga dodamo v seznam vozlisc
            if moznost[i] == 1:
                vsota += w[i][u]
                vozlisca.append((i,u))
        return vsota, vozlisca

    #v ta slovar bomo shranjevali vmesne rezultate za nadaljnjo uporabo
    slovar_rezultatov = {}
    #najmanjsa mozna teza
    neginf = -float('inf')
    
    #funkcija izracunaj se bo klicala v postvisitu pri DFS obhodu drevesa
    def izracunaj(u, v = None):
        nonlocal neginf
        #seznam otrok danega vozlisca
        otroci = [x for x in T[u] if x != v]

        #za vsako mozno izbiro podmnozice na ciklu (cikel vsebuje trenutno vozlisce u) vnaprej izracunamo tezo in pripadajoca vozlisca
        #vse podatke shranimo v slovar_tez
        slovar_tez = {}
        for x in slovar_moznosti:
            slovar_tez[x] = teza(u, slovar_moznosti[x])
            
        slovar_rezultatov[u] = {}
        #slovar_rezultatov[u][moznost] bo vseboval 3 podatke:
        # - maksimalno tezo za del grafa, ki se v drevesu nahaja pod vozliscem u (pri pogoju, da smo na ciklu, ki vsebuje u, izbrali podmnozico, ki se ujema z 'moznost')
        # - vozlisca izbrane podmozice (le iz cikla, ki vsebuje u)
        # - oznako izbrane podmnozice (torej stevilo, ki nam je v binarnem zapisu porodilo to podmnozico)
        for moznost in slovar_ujemanj:
            #za zacetek nastavimo na najmanjso mozno tezo
            slovar_rezultatov[u][moznost] = (neginf, [], None)
            #pregledamo vse podmnozice, ki se ujemajo z 'moznost'
            for ujemanje in slovar_ujemanj[moznost]:
                skupaj, vozlisca = slovar_tez[ujemanje]
                #pristejemo vse maksimalne teze otrok (pri otrocih smo morali izbrati tako podmnozico, ki se ujema z 'ujemanje')
                #vse podatke ze otroke imamo ze shranjene v slovarju_rezultatov, saj smo za njih ze klicali postvisit
                for otrok in otroci:
                    skupaj += slovar_rezultatov[otrok][ujemanje][0]
                #popravimo trenutno najvecjo tezo, ce smo nasli vecjo tezo
                if skupaj > slovar_rezultatov[u][moznost][0]:
                    slovar_rezultatov[u][moznost] = (skupaj, vozlisca, ujemanje)

        return True

    iterDFS(T, [0], postvisit = izracunaj)

    #optimalna resitev je shranjena pod slovar_rezultatov[0][0]
    #to pomeni, da se mora na ciklu, ki vsebuje koren drevesa (vozlisce 0), ujemati s prazno podmnozico (oznaka 0) - torej smo lahko zaceli s katerokoli mnozico
    
    #v optimalno bomo dodajali vozlisca optimalne resitve
    optimalno = []
    #sem bomo shranjevali oznake podmnozic, ki smo jih izbrali na posameznem koraku
    predhodniki = [None] * n
    
    #funkcija dodaj_vozlisca se bo klicala v previsitu pri DFS obhodu drevesa
    def dodaj_vozlisca(u, v = None):
        nonlocal optimalno
        #to pomeni, da smo v korenu drevesa
        if v is None:
            predhodniki[u] = slovar_rezultatov[u][0][2]
            optimalno += slovar_rezultatov[u][0][1]
        else:
            #izbira je oznaka podmnozice, ki smo jo izbrali pri predhodnem vozliscu
            izbira = predhodniki[v]
            predhodniki[u] = slovar_rezultatov[u][izbira][2]
            optimalno += slovar_rezultatov[u][izbira][1]
        return True

    iterDFS(T, [0], previsit = dodaj_vozlisca)

    #vrnemo maksimalno tezo in seznam izbranih vozlisc
    return (slovar_rezultatov[0][0][0], optimalno)

            
                
        
        
