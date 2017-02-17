# Poročilo

*Eva Erzin*

## 1. Opis algoritma

Funkcija maxindepset predstavlja algoritem za iskanje maksimalne neodvisne množice v produktu cikla a k elementi in drevesa.
Najprej preverimo, če so dimenzije vseh vhodnih podatkov ustrezne in je graf zares neusmerjen.
Nato definiramo nekaj pomožnih funkcij, s pomočjo katerih bomo poiskali maksimalno neodvisno množico in njeno težo.
Kot vhodna podatka dobimo drevo T z *n* vozlišči, predstavljeno s tabelo sosednosti in dvodimenzionalno tabelo tež dimenzij *k x n*

### 1.1 independentCycleSubsets

Ta funkcija poišče vse možne neodvisne podmnožice v grafu. Za vsako število med *0* in *2^k* preveri, če njegov binarni zapis ustreza neodvisni podmnožici cikla *C_k* - preveri, da prvi in zadnji, ter po dva sosednja bita nista khrati enaka ena.
Element v vrnjeni množici je enak paru *(a, b)*, kjer je *b* število med *0* in *2^k*, *b* pa njegov binarni zapis.

### 1.2 compatibleDict

Ta funkcija sprejme seznam, ki ga generiramo s prejšnjo funkcijo in nato oštevilčimo s funkcijo enumerate(), vrne pa slovar kompatibilnih neodvisnih podmnožic. Če sta dve podmnožici kompatibilni (torej neodvisni) vemo, če na enakem mestu v ciklu khrati nimata enice. To zlahka preverimo z binarnim operatorjem *&*.

### 1.3 setWeight

Kot vhodne podatke sprejme neodvisno podmnožico cikla predstavjeno v binarnem zapisu in indeks *u*, ki predstavlja vozlišče v drevesu T. Vrne težo neodvisne podmnožice cikla *C_k*, če se ta nahaja v produktu cikla z u-tim elementom drevesa.

### 1.4 postvisit

Funkcijo postvisit bomo uporabili v algoritmu DFS, ki ga poznamo iz vaj in predavanj. Z njo bomo napolnili slovar max_weights, ki za vsako vozlišče *t* v drevesu T vsebuje slovar, katerega ključi so indeksi *i* neodvisnih podmnožic, vrednosti pa maksimalne teže, ki jih lahko dobimo, če na produktu cikla in drevesa za *t*-to vozlišče uporabimo neodvisno podmnožico cikla z indeksom *i*, ter seznam parov vseh potomcev vozlišča *t* v drevesu in indeksov neodvisnih podmnožic, ki smo jih izbrali na tistem mestu, da smo prišli do maksimalne vsote.

Najprej generiramo vse neodvisne podmnožice cikla *C_k*, jih oštevilčimo in nato generiramo še slovar kompatibilnih podmnožic. Ustvarimo še seznam *max_weights*, ki ga bomo napolnimo tekom izvajanja algoritma DFS z uporabo funkcije postvisit.
Težo maksimalne neodvisne podmnožice v kartezičnem produktu poiščemo tako, da poiščemo maksimum tež, ki jih lahko dobimo na prvem elementu drevesa z različnimi podmnožicami ciklov.
Dejansko maksimalno podmnožico dobimo iz pripadajočega seznama elementov drevesa in indeksov podmnožic.

## 2. Analiza časovne in prostorske zahtevnosti algoritma

### 2.1 independentCycleSubsets

Funkcija za 2^k števil preveri, če njihov binarni zapis ustreza neodvisni podmnožici cikla. Za to porabi *2^k x O(k) = O(k x 2^k)* časa. Število vseh neodvisnih podmnožic cikla s k elementi dobimo iz rekurzivne formule *N_k = N_(k-1) + N_(k-2)*, ki predstavlja premaknjeno Fibonaccijevo zaporedje z začetnima vrednostima *N_1 = 2* in *N_2 = 3*, njegova rešitev pa je *N = ((1+sqrt(5))/2)^k*. Porabimo torej *O(N = (1+sqrt(5))/2)^k)* prostora.

### 2.2 compatibleDict

Funkcija gre čez seznam vseh množic generiranih v prejšnjem koraku in za vsako izmed njih preveri, če je kompatibilna z vsemi ostalimi podmnožicami. Torej porabi *O(N^2)* časa.
V najslabšem primeru bi bile vse množice kompatibilne med sabo in bi za shranjevanje seznama kompatibilnosti porabili *O(N^2)* prostora.

### 2.3 setWeight

Časovna zahtevnost te funkcije je *O(k)*, saj za vsakega izmed k elementov opravimo eno primerjavo in morda še eno seštevanje. Ker je podmnožica že predstavljena v binarnem zapisu, porabimo le *O(1)* prostora za sprotno računanje.

### 2.4 postvisit

Funkcija postvisit za vsako vozlišče drevesa pregleda vse mogoče neodvisne podmnožice cikla, za vsako izmed njih gre čez seznam vseh sinov tega vozlišča, potem pa še čez vse neodvisne podmnožice, ki so kompatibilne s prvo množico. Za to porabi *c = O(N x y x N)*, kjer je *y* maksimalno število sinov vseh vozlišč. Ta funkcija polni slovar max_weights, ki porabi *O(n x N x y)* prostora, kjer je n število vseh vozlišč drevesa T.
Funkcija DFS porabi *O(m) + O(n) x c* časa in *O(n)* dodatnega prostora.
Na koncu moramo še sestaviti seznam vseh vozlišč v največji neodvisni množici. Za to porabimo *O(n x k)* časa, saj seznam čez katerega iteriramo za vsako vozlišče drevesa T vsebuje binarno predstavitev neodvisne množice, v kateri moramo poiskati vse člene, ki so enaki '1'. Za shranjevanje končnega seznama porabimo *O(n x k)* prostora.

## 3. Primerjava dejanskih časov izvajanja algoritma

Čase sem primerjala na binarnih drevesih različnih globin za fiksne dolžine ciklov.
Binarno drevo globine *m* ima *2^m - 1* elementov.

n... število elementov v drevesu

m... globina drevesa

k... dolžina cikla

|(m, n)\k|5|10|15|
|---|---|---|---|
|(2, 3)|0.00|0.01|0.63|
|(3, 7)|0.00|0.01|0.95|
|(4, 15)|0.00|0.03|1.79|
|(5, 31)|0.00|0.05|3.04|
|(6, 63)|0.00|0.13|5.67|
|(7, 127)|0.05|0.20|11.31|
|(8, 255)|0.02|0.50|22.55|
|(9, 511)|0.04|1.00|48.50|
|(10, 1023)|0.14|1.99|108.40|
|(11, 2047)|0.14|4.21|213.60|
|(12, 4095)|0.32|7.33|432.39|

