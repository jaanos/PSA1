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
`V(1) = 2 in V(2) = 3,`
katere rešitev je:
`V(k) = ((1 + sqrt(5))/2)^k`

Algoritem za večjo preglednost vsebuje več pomožnih fukcij in sicer:

### vzorciZaPot(k)

#### Opis funkcije vzorciZaPot(k)
Ta fukcija ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k oblike [0, 1, 0, 0, 0], kjer
dve sosednji vrednosti nista hkrati enaki 1. Drugi seznam vrne iste vzorce kot prvi seznam, vendar v obliki števila,
ki ga predstavlja vzorec, če si ga predstavljamo kot število v binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaPot(k)
*k = 0, 1, 2, 3: T(k) = O(1)*
*sicer : T(k) = T(k-2) + T(k-1) + O(1) = 2*T(k-2) + T(k-3) + O(1) = 3*T(k-3) + 2*T(k-2) +O(1) =
        = ... =
        = O((V(k))^k)
#### Prostorska zahtevnost funkcije vzorciZaPot(k)
O((V(k))^k)

### vzorciZaCikel(k)

#### Opis funkcije vzorciZaCikel(k)
Ta fukcija s pomočjo funkcije VzorciZaPot(k) ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k
oblike [0, 1, 0, 0, 0], kjer dve sosednji vrednosti ter prva in zadnja vrednost nista hkrati enaki 1. Drugi seznam vrne
iste vzorce kot prvi seznam, vendar v obliki števila, ki ga predstavlja vzorec, če si ga predstavljamo kot število v
binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaCikel(k)
T(k) = T(klic funkcije vzorciZaPot(k-2)) + T(klic funkcije vzorciZaPot(k-3))
        + 2 * O(V(k-2)) + 2* O(V(k-3))=
        = O(n^(k-2)) + O(n^(k-3)) + 2 * O(((1 + sqrt(5))/2)^(k-3)*((1+sqrt(5))/2)+1)
T(k) = O(n^(k-2)) + O(n^(k-3)) = O(n^(k-3)*(n+1)) = O(n^(k-3)*n)
#### Prostorska zahtevnost funkcije vzorciZaCikel(k)
P(k) = 2 * k * V(k) = 2 * k * ((1 + sqrt(5))/2)^k

### vsotaVzorca(indexVzorca, u)

#### Opis funkcije vsotaVzorca(indexVzorca, u)
izračuna vsoto, ki jo dobimo, če seštejemo uteži na vozliščih, ki ležijo n vozlišču u v drevesu in v ciklu na točkah,
ki ga prestavlja vzorec cikla z indeksom indexVzorca.

#### Časovna zahtevnost funkcije vsotaVzorca(indexVzorca, u)
V tej funkciji se sprehodimo skozi vzorec dolžine k, zato je časovna zahtevnost enaka O(k).

#### Prostorska zahtevnost funkcije vsotaVzorca(indexVzorca, u)
Shranjujemo si le vrednost vsota, zato je prostorska zahtevnost enaka O(1).

### slovarZdruzljivih(vzorci)

#### Opis funkcije slovarZdruzljivih(vzorci)
za množico vzorcev ustvari slovar združljivih vzorcev (vzorci so podani s števili, ki jih vzorci predstavljajo,
če na njih gledamo kot na dvojiški zapis števila). Za vsak vzorec nam poda indekse vzorcev, ki so združljivi z
našim vzorcem.

#### Časovna zahtevnost funkcije slovarZdruzljivih(vzorci)
v prvi zanki V(k)-krat izvedemo zanko, katere časovna zahtevnost je enaka O(V(k)). Skupna časovna zahtevnost je
torej enaka O(V(k)^(2)) = O(((1+sqrt(5))/2)^(2)).

#### Prostorska zahtevnost funkcije slovarZdruzljivih(vzorci)
V slovarju za vsak vzorec shranimo indekse vzorcev, ki so z njim združljivi, torej je prostorska zahtevnost
navzgor omejena z O(V(k)^(2)) = O(((1+sqrt(5))/2)^(2)).

### nothing(u)

#### Opis funkcije nothing(u)
Ta funkcija ne naredi ničesar ter vrne True.

#### Časovna zahtevnost funkcije nothing(u)
O(1)

#### Prostorska zahtevnost funkcije nothing(u)
O(1)

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
O(m) + O(n) klicev funkcij previsit in postvisit

#### Prostorska zahtevnost funkcije DFS(G, roots = None, previsit = nothing, postvisit = nothing)
TODO

## število vzorcev cikla dolžine k
če na začetek postavimo 0, imamo za naslednjih k-1 mest V(k-1) možnost, če na začetek postavimo 1, moramo na drugo mesto
postaviti 0 in imamo tako za preostali del vzorca V(k-2) možnosti.
Dobimo torej rekurzivno formulo
V(k) = V(k-1) + V(k-2)
z začetnima vrednostma
V(1) = 2 in V(2) = 3,
katere rešitev je:
V(k) = ((1 + sqrt(5))/2)^k


Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
