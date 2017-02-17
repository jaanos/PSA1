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
spremeni napisane rekurzivne zveze, tudi ko nastopi najzahtevnejši problem, vse dimezije lihe.   
Sedaj na `T(a) = 7 * T(a/2) + O(a^2)` uporabimo krovni izrek in dobimo in dobimo časovno zahtevnost reda `O(a^log_2(7))`.


#### Prostorska zahtevnost
Definiranje vseh dimenzij v spremenljivke porabi konstantno časa, prav tako tudi reference na dele vhodnih matrik.   
Za razliko od časovne zahtevnosti, se prostor, ko pridemo iz enega rekurzivnega klica, sprosti oz. porabimo le toliko 
prostora, kot ga porabi najpožrešnejši rekurzivni klic. Vse nadaljne operacije porabijo kvečjemu "kvadratičen" prostor.   
Da lažje analiziramo maksimalni red zasedenega prostora, predpostavimo `a = max{m,n,k}`. S pomočje tega dobimo rekurzivno
zvezo `S(a) = S(a/2) + O(a^2)`, kjer so vse konstante skrite v notaciji. Iz nje dobimo prostorsko zahtevnost `O(a^2)`.



### CheapMatrix
Algoritem se izvaja isto, kot FastMatrix, razlika je, da tukaj pazimo na prostor, ko definiramo `P1,...,P7`. Uporabljamo
delovne matrike oz. delovno matriko, ki jo spreminjamo tekom izvajanja. Pazimo tudi pri seštevanju in množenju, da
prepisujemo že obstoječe matrike oz da si dodatne vmesne matrike shranjujemo v delovno matriko, tako da ne porabimo 
dodatno prostora z začasnimi matrikami.

#### Časovna zahtevnost
Časovna zahtevnost je v teoriji enaka FastMatrix-u, saj uporabljamo isto metodo množenja. Časovna zahtevnost je torej 
`O(a^log_2(7))`, pri čemer je `a = max{m,n,k}`.

#### Prostorska zahtevnost
Naša naloga je bila zmanjšati porabljen dodatni prostor, kar smo naredili s pomočjo delovne matrike. V vsakem koraku 
rekurzije smo porabili konstantni čas, torej `O(1)`, saj reference na dele matrik porabijo `O(1)`, vse ostale operacije
množenja in deljenja pa so uporabljale delovno matriko, tako da niso zavzemale dodatnega prostora.   
Rekurzivna zveza za zahtevnost algoritma je torej `S(m,n,k) = S(m/2,n/2,k/2) + O(1)`.   
Definirajmo `a = max{m,n,k}`, kar nam da: `S(a) = S(a/2) + O(1)` Iz tukaj dobimo, da je zahtevnost reda `O(log(a))`.   
To je tudi logicno, saj gremo log_2(a)-krat v rekurzijo, v vsakem koraku pa porabimo konstantno prostora.

## Primerjava

### Časovna zahtevnost

Po časovni zahtevnosti se FastMatrix in CheapMatrix ne razlikujeta, sta pa oba hitrejša od SlowMatrixa oz. imata 
manjšo časovno zahtevnost.

### Prostorska zahtevnost

Najmanj prostora porabi SlowMatrix, torej naivno množenje, saj porabi le konstanto. Sledi mu CheapMatrix, nato pa še 
FastMatrix.

### Izvajalni časi

V tabeli so dejanski časi izvajanja (oz. povprečje 10ih izvajanj), za množenje matrik dimenzij 
`m × n` in `n × k` s samimi enkami. Vse vrednosti so predstavljene v sekundah.

Dimenzije(m,n,k)|SlowMatrix|FastMatrix|CheapMatrix
---|---|---|---
m=10,n=10,k=10|0.00564|0.03691|0.02594
m=25,n=25,k=25|0.05657|0.31830|0.23621
m=50,n=50,k=50|0.46255|2.18726|1.63369
m=100,n=100,k=100|4.34777|15.36482|11.50693
m=250,n=250,k=250|104.36355|129.19715|101.67918
m=500,n=500,k=500|1395.09151|904.66493|717.38643

Kot vidimo v tabeli in kot je bilo pričakovano, je za majhne dimenzije najhitrejši SlowMatrix, saj ima časovno zahtevnost
odvisno le od vhodnih podatkov, ne pa še od konstant. Čim večja je dimenzija, tem hitrejša, v primerjavi z SlowMatrix, 
postajata Fastmatrix in CheapMatrix. Zanimivo pa je videti, da so tudi razlike med FastMatrix in CheapMatrix kar opazne, 
tudi za 30%. To je posledica manjše prostorske porabe algoritma CheapMatrix.   
Iz tukaj vidimo, da je za majše matrike boljše uporabljati navadno množenje, za večje (tukaj vidimo, da že za 500) 
pa optimizirane variante Strassenovega algoritma. Prav tako pa nam to pokaže, da red časovne zahtevnosti oz `O` notacija 
ne pokaže vedno cele zgodbe o hitrosti.

