# Poročilo

*Eva Zmazek*

##1.del: SlowMatrix:
Opis množenja matrik:
Dve matriki A in B lahko množimo med seboj, če je število stolpcev leve matrike enako številu vrstic desne matrike.
Njun produkt je enak matriki C velikosti *nXm*, pri čemer je *n* enako številu vrstic prve matrike in m številu stolpcev druge matrike.
*(i,j)*-ti element matrike c je enak skalarnemu produktu *i*-te vrstice matrike A in *j*-tega stolpca matrike B.

###Opis algoritma SlowMatrix:
V metodi SlowMatrix si najprej sharnimo velikosti matrik A in B, ki jih dobimo s pomočjo ukazov ".ncol" in ".nrow", nato pa se sprehodimo čez tri for zanke.
Torej sprehodimo se čez vse vrstice prve matrike (prva for zanka) in vse stolpce druge matrike (druga for zanka), nato pa s tretjo for zanko izvedemo skalarni produkt,
izbran vrstice matrike A in izbranega stolpca matrike B. ta skalarni produkt nato shranimo v element matrike C, ki leži v isti vrstici, kot izbrana vrstica v prvi for zanki,
in istem stolpcu kot izbran stolpec druge for zanke.
Vrnemo matriko C.

###Časovna zahtevnost algoritma:
Če je matrika A velikosti mxn in matrika B velikosti nxp, potem je časovna zahtevnost algoritma enaka O(m*n*p).
To se vidi direktno iz algoritma, ker gremo čez m števil v prvi zanki, znotraj katere gremo čez p števil, znotraj te pa še čez n števil.
Z drugimi besedami, za vsak element v novi matriki C, velikosti mxp, moramo skalarno pomnožiti dva vektorja dolžine n, kar nam vzame O(n) časa.
Torej za matriko C, moramo izračunati m*n skalarnih produktov, iz tega pa sledi, da je časovna zahtevnost metode SlowMatrix O(m*n*p).

###Prostorska zahtevnost algoritma:
Od dodatnega prostora porabimo prostor za shranjevanje vrednosti "vrednost", ki jo skozi vse for zanke le spreminjamo in ne ustvarjamo vedno nove,
torej na koncu porabimo le O(1), torej konstantno veliko prostora.
Ta algoritem torej prostorsko ni zahtevem, medtem ko pa je časovno zelo zahteven.

###Primerjava dejanskih časov izvajanja algoritmov pri vhodih različne velikost:
velikosti vhodnih matrik (gledala sem produkt dveh kvadratnih matrik, keterih vsi elementi so bili enaki 1)

Velikost kvadratnih matrik A in B | čas izračuna
----------------------------------|--------------
    1x1 * 1x1 | 0.000s
    5x5 * 5x5 | 0.001s
    10x10 * 10x10 | 0.005s
    15x15 * 15x15 | 0.012s
    20x20 * 20x20 | 0.024s
    25x25 * 25x25 | 0.052s
    30x30 * 30x30 | 0.087s
    35x35 * 35x35 | 0.152s
    40x40 * 40x40 | 0.259s
    45x45 * 45x45 | 0.429s
    50x50 * 50x50 | 0.510s
    55x55 * 55x55 | 0.611s
    60x60 * 60x60 | 0.948s
    65x65 * 65x65 | 1.176s
    70x70 * 70x70 | 1.405s
    75x75 * 75x75 | 1.759s
    80x80 * 80x80 | 2.257s
    85x85 * 85x85 | 2.600s
    90x90 * 90x90 | 3.295s
    95x95 * 95x95 | 4.185s
    100x100 * 100x100 | 4.411s
    125x125 * 125x125 | 9.514s
    150x150 * 150x150 | 16.268s
    175x175 * 175x175 | 28.596s
    200x200 * 200x200 | 46.541s
    225x225 * 225x225 | 71.574s
    250x250 * 250x250 | 105.487s
    275x275 * 275x275 | 149.519s
    300x300 * 300x300 | 207.473s
    350x350 * 350x350 | 359.316s
    400x400 * 400x400 | 596.140s
    450x450 * 450x450 | 944.968s
    500x500 * 500x500 | 1392.869s



##2.del: FastMatrix:
###Opis algorima FastMatrix:
V metodi FastMatrix si najprej sharnimo velikosti matrik A in B, ki jih dobimo s pomočjo ukazov *".ncol"* in *".nrow"*, nato pa pogledamo, ali je katera od dimenzij enaka 1.
Če je, matriki A in B pomnožimo med seboj tako kot pri metodi *SlowMatrix* (torej po naivni metodi), sicer se pa osredotočimo na primer, ko so
vse tri dimenzije sode. Takrat lahko namreč na matrikah A in B uporabimo Strassenov algoritem, kjer vsako od matrik A in b razdelimo na štiri dele,
nato pa s pomočjo matrik P1,P2,P3,P4,P5,P6,P7 rekurzivno izračunamo produkt. Posebnost tega algoritma je, da namesto osem množenj uporabimo sedem.

V primeru, ko število vrstic matrike A ni sodo, torej je liho, zadnjo vrstico obravnavamo posebaj. Torej matriko A brez zadnje vrstice pomnožimo z matriko B,
njen prosukt pa shranimo v končni matriki v del matrike brez zadnje vrstice. Zadnjo vrstico končne matrike pa dobimo tako, da zadnjo vrstico matrike A pomnožimo
z matriko B. V primeru, ko je število stolpcev v matriki B liho, zadnji stolpec matrike B obravnavamo posebej. Torej matriko A pomnožimo najprej z matriko B brez
zadnjega stolpca in njun prosukt shranimo v končni matriki brez zadnjega stolpca. Zadnji stolpec končne matrike izračunamo s produktom matrike A in zadnjim
stolpcem matrike B. v primeru, ko pa imamo število stolpcev matrike A, torej tudi število vrstic matrike B, liho, končno matriko produkta dobimo kot vsoto
produkta matrike A brez zadnjega stolpca in matrike B brez zadnje vrstice ter produkta zadnjega stolpca matrike A in zadnje vrstice matrike B.
Vrnemo produkt C

###Časovna zahtevnost algoritma:
Pri študiju časovne zahtevnosti bomo vzeli najslabši možen primer, torej primer, ko so vse tri dimenzije liha števila.

Najprej za shranjevanje dimenzih porabimo *O(1)* časa, nato porabimo *O(k*m)* dodatnega časa za izračun zadnje vrstice produkta. V naslednjem koraku
porabimo *O(n*k)* dodatnega časa za izračun zadnjega stolpca produkta. V nasljenjem koraku 'popravimo' lihost števila stolpcev matrike A in
števila vrstic matrike B, v katerem porabimo za drugi del vsote *O(m*n)* dodatnega časa, za produkt zdaj že matrik sodih dimenzij pa
porabimo *O(8)*=*O(1)* dodatnega časa za izpis 'četrtinskih delov' matrik A in B, *O(max(m,n)*k)* dodatnega časa za seštevanje,
ter *T(n//2, k//2, m//2)* dodatnega časa za vsako množenje, ki jih je 7.
Skupna časovna zahtevnost je torej
```
T(n,k,m) = O(1) + O(k*m) + O(n*k) + O(m*n) + o(1) + O(max(n,m)*k) + 7*T(n//2,k//2,m//2) =
         = O(1) + O(k*m) + O(n*k) + O(m*n) + O(max(n,m)*k) + 7*T(n//2,k//2,m//2)=
         = O(k*m+n*k+m*n) + O(max(n,m)*k) + 7*T(n//2,k//2, m//2)=...
```
V naslednjem koraku definiramo novo oznako *M=max(n,k,m)*.
S to oznako dobimo sedaj, da je časovna zahtevnost metode FastMatrix enaka:
```
T(M) = O(3*M^2) + O(M^2) + 7*T(M//2) =
     = 3*O(M^2) + O(M^2) + 7*T(M//2) =
     = O(M^2) + 7*T(M//2) =
     = 7*T(M//2) + O(M^2)
```
Za nadaljno izpeljavo potrebujemo Krovni izrek, ki pravi:`
```
    n...velikost vhoda
    a...število enako velikih podproblemov, na katere delimo problem
    b...velikost posameznega podproblema je n/b
    d...razdelitev na podprobleme in združitev porabita O(n^d)
    Če je T(n) = a*T(n/b) + O(n^d), potem je T(n) enak:
        1. O(n^d), če d>log_{b}(a)
        2. O(n^d*log_{b}(n)), če d=log_{b}(a)
        3. O(n^(log_{b}(a))), če d<log_{b}(a)`
```
v našem primeru je *n*=*M*, *a*=7, *b*=2, *d*=2 (torej *d*<*log_{b}(a)*)
Iz tega lahko do konca izpeljemo našo formulo:

**T(M) = O(M^(log_{2}(7)))**

(natančnejša izpeljava v komentarjih v kodi)

###Podatkovna zahtevnost algoritma:
Tudi pri študijo podatkovne zahtevnosti bomo vzeli najslabši možni primer, torej primer, ko so vse tri dimenzije liha števila. Opazimo, da pri "popravljanju" matrik
porabimo konstantno dodatno prostora. Tudi za shranjevanje dimenzij porabimo konstantno dodatnega prostora. Za zapis 'četrtinskih delov' matrik A in B porabimo
O(n//2*k//2+k//2*m//2)=O(n*k+m*k)=O(k*(m+n)) dodatnega prostora. Matrike P1,P2,P3,P4,P5,P6,P7 so velikosti n//2*m//2, za zapis vsake od njih porabimo O(n/2*m/2)=O(n*m)
dodatnega prostora, zaradi rekurzivnega klica pa v tem koraku porabimo še 7*P(n//2,k//2,m//2).
Skupna podatkovna zahtevnost je torej:
```
P(n,k,m) = O(1) + O(1) + O(k*(n+m)) + O(n*m) + 7*P(n//2,k//2,m//2)=
         = O(1) + O(k*n + k*m + n*m) + 7*P(n//2,k//2,m//2)=
         = O(k*n + k*m + n*m) + 7*P(n//2, k//2, m//2)=...
```

Spet si definiramo oznako *M=max(n,k,m)*.
S to oznako dobimo sedaj, da je prostorska zahtevnost metode FastMatrix enaka:
```
P(M) = O(3*M^2) + 7*P(M//2) =
     = 3*O(M^2) + 7*P(M//2) =
     = O(M^2) + 7*P(M//2) =
     = 7*P(M//2) + O(M^2)
```
Po krovnem izreku je to torej spet enako:

**P(M) = O(M^(log_{2}(7)))**

(natančnejša izpeljava v komentarjih v kodi)
###Primerjava dejanskih časov izvajanja algoritmov pri vhodih različne velikost:
velikosti vhodnih matrik:

Velikost kvadratnih matrik A in B | čas izračuna
----------------------------------|--------------
    1x1 * 1x1 | 0.000s
    5x5 * 5x5 | 0.005s
    10x10 * 10x10 | 0.036s
    15x15 * 15x15 | 0.059s
    20x20 * 20x20 | 0.276s
    25x25 * 25x25 | 0.375s
    30x30 * 30x30 | 0.439s
    35x35 * 35x35 | 1.610s
    40x40 * 40x40 | 1.732s
    45x45 * 45x45 | 2.209s
    50x50 * 50x50 | 2.597s
    55x55 * 55x55 | 2.552s
    60x60 * 60x60 | 2.832s
    65x65 * 65x65 | 10.459s
    70x70 * 70x70 | 10.772s
    75x75 * 75x75 | 10.876s
    80x80 * 80x80 | 12.187s
    85x85 * 85x85 | 13.665s
    90x90 * 90x90 | 14.492s
    95x95 * 95x95 | 14.624s
    100x100 * 100x100 | 17.824s
    125x125 * 125x125 | 23.127s
    150x150 * 150x150 | 81.869s
    175x175 * 175x175 | 84.372s
    200x200 * 200x200 | 119.964s
    225x225 * 225x225 | 140.859s
    250x250 * 250x250 | 147.558s
    275x275 * 275x275 | 529.036s
    300x300 * 300x300 | 591.306s
    350x350 * 350x350 | 652.103s
    400x400 * 400x400 | 790.870s
    450x450 * 450x450 | 1109.650s
    500x500 * 500x500 | 1140.776s

##3.del: CheapMatrix:
###Opis algoritma SlowMatrix:
Metoda CheapMatrix deluje podobno kot metoda FastMatrix, razlikujeta se le v predelu, ko so vse dimenzije (torej število vrstic matrike A,
število stolpcev matrike A, ki je enako številu vrstic matrike B in število stolpcev matrike B) sode. Prilagajanje matrik do matrik
sodih dimenzij ostaja enako.

Algoritem v predelu računanja matrik sodih dimenzij uporablja dodatno delovno matriko, ki je enakih dimenzij kot končna matrika, torej n//2xm//2.
Ta matrika je tudi edini dodaten prostor, ki ga mnozenje matrik dodatno porabi poleg vhodnih matrik A in B ter končne matrike C.

Če še enkrat zapišemo Strassenov algoritem za množenje matrik:

```
  A' =   in   B' =
[ A B ]    [ E F ]
[ C D ]    [ G H ]
```

* *P1 = A (F - H)*,
* *P2 = (A + B) H*,
* *P3 = (C + D) E*,
* *P4 = D (G - E)*,
* *P5 = (A + D) (E + H)*,
* *P6 = (B - D) (G + H)* in
* *P7 = (A - C) (E + F)*.

```
                 C'=A'*B' =
[ P4 + P5 + P6 - P2         P1 + P2      ]
[      P3 + P4         P1 + P5 - P3 - P7 ]
```

Ugotovimo, da naenkrat potrebujemo le 4 vrednosti izmed (P1, P2, P3, P4, P5, P6 in P7).
Naša delovna matrika pa lahko naenkrat shrani 4 vrednosti (matrike) velikosti n//2 x m//2, kar pa je ravno velikost vseh
matrik P1, P2, P3, P4, P5, P6 in P7.

Če si delovno matriko in self matriko razdelimo na 4 dele:

```
      self =                work =
[   S1      S2  ]   [   D1      D2  ]
[   S3      S4  ]   [   D3      D4  ]
```

V algoritmu najprej želimo zapisati spodjni desni del končne matrike C', zato v S1 shranimo P5, v S2 shranimo P1, v S3
shranimo P3 in v S4 shranimo P7.
Za izračun vrednosti P1, P3, P5 in P7 smo pri množenjih za delovne matrike uporabili matrike D1, D2, D3 in D4.
Naši "work" in "self" matriki zdaj izgledata takole:

```
     self =                 work =
[   P5      P1  ]   [   D1      D2  ]
[   P3      P7  ]   [   D3      D4  ]
```
vrednosti S4 mora biti enaka P1 + P5 - P3 - P7, zato S4 najprej pomnožimo z (-1), nato pa ji prištejemo še S1 (P5) in S2 (P1)
ter odštejemo S3 (P3).

En del produkta C' smo s tem že izračunali. Sedaj želimo izračunati S2. Na položaju S2 imamo že matriko P1, prišteti pa ji
moramo še matriko P2. V ta namen si v D1 shranimo vrednost P2, ki jo izračunamo s pomočjo delovne matrike D2.

```
     self =                         work =
[   P5      P1  ]             [   P2      D2  ]
[   P3      -P7+P5+P1-P3  ]   [   D3      D4  ]
```

Sedaj novo vrednost D1 prištejemo vrednosti S2.

```
     self =                         work =
[   P5      P1+P2  ]          [   P2      D2  ]
[   P3      -P7+P5+P1-P3  ]   [   D3      D4  ]
```

S tem smo izračunali že drugi del produkta C'. Sedaj želimo izračunati S3. Na položaju S3 imamo že matriko P3, prišteti pa ji
moramo še matriko P4. V ta namen si v D2 shranimo vrednost P4, ki jo izračunamo s pomočjo delovne matrike D3.

```
     self =                         work =
[   P5      P1+P2  ]          [   P2      P4  ]
[   P3      -P7+P5+P1-P3  ]   [   D3      D4  ]
```
Sedaj novo vrednost D2 prištejemo vrednosti S3.

```
     self =                           work =
[   P5      P1+P2  ]             [   P2      P4  ]
[   P3+P4      -P7+P5+P1-P3  ]   [   D3      D4  ]
```

S tem smo izračunali že tretji del produkta C'. Sedaj želimo izračunati S1. Na položaju S1 imamo že matriko P5, prišteti pa ji
moramo še matriki P4 in P6 te odšteti matriko P2. V ta namen si v D3 shranimo vrednost P6, ki jo izračunamo s pomočjo delovne matrike D4.

```
     self =                           work =
[   P5      P1+P2  ]             [   P2      P4  ]
[   P3+P4      -P7+P5+P1-P3  ]   [   P6      D4  ]
```
vrednosti S1 mora biti enaka P5 + P4 + P6 - P2, zato S1 najprej prištejemo D2 (P4) in D3 (P6) ter odštejemo D1 (P2).

###Časovna zahtevnost algoritma:
Pri študiju časovne zahtevnosti bomo vzeli najslabši možen primer, torej primer, ko so vse tri dimenzije liha števila.

Najprej za shranjevanje dimenzih porabimo *O(1)* časa, nato porabimo *O(k*m)* dodatnega časa za izračun zadnje vrstice produkta. V naslednjem koraku
porabimo *O(n*k)* dodatnega časa za izračun zadnjega stolpca produkta. V nasljenjem koraku 'popravimo' lihost števila stolpcev matrike A in
števila vrstic matrike B, v katerem porabimo za drugi del vsote *O(m*n)* dodatnega časa, za produkt zdaj že matrik sodih dimenzij pa
porabimo *O(max(m,n)*k)* dodatnega časa za seštevanja in odstevanja,
ter *T(n//2, k//2, m//2)* dodatnega časa za vsako množenje, ki jih je 7.
Skupna časovna zahtevnost je torej
```
T(n,k,m) = O(1) + 7*T(n//2,k//2,m//2) + O(k//2 * m//2) + O((n+m)//2 * k//2) +
           O(n//2 * k//2) + O((n+m)//2 * k//2) + O(n//2 * m//2) + O(n*k) + O(k*m) + O(m*n) + O(n//2 * k//2) +
           O(n//2 * m//2) + O(k//2 * m//2) + O(n//2 * m//2) + O((n+m)//2 * k//2) + O(n//2 * m//2) =
         = O(1) + 7*T(n//2,k//2,m//2) + 5*O((n+m)//2 * k//2)+ 4*O(n//2 * m//2)+ O(n*k) + O(k*m) + O(m*n) =
         = O(1) + 7*T(n//2,k//2,m//2) + O((n+m)//2 * k//2) + O(n//2 * m//2)+ O(n*k) + O(k*m) + O(m*n) =
         = ...
```
V naslednjem koraku definiramo novo oznako *M=max(n,k,m)*.
S to oznako dobimo sedaj, da je časovna zahtevnost metode CheapMatrix enaka:
```
T(M) = O(3*M^2) + O(M^2) + 7*T(M//2) =
     = 3*O(M^2) + O(M^2) + 7*T(M//2) =
     = O(M^2) + 7*T(M//2) =
     = 7*T(M//2) + O(M^2)
```

Po Krovnem izreku sedaj velja:

**T(M) = O(M^(log_{2}(7)))**

(natančnejša izpeljava v komentarjih v kodi)

###Prostorska zahtevnost algoritma:
Tudi pri študijo podatkovne zahtevnosti bomo vzeli najslabši možni primer, torej primer, ko so vse tri dimenzije liha števila. Opazimo, da pri "popravljanju" matrik
porabimo konstantno dodatno prostora. Tudi za shranjevanje dimenzij porabimo konstantno dodatnega prostora. Za zapis 'četrtinskih delov' matrik A in B porabimo
O(n//2*k//2+k//2*m//2)=O(n*k+m*k)=O(k*(m+n)) dodatnega prostora. Matrike P1,P2,P3,P4,P5,P6,P7 so velikosti n//2*m//2, za zapis vsake od njih porabimo O(n/2*m/2)=O(n*m)
dodatnega prostora, zaradi rekurzivnega klica pa v tem koraku porabimo še 7*P(n//2,k//2,m//2).
Skupna podatkovna zahtevnost je torej:
```
P(n,k,m) = O(1) + O(1) + O(k*(n+m)) + O(n*m) + 7*P(n//2,k//2,m//2)=
         = O(1) + O(k*n + k*m + n*m) + 7*P(n//2,k//2,m//2)=
         = O(k*n + k*m + n*m) + 7*P(n//2, k//2, m//2)=...
```

Spet si definiramo oznako *M=max(n,k,m)*.
S to oznako dobimo sedaj, da je prostorska zahtevnost metode FastMatrix enaka:
```
P(M) = O(3*M^2) + 7*P(M//2) =
     = 3*O(M^2) + 7*P(M//2) =
     = O(M^2) + 7*P(M//2) =
     = 7*P(M//2) + O(M^2)
```
Po krovnem izreku je to torej spet enako:

**P(M) = O(M^(log_{2}(7)))**

(natančnejša izpeljava v komentarjih v kodi)


###Primerjava dejanskih časov izvajanja algoritmov pri vhodih različne velikost:
Velikost kvadratnih matrik A in B | čas izračuna
----------------------------------|--------------
    1x1 * 1x1 | 0.000s
    5x5 * 5x5 | 0.003s
    10x10 * 10x10 | 0.024s
    15x15 * 15x15 | 0.051s
    20x20 * 20x20 | 0.189s
    25x25 * 25x25 | 0.293s
    30x30 * 30x30 | 0.347s
    35x35 * 35x35 | 1.062s
    40x40 * 40x40 | 1.244s
    45x45 * 45x45 | 1.386s
    50x50 * 50x50 | 2.012s
    55x55 * 55x55 | 2.167s
    60x60 * 60x60 | 2.534s
    65x65 * 65x65 | 6.683s
    70x70 * 70x70 | 7.215s
    75x75 * 75x75 | 7.553s
    80x80 * 80x80 | 8.265s
    85x85 * 85x85 | 8.726s
    90x90 * 90x90 | 8.831s
    95x95 * 95x95 | 9.593s
    100x100 * 100x100 | 14.490s
    125x125 * 125x125 | 18.361s
    150x150 * 150x150 | 52.002s
    175x175 * 175x175 | 60.458s
    200x200 * 200x200 | 102.602s
    225x225 * 225x225 | 71.574s
    250x250 * 250x250 | 105.487s
    275x275 * 275x275 | 149.519s
    300x300 * 300x300 | 207.473s
    350x350 * 350x350 | 359.316s
    400x400 * 400x400 | 596.140s
    450x450 * 450x450 | 944.968s
    500x500 * 500x500 | 1392.869s

vzorec
Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
