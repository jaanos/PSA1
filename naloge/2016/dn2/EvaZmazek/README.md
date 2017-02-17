# Poročilo

*Eva Zmazek*

## Opis algoritma:

Funkcija maxCycleTreeIndependentSet(T, w) najprej preveri, če se vse dimenzije ujemajo in vrne napako, če se ne.
Algoritem za večjo preglednost vsebuje več pomožnih fukcij in sicer:

### vzorciZaPot(k)

#### Opis funkcije vzorciZaPot(k)
Ta fukcija ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k oblike [0, 1, 0, 0, 0], kjer
dve sosednji vrednosti nista hkrati enaki 1. Drugi seznam vrne iste vzorce kot prvi seznam, vendar v obliki števila,
ki ga predstavlja vzorec, če si ga predstavljamo kot število v binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaPot(k)
*k = 0, 1, 2, 3: T(k) = O(1)*
*sicer : T(k) = T(k-2) + T(k-1) + O(1) = 2*T(k-2) + T(k-3) + O(1) = 3*T(k-3) + 2*T(k-2) +O(1) = ... = O(2^k)*
#### Prostorska zahtevnost funkcije vzorciZaPot(k)
*O(k)*

### vzorciZaCikel(k)

#### Opis funkcije vzorciZaCikel(k)
Ta fukcija s pomočjo funkcije VzorciZaPot(k) ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k
oblike [0, 1, 0, 0, 0], kjer dve sosednji vrednosti ter prva in zadnja vrednost nista hkrati enaki 1. Drugi seznam vrne
iste vzorce kot prvi seznam, vendar v obliki števila, ki ga predstavlja vzorec, če si ga predstavljamo kot število v
binarni obliki.
#### Časovna zahtevnost funkcije vzorciZaCikel(k)
TODO
#### Prostorska zahtevnost funkcije vzorciZaCikel(k)
TODO

### vsotaVzorca(indexVzorca, u)

#### Opis funkcije vsotaVzorca(indexVzorca, u)
TODO

#### Časovna zahtevnost funkcije vsotaVzorca(indexVzorca, u)
TODO

#### Prostorska zahtevnost funkcije vsotaVzorca(indexVzorca, u)
TODO

### slovarZdruzljivih(vzorci)

#### Opis funkcije slovarZdruzljivih(vzorci)
TODO

#### Časovna zahtevnost funkcije slovarZdruzljivih(vzorci)
TODO

#### Prostorska zahtevnost funkcije slovarZdruzljivih(vzorci)
TODO

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


## število vzorcev poti dolžine k
vp(k) = vp(k-1) + vp(k-2) <= O(2^(k))
## število vzorcev cikla dolžine k
V(k) <= O(2^(k))
**V(k) = k + \bin{k}{2} + \bin{k}{3} + \bin{k}{4} + \bin{k}{5} + \bin{k}{6} + ... + \bin{k}{k//2} =
=-1 + 2^n - (2^(-1 + n) n Γ(1/2 + n/2) 2F1(1, 1 - n/2, (4 + n)/2, -1))/(sqrt(π) Γ(2 + n/2))**

Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
