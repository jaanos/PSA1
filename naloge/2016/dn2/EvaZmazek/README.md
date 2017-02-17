# Poročilo

*Eva Zmazek*

## Opis algoritma:

Funkcija maxCycleTreeIndependentSet(T, w) najprej preveri, če se vse dimenzije ujemajo in vrne napako, če se ne.
V naslednjem koraku si pripravimo seznam vseh vzorcev za cikel dolžine k vsi_vzorci_za_cikel. Pripravimo si tudi
slovar, ki nam za vsak vzorec poda indekse vzorcev, ki so z njim združjivi. Da sta vzorca združjiva pomeni, da sta
lahko vzorca sosednjih vozlišč v drevesu, torej da je množica vozlišč v dveh sosednjih vozliščih grafa z
združljivima cikloma neodvisna množica. Pripravimo si tudi matriko, v kateri (i,j)-ti element predstavlja double
oblike (maksimalna vrednost, ki jo lahko doseže i-ti element drevesa, če na njem uporabimo j-ti vzorec, seznam doublov,
ki povedo na katerem vozlišču smo uporabili kateri vzorec). Z DFSjem poskrbimo, da se vrednosti polnijo v
pravilnem vrstnem redu in sicer od listov navzgor, dogled ne pridemo do korena. Na koncu pogledamo katera je največja
možna vrednost dosežena v korenu ter iz seznama parov vozlišč drevesa in vzorcev ciklov, uporabljenih na teh vozliščih
razberemo katere točke so vsebovane v največji neodvisni množici kartezičnega produkta drevesa in cikla.

V naslednjih računih bomo večkrat rabili izračun števila vzorcev.

### število vzorcev cikla dolžine k
Če na začetek vzorca postavimo 0, imamo za naslednjih k-1 mest V(k-1) možnost, če na začetek postavimo 1, moramo
na drugo mesto postaviti 0 in imamo tako za preostali del vzorca V(k-2) možnosti.
Dobimo torej rekurzivno formulo
`V(k) = V(k-1) + V(k-2)`
z začetnima vrednostma
`V(1) = 2 in V(2) = 3`,
katere rešitev je:
`V(k) = ((1 + sqrt(5))/2)^k`

Algoritem za večjo preglednost vsebuje več pomožnih fukcij in sicer:

### vzorciZaPot(k)

#### Opis funkcije vzorciZaPot(k)
Ta fukcija ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k oblike [0, 1, 0, 0, 0], kjer
dve sosednji vrednosti nista hkrati enaki 1. Drugi seznam vrne iste vzorce kot prvi seznam, vendar v obliki števila,
ki ga predstavlja vzorec, če si ga predstavljamo kot število v binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaPot(k)
`k = 0, 1, 2, 3: T(k) = O(1)`

`sicer : T(k) = T(k-2) + T(k-1) + O(1) = 2*T(k-2) + T(k-3) + O(1) = 3*T(k-3) + 2*T(k-2) +O(1) = ... = O((V(k)))`
#### Prostorska zahtevnost funkcije vzorciZaPot(k)
O((V(k)))

### vzorciZaCikel(k)

#### Opis funkcije vzorciZaCikel(k)
Ta fukcija s pomočjo funkcije VzorciZaPot(k) ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k
oblike [0, 1, 0, 0, 0], kjer dve sosednji vrednosti ter prva in zadnja vrednost nista hkrati enaki 1. Drugi seznam vrne
iste vzorce kot prvi seznam, vendar v obliki števila, ki ga predstavlja vzorec, če si ga predstavljamo kot število v
binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaCikel(k)
`T(k) = T(klic funkcije vzorciZaPot(k-2)) + T(klic funkcije vzorciZaPot(k-3))
        + 2 * O(V(k-2)) + 2* O(V(k-3)) = O(k*V(k))`

#### Prostorska zahtevnost funkcije vzorciZaCikel(k)
`P(k) = 2 * k * V(k) = 2 * k * ((1 + sqrt(5))/2)^k`

### vsotaVzorca(indexVzorca, u)

#### Opis funkcije vsotaVzorca(indexVzorca, u)
izračuna vsoto, ki jo dobimo, če seštejemo uteži na vozliščih, ki ležijo n vozlišču u v drevesu in v ciklu na točkah,
ki ga prestavlja vzorec cikla z indeksom indexVzorca.

#### Časovna zahtevnost funkcije vsotaVzorca(indexVzorca, u)
V tej funkciji se sprehodimo skozi vzorec dolžine k, zato je časovna zahtevnost enaka O(k).

#### Prostorska zahtevnost funkcije vsotaVzorca(indexVzorca, u)
Shranjujemo si le vrednost vsota, zato je prostorska zahtevnost enaka `O(1)`.

### slovarZdruzljivih(vzorci)

#### Opis funkcije slovarZdruzljivih(vzorci)
za množico vzorcev ustvari slovar združljivih vzorcev (vzorci so podani s števili, ki jih vzorci predstavljajo,
če na njih gledamo kot na dvojiški zapis števila). Za vsak vzorec nam poda indekse vzorcev, ki so združljivi z
našim vzorcem.

#### Časovna zahtevnost funkcije slovarZdruzljivih(vzorci)
v prvi zanki V(k)-krat izvedemo zanko, katere časovna zahtevnost je enaka `O(V(k))`. Skupna časovna zahtevnost je
torej enaka `O(V(k)^(2)) = O(((1+sqrt(5))/2)^(2))`.

#### Prostorska zahtevnost funkcije slovarZdruzljivih(vzorci)
V slovarju za vsak vzorec shranimo indekse vzorcev, ki so z njim združljivi, torej je prostorska zahtevnost
navzgor omejena z `O(V(k)^(2)) = O(((1+sqrt(5))/2)^(2))`.

### nothing(u)

#### Opis funkcije nothing(u)
Ta funkcija ne naredi ničesar ter vrne True.

#### Časovna zahtevnost funkcije nothing(u)
`O(1)`

#### Prostorska zahtevnost funkcije nothing(u)
`O(1)`

### postvisitSedem

#### Opis funkcije postvisitSedem(u,v):
za vozlišče u poiščemo za vsak vzorec najboljšo izbiro vzorcev na sinovih od vozlišča u, da dobimo čimvečjo vsoto.

#### Časovna zahtevnost funkcije postivsitSedem(u, v):
V tej funkciji se sprehodimo čez prvo zanko, ki opravi V(k) klicev, v katerih izračunamo vsoto na tem vzorcu in tem
vozlišču (kar nam vzame `O(1)` časa) ter se sprehodimo čez vse sinove vozlišča u,
nato pa še čez vse indekse združljivih vzorce (ki so navzgor omejeni s številom vzorcev `V(k)`). Primerjave znotraj
zadnje zanke porabijo `O(1)` časa.
Skupna časovna zahtevnost je torej enaka `O(V(k)*(stevilo sinov = konstanta)*V(k)) = O(V(k)^(2))`.

#### Prostorska zahtevnost funkcije postvisitSedem(u, v):
V vmesnih korakih si shranjujemo vrednost vsota, ki nam zasede O(1) prostora, vzorec, ki nam zasede O(k) prostora,
maximum, ki nam zasede `O(1)` prostora, seznam `sezna`, ki nam zasede O(n) prostora.
Skupna prostorska zahtevnost funkcije postvisitSedem(u, v) je torej enaka `O(1) + O(k) + O(1) + O(n)` = `O(max(n,k))`.

### DFS(G, roots = None, previsit = nothing, postvisit = nothing)

#### Opis funkcije DFS(G, roots = None, previsit = nothing, postvisit = nothing)
Rekurzivno iskanje v globino.
Graf G je podan kot seznam seznamov sosedov za vsako vozlišče.
Seznam roots določa vozlišča, iz katerih se začne iskanje - privzeto so to vsa vozlišča v grafu.
Spremenljivki previsit in postvisit določata funkciji, ki se izvedeta ob prvem oziroma zadnjem obisku
posameznega vozlišča. Kot vhod dobita trenutno vozlišče in njegovega predhodnika (oziroma None, če tega ni).
Da se algoritem nadaljuje, morata vrniti True; če vrneta False, se funkcija prekine in vrne False.
Če iskanje pride do konca, funkcija vrne True.

#### Časovna zahtevnost funkcije DFS(G, roots = None, previsit = nothing, postvisit = nothing)
`O(m) + O(n)` klicev funkcij previsit in postvisit

### Skupna časovna zahtevnost
`T(k,n) = T(ustvarimo si seznam ciklov) + T(urstvarimo si slovar združljivih ciklov) + T(DFS) + T(zapišemo prave točke) <=  O(2^k) + O(((1+sqrt(5))/2)^(2)) + n * O(V(k)^(2)) + n * k`

### Skupna prostorsk zahtevnost
`P(k,n) = P(ustvarimo si seznam ciklov) + P(ustvarimo si slovar združljivih ciklov) + P(DFS) + P(zapišemo prave točke) <= O(n * k * V(k))`


## Primerjava časov na drevesu z n vozlišči in cikli s k vozlišči

k\n | 10 | 20 | 50 | 70 |100
----|----|----|----|----|---
  2  | 0.001s| 0.001s | 0.002s| 0.002s | 0.003s
  5  | 0.002s| 0.002s | 0.004s| 0.009s | 0.010s
  10  |0.019s| 0.037s | 0.038s| 0.148s | 0.285 s
  15  |1.375s| 2.099s | 2.206s| 7.449s | 10.202s
  17 | 6.592s| 11.804s| - | - | -

 Vidimo, da vrednosti po stolpcih naraščajo veliko hitreje kot po vrsticah (posledica eksponentne časovne zahtevnosti
 v k in polinomske časovne zahtevnosti v n).



