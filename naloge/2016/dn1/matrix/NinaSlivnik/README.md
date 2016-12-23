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

## Primerjava dejanskih časov izvajanja



Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
