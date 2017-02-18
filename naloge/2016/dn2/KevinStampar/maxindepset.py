def niSosed(sez1, sez2, k):
    #preveri ce sta dva seznama sosednja v ciklu C_k
    #Casovna zahtevnost:
    #V vsakem koraku eno odstevanje in deljenje
    #maksimalno stevilo korakov je len(sez1)*len(sez2)
    #Casovna zahtevnost = O(len(sez1)*len(sez2))
    for i in sez1:
        for el in sez2:
            vrednost = abs(el - i) % k
            if vrednost <= 1 or vrednost == k - 1:
                return False
    return True


def ostaliCikli(neod, neodC_k):
    # najde preostale mozne neodvisne mnozice, neod mora biti element
    # iz neodvisnih mnozic cikla C_k
    #Casovna zahtevnost:
    #len(neodC_k)=Fib(n)
    #stevilo korakov < Fib(n)*k/2*k/2
    #Casovna zahtevnost = O( ((1+sqrt(5))/2)^k * k^2 )
    sez = []
    for k in neodC_k:
        i = 0
        for j in neod:
            if j in k:
                i = 1
        if i == 0:
            sez.append(k)
    return sez


def neodCikel(k):
    #poisce vse neodvisne mnozice znotraj cikla C_k
    #Casovna zahtevnost:
    #stevilo korakov < k*Fib(k)*Fib(k)*Fib(k)
    #Casovna zahtevnost: O( (1+sqrt(5))/2)^(3k) * k )
    sez = []
    for i in range(k):
        sez.append(frozenset([i]))
        # ustvarimo seznam [[0],[1],[2],...[k]]

    i = 0
    while i < k:
        t = range(len(sez))
        for j in t:
            if niSosed([i], sez[j], k):
                a = frozenset(sez[j] | frozenset([i]))
                # da ne dodajamo enakih elementov
                if a not in sez:
                    sez.append(a)

        i = i + 1
    sez.append(frozenset([]))

    return sez


def slovNeodMnC_k(k):
    #Naredi slovar kjer so kljuci neodvisne mnozice v ciklu C_k, vrednosti
    #pa so seznami neodvisnih mnozic C_k, ki ne vsebujejo elementov iz kljuca
    #Casovna zahtevnost:
    #najvecjo zahtevnost ima klic funkcije neodCikel(k), ostalo je asimptotsko gledano, majhno.
    #O( (1+sqrt(5))/2)^(3k) * k )
    neodC_k = neodCikel(k)
    i = 0
    slov = {}
    for c in neodC_k:
        slov[frozenset(c)] = ostaliCikli(c, neodC_k)
        i = i + 1
    return slov








def maxIndeTree(tree, weights, root, nasledniki=[], izracunani={}, neodC_k=[]):
    #Za vsako vozlisce izracuna maksimalno neodvisno mnozico, v odvisnosti od tega, katere elemente vozlisca vzamemo
    k = len(weights)
    if neodC_k == []:
        #ce neodvisne mnozice cikla niso se bile poracunane, nam naredi slovar
        neodC_k = slovNeodMnC_k(k)
    if nasledniki == []:
        #ce nimamo naslednikov pomeni da smo na koncu drevesa, tukaj je maksimalna neodvisna mnozica v odvisnosti od tega,
        #katere elemente vozlisca vzamemo samo vsota utezi elementov ki jih izberemo
        slovarVozlisca = {}
        for i in neodC_k:
            #casovna zhtevnost za izracun vrednosti neodvisne mnozice v vozliscu:
            #st korakov < Fib(k)*k/2
            #O( (1+sqrt(5))/2)^k * k )
            vsota = (0,[])
            for j in i:
                vsota =(vsota[0] + weights[j][root],vsota[1] + [(j,root)])
            slovarVozlisca[i] = vsota


        izracunani[root] = slovarVozlisca

    else:
        for i in nasledniki:
            #ce naslednike imamo posljemo algoritem naprej, da poracuna prvo za njih
            noviNasledniki = [x for x in tree[i] if x != root]
            #naredimo seznam z novimi nasledniki casovna zahtevnost: O(n) (ce drevo ni nujno binarno seveda,ce je binarno O(3))
            maxIndeTree(tree, weights, i, noviNasledniki, izracunani, neodC_k)
            #racuna naprej, funkcija bo klicana n-krat, kjer je n stevilo vozlisc
        slovarVozlisca = {}
        #seznam v katerega shranjujemo najboljso mozno pot in vrednost za vsako neodvisno mnozico iz C_k
        slovarVozliscaNeod = {}
        #seznam v katerem shranimo sestevek utezi za vsako neodvisno mnozico cikla C_k
        for p in neodC_k:
            # st korakov < Fib(k)*k/2
            # O( (1+sqrt(5))/2)^k * k )
            vsota = 0
            for j in p:
                vsota += weights[j][root]
            slovarVozliscaNeod[p] = vsota


        for neod in neodC_k:
            #za vsako neodvisno mnozico cikla C_k poisce maksimalno neodvisno mnozico v naslednikih
            #Casovna zahtevnost zanke:
            #st korakov <<  Fib(k)*Fib(k)*Fib(k) PS:Zelo groba ocena, za binarna drevesa se nam en Fib(k) spremeni v 2!
            #O( (1+sqrt(5))/2)^2k *n)) oziroma O( (1+sqrt(5))/2)^2k *2)) za binarno drevo
            seznam=[]
            #seznam v katerem shranjujemo maksimalno neodvisno mnozico vsakega naslednika
            for i in nasledniki:
                #st korakov za vsakega naslednika < max(len(neodC_k[neod))=Fib(k)
                #casovna zahtevnost ostalih operacij ni odvisna od n ali k
                najboljsi = (0, [])
                for neomn in neodC_k[neod]:
                    novaVrednost = izracunani[i][neomn][0]
                    if novaVrednost >najboljsi[0]:
                            najboljsi=(novaVrednost,(neomn,izracunani[i][neomn][1]))
                seznam.append(najboljsi)

            vsota=slovarVozliscaNeod[neod]
            seznamVozl=[]
            for vozu in neod:
                #st korakov < Fib(k)
                seznamVozl += [(vozu, root)]
            for (a,b) in seznam:
                #St korakov < n, ce je binarno <=2
                vsota +=a
                if len(b)!=0:
                    seznamVozl+=b[1]
            slovarVozlisca[neod] = (vsota,seznamVozl)



        izracunani[root] = slovarVozlisca


def maxCycleTreeIndependentSet(T, w):
    izracunani = {}
    k = len(w)
    neodC_k = slovNeodMnC_k(k)
    maxIndeTree(T, w, 0, T[0], izracunani, neodC_k)
    return max([izracunani[0][a] for a in neodC_k])


T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],
     [3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
     [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],
     [5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]


