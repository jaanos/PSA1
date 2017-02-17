# Poročilo

*Ime Priimek*

## Opis algoritma:

Funkcija maxCycleTreeIndependentSet(T, w) najprej preveri, če se vse dimenzije ujemajo in vrne napako, če se ne.
Algoritem za večjo preglednost vsebuje več pomožnih fukcij in sicer:

### VzorciZaPot(k)

#### Opis funkcije VzorciZaPot(k)
Ta fukcija ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k oblike [0, 1, 0, 0, 0], kjer
dve sosednji vrednosti nista hkrati enaki 1. Drugi seznam vrne iste vzorce kot prvi seznam, vendar v obliki števila,
ki ga predstavlja vzorec, če si ga predstavljamo kot število v binarni obliki.
#### Časovna zahtevnost funkcije VzorciZaPot(k)
TODO
#### Prostorska zahtevnost funkcije VzorciZaPot(k)
TODO

### VzorciZaCikel(k)

#### Opis funkcije VzorciZaCikel(k)
Ta fukcija s pomočjo funkcije VzorciZaPot(k) ustvari seznam dveh seznamov. Prvi vrne vse možne vzorce dolžine k
oblike [0, 1, 0, 0, 0], kjer dve sosednji vrednosti ter prva in zadnja vrednost nista hkrati enaki 1. Drugi seznam vrne
iste vzorce kot prvi seznam, vendar v obliki števila, ki ga predstavlja vzorec, če si ga predstavljamo kot število v
binarni obliki.
#### Časovna zahtevnost funkcije VzorciZaCikel(k)
TODO
#### Prostorska zahtevnost funkcije VzorciZaCikel(k)
TODO

### 

Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
