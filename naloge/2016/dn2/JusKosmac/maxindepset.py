# -*- coding: utf-8 -*-
from .pripomocki import *
import sys
import time
##sys.setrecursionlimit(10000)

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

    #z uporabo pomozne funkcije iz drevesa T konstruiramo lepo drevesno dekompozicijo z drevesno sirino 2k
    D = buildTree(T, k)
    print(len(D))

    #pripravimo si slovar, kamor bomo shranjevali vmesne rezultate
    memo = {}

    #funkcija 'soseda' preveri, ce sta vozlisci 'i' in 'v' sosednji v grafu
    def soseda(i,v):
        #imata prvi komponenti enaki in sta drugi komponenti sosednji v T
        if i[0] == v[0] and i[1] in T[v[1]]:
            return True
        #imata drugi komponenti enako in sta drugi komponenti sosednji v ciklu (se razlikujeta za +-1)
        if i[1] == v[1] and ((i[0] - v[0])%k == 1 or (v[0] - i[0])%k == 1):
            return True
        return False

    #postvisit bomo uporabljali pri DFS pregledu grafa D
    def postvisit(u, v=None):
        memo[u] = {}
        mn, stars, otroci = D[u]
        if len(otroci) == 0: #leaf
            v = mn.copy().pop()
            memo[u][frozenset()] = (0, [])
            memo[u][frozenset([v])] = (w[v[0]][v[1]], [v])
        elif len(otroci) == 1:
            ot = otroci[0]
            mn1, stars1, otroci1 = D[ot]
            if len(mn1) < len(mn): #introduce node
                v = (mn - mn1).pop()
                for x in powerset(mn1):
                    x = frozenset(x)
                    memo[u][x] = memo[ot][x]
                    flag = True
                    for i in x:
                        if soseda(i,v):
                            memo[u][x|frozenset([v])] = (None, [])
                            flag = False
                    if flag:
                        if memo[ot][x][0] is None:
                            memo[u][x|frozenset([v])] = (None, [])
                        else:
                            memo[u][x|frozenset([v])] = (memo[ot][x][0] + w[v[0]][v[1]], memo[ot][x][1] + [v])
            else: #forget node
                v = (mn1 - mn).pop()
                for x in powerset(mn):
                    x = frozenset(x)
                    a, c = memo[ot][x]
                    b, d = memo[ot][x|frozenset([v])]
                    if a is not None and b is not None:
                        if a >= b:
                            memo[u][x] = (a, c)
                        else:
                            memo[u][x] = (b, d)
                    elif a is not None and b is None:
                        memo[u][x] = (a, c)
                    elif a is None and b is not None:
                        memo[u][x] = (b, d)
                    else:
                        memo[u][x] = (None, [])
        else: #join node
            a = otroci[0]
            b = otroci[1]
            for x in powerset(mn):
                x = frozenset(x)
                teza =  0
                for i in x:
                    teza += w[i[0]][i[1]]
                if memo[a][x][0] is not None and memo[b][x][0] is not None:
                    memo[u][x] = (memo[a][x][0] + memo[b][x][0] - teza, list(set(memo[a][x][1] + memo[b][x][1])))
                else:
                    memo[u][x] = (None, [])
                    
        for i in otroci:
            del memo[i]
            
        return True

    t = time.time()
    iterDFS(D, [0], previsit=nothing, postvisit=postvisit)
    print(time.time() - t, 'pregled')
    
    maxi = 0
    rezultat = 0
    for x, y in memo[0].values():
        if x is not None and x > maxi:
            maxi = x
            rezultat = (x, sorted(y))
    return rezultat
    

#konstruiramo drevesno dekompozicijo
def treeDecomposition(T, k):
    #D bo nasa drevesna dekompozicija
    #D je predstavljen s seznamom, i-temu vozliscu v D pripada D[i]
    #D[i] je seznam s tremi elementi: mnozica ("vrecka" vozlisc, ki pripada vozliscu i), stars (None, ce je vozlisce koren) in seznam otrok
    D = [0]*len(T)

    def visit(u, v = None):
        stars = v
        otroci = []
        for x in T[u]:
            if x != v:
                #k otrokom dodamo vse sosede razen starsa
                otroci.append(x)
        #konstruiramo mnozico: dodamo toliko kopij trenutnega vozlisca kot je velikost cikla in enako za starsa, ce obstaja
        #torej so mnozice velikosti najvec 2k
        mnozica = {(i,u) for i in range(k)}
        if v != None:
            for i in range(k):
                mnozica.add((i,v))
        D[u] = [mnozica, stars, otroci]
        return True
        
    #pozenemo BFS iz zacetnega vozlisca, uporabljamo prej definirano funkcijo visit
    #s tem smo generirali drevesno dekompozicijo
    BFS(T, 0, visit)
    return D

#drevesno dekompozicijo pretvorimo v lepo drevesno dekompozicijo
#pretvorba bo potekala v treh korakih
def buildTree(D, k):
    T = treeDecomposition(D, k)

    #v prvem koraku bomo poskrbeli, da imajo vsa vozlisca najvec 2 otroka
    def niceTreeDecompositionPrva(u):
        #ce je bilo vozlisce ze obiskano, ga ne popravljamo vec
        if visited[u]:
            return
        #oznacimo, da smo vozlisce ze obiskali
        visited[u] = True
        mn, stars, otroci = T[u]
        #popravljamo le v primeru, ko ima vozlisce vec kot 2 otroka
        if len(otroci) > 2:
            #izberemo prvega otroka
            prvi = otroci[0]
            #prvega otroka izbrisemo iz seznama otrok
            del otroci[0]
            #preostalim otrokom nastavimo novega starsa (to bo vozlisce, ki ga bomo na novo dodali)
            temp = len(T)
            for x in otroci:
                T[x][1] = temp
            #trenutnemu vozliscu nastavimo nova otroka (sedaj ima le se 2)
            T[u][2] = [prvi, temp]
            #v drevo dodamo novo vozlisce (sedaj ima to vozlisce morebiti prevec otrok - to bomo popravili ko pridemo do njega)
            T.append([mn, u, otroci])
            visited.append(False)
            #otroke trenutnega vozlisca dodamo v vrsto
            q.enqueue(prvi)
            q.enqueue(temp)
        else:
            #otroke trenutnega vozlisca dodamo v vrsto
            for i in otroci:
                q.enqueue(i)

    #belezimo katera vozlisca smo ze obiskali
    visited = [False]*len(T)
    #v vrsto dodajamo vozlisca, ki jih potencialno moramo se popraviti
    q = Queue()

    t = time.time()
    #zacnemo v zacetnem vozliscu in izvajamo prvi korak dokler ni vrsta prazna
    q.enqueue(0)
    while len(q) > 0:
        u = q.dequeue()
        niceTreeDecompositionPrva(u)
    print(time.time() - t, 'prva')

    #v drugem koraku bomo poskrbeli, da imajo vozlisca z dvema otrokoma enake mnozice (vrecke) kot oba otroka
    def niceTreeDecompositionDruga(u):
        if visited[u]:
            return
        visited[u] = True
        mn, stars, otroci = T[u]
        if len(otroci) == 2:
            prvi = otroci[0]
            #v primeru, ko prvi otrok nima enake mnozice kot stars, dodamo vmes novo vozlisce, ki ima enako mnozico kot stars
            if T[prvi][0] != mn:
                temp = len(T)
                #novo vozlisce ima za starsa trenutno vozlisce, za otroka pa 'prvi'
                T.append([mn,u,[prvi]])
                visited.append(False)
                #popravimo starsa od 'prvi' in otroka od trenutnega vozlisca
                T[prvi][1] = temp
                otroci[0] = temp
            drugi = otroci[1]
            #ce je potrebno popravimo se drugega otroka
            if T[drugi][0] != mn:
                temp = len(T)
                T.append([mn,u,[drugi]])
                visited.append(False)
                T[drugi][1] = temp
                otroci[1] = temp
        for i in otroci:
            #dodamo vse otroke v vrsto
            q.enqueue(i)


    #ustvarimo nov seznam obiskanih in novo vrsto
    visited = [False]*len(T)
    q = Queue()
    
    t = time.time()
    #iz korena izvedemo drug korak pretvorbe v lepo drevesno dekompozicijo
    q.enqueue(0)
    while len(q) > 0:
        u = q.dequeue()
        niceTreeDecompositionDruga(u)
    print(time.time() - t, 'druga')


    #v tretjem koraku bomo poskrbeli za vozlisca z enim otrokom
    #mnozici starsa in otroka se morata razlikovati v natanko enem elementu (torej en element dodamo ali enega odvzamemo)
    #to bomo dosegli tako, da bomo med starsa in otroka, ki ne ustrezata zahtevi, vrinili vmesna vozlisca
    #popraviti moramo tudi liste, saj morajo imeti mnozico velikosti 1
    def niceTreeDecompositionTretja(u):
        if visited[u]:
            return
        visited[u] = True
        mn, stars, otroci = T[u]
        #v primeru, ko je 'u' list in ima mnozico velikosti vec kot 1
        if len(otroci) == 0 and len(mn) > 1:
            #naredimo kopijo mnozice
            mn1 = mn.copy()
            #odstranimo poljuben element iz 'mn1'
            mn1.pop()
            #ustvarimo novo vozlisce, ki bo sedaj nov list z mnozico velikosti 1 manj kot 'u'
            temp = len(T)
            T.append([mn1,u,[]])
            visited.append(False)
            #'u' sedaj ni vec list ampak ima novo ustvarjeno vozlisce za otroka
            otroci.append(temp)
        
        #v primeru, ko ima 'u' samo enega otroka    
        elif len(otroci) == 1:
            a = otroci[0]
            mn1, stars1, otroci1 = T[a]
            #v primeru, ko je 'mn' podmnozica 'mn1'
            if mn <= mn1:
                #ce se velikosti mnozic ne razlikujeta samo za 1, moramo popravljati drevo
                if len(mn1) - len(mn) > 1:
                    #poiscemo element, ki ni v 'mn' (takoj ko ga najdemo, prekinemo zanko)
                    for x in mn1:
                        if x not in mn:
                            novi = x
                            break
                    temp = len(T)
                    #ustvarimo novo vozlisce, ki bo med 'u' in 'a', imelo pa bo enako mnozico kot 'u', le da ji dodamo se element 'novi'
                    T.append([mn|{novi},u,[a]])
                    visited.append(False)
                    #popravimo starsa vozliscu 'a' (stars je novo vozlisce)
                    T[a][1] = temp
                    #popravimo otroka vozliscu 'u' (otrok je novo vozlisce)
                    otroci[0] = temp
            #podobno uredimo primer, ko 'mn' ni podmnozica 'mn1'
            else:
                #najdemo element, ki je v 'mn' in ni v 'mn1'
                for x in mn:
                    if x not in mn1:
                        novi = x
                        break
                #vmes vrinemo novo vozlisce, le da tokrat mnozici vozlisca 'u' odvzamemo element 'novi'
                temp = len(T)
                T.append([mn-{novi},u,[a]])
                visited.append(False)
                T[a][1] = temp
                otroci[0] = temp

        #v vrsto dodamo vse otroke
        for i in otroci:
            q.enqueue(i)

            
    visited = [False]*len(T)
    q = Queue()

    t = time.time()
    #izvedemo se tretji korak pretvorbe
    q.enqueue(0)
    while len(q) > 0:
        u = q.dequeue()
        niceTreeDecompositionTretja(u)
    print(time.time() - t, 'tretja')
    
    #sedaj smo drevesno dekompozicijo T transformirali v lepo drevesno dekompozicijo
    return T
        
    
##def pripraviDrevo(T, k):
##    D = treeDecomposition(T,k)
##    oznaka = len(D)
##    visited = [False]*oznaka
##
##    def niceTreeDecompositionPrva(T,u):
##        if visited[u]:
##            return
##        visited[u] = True
##        nonlocal oznaka
##        mn, stars, otroci = T[u]
##        if len(otroci) > 2:
##            c = otroci[0]
##            del otroci[0]
##            for x in otroci:
##                T[x][1] = oznaka
##            T[u][2] = [c, oznaka]
##            T.append([mn, u, otroci])
##            visited.append(False)
##            o = oznaka
##            oznaka += 1
##            niceTreeDecompositionPrva(T,c)
##            niceTreeDecompositionPrva(T,o)
##        for i in otroci:
##            niceTreeDecompositionPrva(T,i)
##
##    niceTreeDecompositionPrva(D,0)
##
##    oznaka = len(D)
##    visited = [False]*oznaka
##
##    def niceTreeDecompositionDruga(T,u):
##        if visited[u]:
##            return
##        visited[u] = True
##        nonlocal oznaka
##        mn, stars, otroci = T[u]
##        if len(otroci) == 2:
##            a = otroci[0]
##            if T[a][0] != mn:
##                T.append([mn,u,[a]])
##                visited.append(False)
##                T[a][1] = oznaka
##                otroci[0] = oznaka
##                oznaka += 1
##            b = otroci[1]
##            if T[b][0] != mn:
##                T.append([mn,u,[b]])
##                visited.append(False)
##                T[b][1] = oznaka
##                otroci[1] = oznaka
##                oznaka += 1
##        for i in otroci:
##            niceTreeDecompositionDruga(T,i)
##
##    niceTreeDecompositionDruga(D,0)
##
##    oznaka = len(D)
##    visited = [False]*oznaka
##    
##    def niceTreeDecompositionTretja(T,u):
##        if visited[u]:
##            return
##        visited[u] = True
##        nonlocal oznaka
##        mn, stars, otroci = T[u]
##        if len(otroci) == 0 and len(mn) > 1:
##            mn1 = mn.copy()
##            mn1.pop()
##            T.append([mn1,u,[]])
##            visited.append(False)
##            otroci.append(oznaka)
##            oznaka += 1
##            
##        elif len(otroci) == 1:
##            a = otroci[0]
##            mn1, stars1, otroci1 = T[a]
##            if mn <= mn1:
##                if len(mn1) - len(mn) > 1:
##                    for x in mn1:
##                        if x not in mn:
##                            b = x
##                            break
##                    T.append([mn|{b},u,[a]])
##                    visited.append(False)
##                    T[a][1] = oznaka
##                    otroci[0] = oznaka
##                    oznaka += 1
##            else:
##                for x in mn:
##                    if x not in mn1:
##                        b = x
##                        break
##                T.append([mn-{b},u,[a]])
##                visited.append(False)
##                T[a][1] = oznaka
##                otroci[0] = oznaka
##                oznaka += 1
##            
##        for i in otroci:
##            niceTreeDecompositionTretja(T,i)
##            
##            
##    niceTreeDecompositionTretja(D,0)     
##
##    return D







    
