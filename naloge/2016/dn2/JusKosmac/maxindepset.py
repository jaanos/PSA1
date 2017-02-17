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
        #pretvorimo stevilo v binarni zapis dolzine 'k' (po potrebi na koncu dodamo nicle)
        #enice ustrezajo vozliscem s cikla, ki smo jih izbrali, nicle pa vozliscem, ki jih nismo izbrali
        moznost = bin(i)[2:].zfill(k)
        ustreza = True
        #preveriti moramo, da nismo izbrali sosednjih vozlisc na ciklu (upostevati moramo tudi zadnje in prvo vozlisce)
        for j in range(k - 1, -1, -1):
            if moznost[j] == '1' and  moznost[j - 1] == '1':
                ustreza = False
                break
        if not ustreza:
            continue
        #ce 'moznost' ustreza zahtevam, jo dodamo v slovar_moznosti (kljuc je pripadajoce stevilo)
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

    #funkcija, ki nam za dano vozlisce drevesa in dano izbiro podmnozice vrne njeno tezo
    def teza(u, moznost):
        vsota = 0
        niz = slovar_moznosti[moznost]
        for i in range(k):
            #ce naletimo na enico, pomeni da smo izbrali to vozlisce s cikla, torej povecamo skupno tezo
            if niz[i] == '1':
                vsota += w[i][u]
        return vsota

    #v ta slovar bomo shranjevali vmesne rezultate za nadaljnjo uporabo
    slovar_rezultatov = {}
    #najmanjsa mozna teza
    neginf = -float('inf')
    
    #funkcija 'izracunaj' se bo klicala v postvisitu pri DFS obhodu drevesa
    def izracunaj(u, v = None):
        nonlocal neginf
        #seznam otrok danega vozlisca
        otroci = [x for x in T[u] if x != v]

        #za vsako mozno izbiro podmnozice na ciklu (cikel se v kartezicnem produktu nahaja na nivoju trenutnega vozlisca 'u') vnaprej izracunamo njeno tezo
        #vse podatke shranimo v 'slovar_tez'
        slovar_tez = {}
        for x in slovar_moznosti:
            slovar_tez[x] = teza(u, x)
            
        slovar_rezultatov[u] = {}
        #slovar_rezultatov[u][moznost] bo vseboval 2 podatka:
        # - maksimalno tezo neodvisne mnozice za del grafa, ki se v drevesu nahaja pod vozliscem 'u' (pri pogoju, da smo na ciklu na nivoju vozlisca 'u' izbrali podmnozico, ki se ujema z 'moznost')
        # - oznako izbrane podmnozice (torej stevilo, ki nam je v binarnem zapisu porodilo to podmnozico)
        for moznost in slovar_ujemanj:
            #za zacetek nastavimo na najmanjso mozno tezo
            slovar_rezultatov[u][moznost] = (neginf, None)
            #pregledamo vse podmnozice, ki se ujemajo z 'moznost'
            for ujemanje in slovar_ujemanj[moznost]:
                skupaj = slovar_tez[ujemanje]
                #pristejemo vse maksimalne teze otrok (pri otrocih smo morali izbrati tako podmnozico, ki se ujema z 'ujemanje')
                #vse podatke ze otroke imamo ze shranjene v slovarju_rezultatov, saj smo za njih ze klicali postvisit
                for otrok in otroci:
                    skupaj += slovar_rezultatov[otrok][ujemanje][0]
                #popravimo trenutno najvecjo tezo, ce smo nasli vecjo tezo
                if skupaj > slovar_rezultatov[u][moznost][0]:
                    slovar_rezultatov[u][moznost] = (skupaj, ujemanje)

        return True

    iterDFS(T, [0], postvisit = izracunaj)

    #optimalna resitev je shranjena pod slovar_rezultatov[0][0]
    #to pomeni, da se mora na ciklu na nivoju korena drevesa (vozlisce 0), ujemati s prazno podmnozico (oznaka 0 - vsebuje same nicle) - torej smo lahko zaceli s katerokoli podmnozico
    
    #v seznam 'optimalno' bomo dodajali vozlisca optimalne resitve
    optimalno = []
    #sem bomo shranjevali oznake podmnozic, ki smo jih izbrali na posameznem koraku
    izbrane_podmnozice = [None] * n
    
    #funkcija 'dodaj_vozlisca' se bo klicala v previsitu pri DFS obhodu drevesa
    def dodaj_vozlisca(u, v = None):
        nonlocal optimalno
        #to pomeni, da smo v korenu drevesa
        if v is None:
            izbrane_podmnozice[u] = slovar_rezultatov[u][0][1]
            #'izbira' je podmnozica, ki smo jo dejansko izbrali pri trenutnem vozliscu 'u'
            izbira = slovar_moznosti[izbrane_podmnozice[u]]
            #dodamo vozlisca, ki ustrezajo izbrani podmnozici pri trenutnem vozliscu 'u'
            for i in range(k):
                if izbira[i] == '1':
                    optimalno.append((i,u))
        else:
            izbrane_podmnozice[u] = slovar_rezultatov[u][izbrane_podmnozice[v]][1]
            #'izbira' je podmnozica, ki smo jo dejansko izbrali pri trenutnem vozliscu 'u'
            izbira = slovar_moznosti[izbrane_podmnozice[u]]
            #dodamo vozlisca, ki ustrezajo izbrani podmnozici pri trenutnem vozliscu 'u'
            for i in range(k):
                if izbira[i] == '1':
                    optimalno.append((i,u))
        return True

    iterDFS(T, [0], previsit = dodaj_vozlisca)

    #vrnemo maksimalno tezo in seznam izbranih vozlisc
    return (slovar_rezultatov[0][0][0], optimalno)

            
                
        
        
