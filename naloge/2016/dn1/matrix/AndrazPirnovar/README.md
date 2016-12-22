# Poročilo

*Andraž Pirnovar*

##Algoritmi:

### SlowMatrix
Algoritem zmnoži dve matriki velikosti `m × n` in `n × k`. Množi ju po principu skalarnega produkta. 
Prvo matriko bomo imenovali *left*, drugo pa *right*.

#### Časovna zahtevnost

Ker množimo po principu skalarnega produkta, porabimo `O(m*n*k)` operacij.


#### Prostorska zahtevnost
Začetni matriki porabita `m × n` in `n × k` prostora, torej skupaj `n*(m+k)` prostora.
Algoritem pri izvajanju skalarnega produkta shranjuje vmesne vrednosti v spremenljivko `v`, ki jo nato zapišemo na mesto 
`(i,j)`v novi matriki.
Ta spremenljivka porabi `O(1)` dodatnega prostora.

Prostorska zahtevnost tega algoritma je: `O(1)`



### FastMatrix
Algoritem uporablja varianto Strassenovega algoritma za matrike poljubnih velikosti.    
Če so dimenzije matrike sode, razdelimo matriko na 4 enake dele, s katerimi nato računamo naprej.   
Če pa je ena ali več dimenzij lihih, pa ločimo na podprimere, kot je opisano v dokumentaciji v algoritmu.


#### Časovna zahtevnost
Navaden Strassenov algoritem za množenje kvadratnih matrik porabi `O(n^log_2(7))`.   
Naš algoritem pa lahko množi matrike poljubnih dimezij. Največja časovna zahtevnost se pojavi pri računanju `P1, P2, ..., P7`, 
saj tam uporabimo rekurzijo. Če imamo matriki velikosti `m*n` in `n*k`, dobimo na tem koraku za časovno zahtevnost
rekurzivno zvezo: `T(m,n,k) = 7 * T(m/2,n/2,k/2) + 5 * O((m/2)*(n/2)) + 5 * O((n/2)*(k/2))`. 
Podrobnejši opis, kako do te zveze pridemo, je v algoritmu.   
Za izračun časovne zahtevnosti v `O` notaciji predpostavimo, da je `a = max{m,n,k}`. Sedaj se prejšnja rekurzivna zveza 
pretvori v: `T(a) = 7 * T(a/2) + O(a^2)`. Vse nadaljne operacije v algoritmu porabijo kvečjemu `O(a^2)` časa, kar pa ne 
spremeni napisane rekurzivne zveze.   
Sedaj na `T(a) = 7 * T(a/2) + O(a^2)` uporabimo krovni izrek in dobimo in dobimo časovno zahtevnost reda `O(a^log_2(7))`.


#### Prostorska zahtevnost
Definiranje vseh dimenzij v spremenljivke porabi konstantno časa, prav tako tudi reference na dele vhodnih matrik.   
Tako kot pri časovni zahtevnosti je tudi pri prostorski zahtevnosti največ prispevek pri izračunu `P1, P2, ..., P7`,
torej pri rekurziji. Vsak tak `P1, P2, ..., P7` porabi `O((m/2)*(k/2))` prostora za shranjenje. Ker se pri seštevanju 
ustvarijo dodatne začasne matrike, dobimo na tem koraku prostorsko zahtevnost 
`S(m,n,k) = 7 * S(m/2,n/2,k/2) + O((m/2)*(n/2)) + O((n/2)*(k/2))`.   
Izberemo `a = max{m,n,k}` in dobimo `S(a) = 7 * S(a/2) + O(a^2)`. Tudi tukaj maksimalna prostorska zahtevnost kasnejših
operacij ne preseže `O(a^2)`.   
Iz te rekurzivne zveze,`S(a) = 7 * S(a/2) + O(a^2)`, izračunamo, da je prostorska zahtevnost `O(a^log_2(7))`.

### CheapMatrix

#### Časovna zahtevnost

#### Prostorska zahtevnost

## Primerjava

### Časovna zahtevnost

### Prostorska zahtevnost

### Izvajalni časi