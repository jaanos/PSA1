# Poročilo

*Nina Slivnik*

## Kratek opis algoritmov
### SlowMatrix
SlowMatrix predstavlja množenje matrik po definiciji, torej skalarno množenje vrstic s stolpci. V ta namen uporabimo tri gnezdene for zanke.
### FastMatrix
FastMatrix deluje po principu Strassenovega množenja, torej imamo sedem produktov, ki jih nato seštejemo v bloke ciljne matrike:
Če vhodni matriki X in Y predstavimo kot

```
X = [[A B][C D]]
Y = [[E F][G H]]
```

dobimo produkte po sledečih formulah:

* P1 = A(F-H),
* P2 = (A+B)H,
* P3 = (C+D)E,
* P4 = D(G-E),
* P5 = (A+D)(E+H),
* P6 = (B-D)(G+H) in
* P7 = (A-C)(E+F),

Ciljna matrika pa je

```
X*Y = [[P4+P5+P6-P2 P1+P2][P3+P4 P1+P5-P3-P7]]
```

Bolj natančno: Vhodni matriki najprej razdelimo na največji matriki velikosti *n* x *m*, kjer sta *n* in *m* soda, ter preostanek, torej lahko ostaneta liha vrstica ali stoplec.
Sodi podmatriki zmnožimo po Strassenu, preostanek pa po definiciji.
### CheapMatrix
Tako kot FastMatrix, tudi CheapMatrix uporablja Strassenovo množenje, le da dobljene produkte shrani bodisi v ciljno bodisi v delovno matriko. Pri tem moramo paziti, da vhodni matriki ostajata nespremenjeni.
Produkte nato spet seštejemo v nekem določenem vrstnem redu.
Bolj natančno: Vhodni matriki najprej razdelimo na največji matriki velikosti *n* x *m*, kjer sta *n* in *m* soda, ter preostanek, torej lahko ostaneta liha vrstica ali stoplec.
Sodi podmatriki zmnožimo po Strassenu, preostanek pa po definiciji.
Imamo naslednje matrike:

```
X = [[A B][C D]]
Y = [[E F][G H]]
C = [[C11 C12][C21 C22]]
D = [[D11 D12][D21 D22]]
```


Zgled za *P1 = A(F-H)*:
*P1* bomo shranili v *C12*.
*F-H* bomo izračunali kar kot *F-=H*, da ne bomo porabili dodatnega prostora.
V *C12* zmnožimo *A* in trenutni *F*, torej imamo *P1* shranjen v *C12* (za delovno matriko pri tem uporabimo *D22*).
Zdaj samo še popravimo *F*, torej *F+=H*.

Zgled za *P5 = (A+D)(E+H)*:
*P5* bomo shranili v *D21*.
Najprej izračunamo *A+D* in *E+H* kot *A+=D* in *E+=H* ter ju zmnožimo 



## Analiza časovne in prostorske zahtevnosti
KROVNI IZREK
### SlowMatrix
Časovna zahtevnost: Za izračun produkta porabimo *O(mnk)*, kjer je *n* x *m* velikost ciljne matrike, *k* pa dolžina vektorjev, ki jih množoimo.
Prostorska zahtevnost: Ne porabimo nič dodatnega prostora, ker vmesne rezultate prištevamo direktno v ciljno matriko, torej O(1). 
### FastMatrix
Časovna zahtevnost: Časovna zahtevnost algoritma je *O(N^2.8)*, oz. *O(N^log_2(7))*, kjer je *N = max(m,n,k)* (vemo, da velja za Strassenov algoritem, uporabimo tudi krovni izrek).
Prostorska zahtevnost: Obravnavamo najslabši (najpočasnejši) primer, torej *m*, *n* in *k* so vsi lihi. Po krovnem izreku iz formule *S(N) = S(N/2) + 33/4 O(N^2)* oz. po krovnem izreku *S(N) = O(N^2)*.
### CheapMatrix
Časovna zahtevnost: Ker ponovno računamo po Strassenovem algoritmu, je prostorska zahtevnost spet enaka *O(n^2.8)*.
Prostorska zahtevnost: Najprej naredimo delovno matriko, ki je enake velikosti, kot ciljna matrika, torej *O(mn)*. Ostale operacije porabijo le konstanten čas (torej *O(1)*), ali pa imamo rekurzivne klice, torej največ *O(log(mnk))*.

## Primerjava dejanskih časov izvajanja
Za primerjavo si bomo ogledali delovanje vseh treh algoritmov na kvadratnih matrikah velikosti *2^n*, kjer je *n = 0,1,...,10*.


| Algoritem   | 1   | 2   | 4     | 8     | 16    | 32    | 64     | 128    | 256     | 512      |
|-------------|-----|-----|-------|-------|-------|-------|--------|--------|---------|----------|
| SlowMatrix  | 0.0 | 0.0 | 0.0   | 0.0   | 0.016 | 0.234 | 1.813  | 17.469 | 189.313 | 2080.521 |
| FastMatrix  | 0.0 | 0.0 | 0.016 | 0.031 | 0.266 | 1.625 | 10.609 | 76.578 | 507.703 | 3556.875 |
| CheapMatrix | 0.0 | 0.0 | 0.0   | 0.031 | 0.125 | 0.969 | 7.390  | 53.406 | 338.516 | 2600.891 |


Oglejmo si še graf, kjer je:
* SlowMatrix zelen,
* FastMatrix rdeč,
* CheapMatrix moder.

![Graf](https://github.com/SlivnikN/PSA1/tree/master/naloge/2016/dn1/matrix/NinaSlivnik/graf.png)

Vidimo, da je SlowMatrix najhitrejši, sledi mu CheapMatrix, najpočasnejši pa FastMatrix.



