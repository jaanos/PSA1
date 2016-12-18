# Poročilo

*Eva Zmazek*

##1.del: SlowMatrix:
Opis množenja matrik:
Dve matriki A in B lahko množimo med seboj, če je število stolpcev leve matrike enako številu vrstic desne matrike.
Njun produkt je enak matriki C velikosti nXm, pri čemer je n enako številu vrstic prve matrike in m številu stolpcev druge matrike.
(i,j)-ti element matrike c je enak skalarnemu produktu i-te vrstice matrike A in j-tega stolpca matrike B.

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
velikosti vhodnih matrik (gledala sem pridukt dveh kvadratnih matrik, keterih vsi elementi so bili enaki 1)
1x1 * 1x1 : 0.000s
5x5 * 5x5 : 0.001s
10x10 * 10x10 : 0.005s
15x15 * 15x15 : 0.012s
20x20 * 20x20 : 0.024s
25x25 * 25x25 : 0.052s
30x30 * 30x30 : 0.087s
35x35 * 35x35 : 0.152s
40x40 * 40x40 : 0.259s
45x45 * 45x45 : 0.429s
50x50 * 50x50 : 0.510s
55x55 * 55x55 : 0.611s
60x60 * 60x60 : 0.948s
65x65 * 65x65 : 1.176s
70x70 * 70x70 : 1.405s
75x75 * 75x75 : 1.759s
80x80 * 80x80 : 2.257s
85x85 * 85x85 : 2.600s
90x90 * 90x90 : 3.295s
95x95 * 95x95 : 4.185s
100x100 * 100x100 : 4.411s
125x125 * 125x125 : 9.514s
150x150 * 150x150 : 16.268s
175x175 * 175x175 : 28.596s
200x200 * 200x200 : 46.541s
225x225 * 225x225 : 71.574s
250x250 * 250x250 : 105.487s
275x275 * 275x275 : 149.519s
300x300 * 300x300 : 207.473s
350x350 * 350x350 : 359.316s
400x400 * 400x400 : 596.140s
450x450 * 450x450 : 944.968s
500x500 * 500x500 : 1392.869s



##2.del: FastMatrix:
###Opis algorima FastMatrix:
V metodi FastMatrix si najprej sharnimo velikosti matrik A in B, ki jih dobimo s pomočjo ukazov ".ncol" in ".nrow", nato pa pogledamo, ali je katera od dimenzij enaka 1.
Če je, matriki A in B pomnožimo med seboj tako kot pri metodi SlowMatrix (torej po naivni metodi), sicer se pa osredotočimo na primer, ko so
vse tri dimenzije sode. Takrat lahko namreč na matrikah A in B uporabimo Strassenov algoritem, kjer vsako od matrik A in b razdelimo na štiri dele, nato pa s pomočjo matrik P1,P2,P3,P4,P5,P6,P7 rekurzivno
izračunamo produkt. Posebnost tega algoritma je, da namesto osem množenj uporabimo sedem.
V primeru, ko število vrstic matrike A ni sodo, torej je liho, zadnjo vrstico obravnavamo posebaj. Torej matriko A brez zadnje vrstice pomnožimo z matriko B,
njen prosukt pa shranimo v končni matriki v del matrike brez zadnje vrstice. Zadnjo vrstico končne matrike pa dobimo tako, da zadnjo vrstico matrike A pomnožimo
z matriko B. V primeru, ko je število stolpcev v matriki B liho, zadnji stolpec matrike B obravnavamo posebej. Torej matriko A pomnožimo najprej z matriko B brez
zadnjega stolpca in njun prosukt shranimo v končni matriki brez zadnjega stolpca. Zadnji stolpec končne matrike izračunamo s produktom matrike A in zadnjim
stolpcem matrike B. v primeru, ko pa imamo število stolpcev matrike A, torej tudi število vrstic matrike B, liho, končno matriko produkta dobimo kot vsoto
produkta matrike A brez zadnjega stolpca in matrike B brez zadnje vrstice ter produkta zadnjega stolpca matrike A in zadnje vrstice matrike B.
Vrnemo produkt C

###Časovna zahtevnost algoritma:
Pri študiju časovne zahtevnosti bomo vzeli najslabši možen primer, torej primer, ko so vse tri dimenzije liha števila.
Najprej za shranjevanje dimenzih porabimo O(1) časa, nato porabimo O(k*m) dodatnega časa za izračun zadnje vrstice produkta. V naslednjem koraku porabimo O(n*k) dodatnega časa za
izračun zadnjega stolpca produkta. V nasljenjem koraku 'popravimo' lihost števila stolpcev matrike A in tevila vrstic matrike B, v katerem porabimo za
drugi del vsote O(m*n) dodatnega časa, za produkt zdaj že matrik sodih dimenzij pa porabimo O(8)=O(1) dodatnega časa za izpis 'četrtinskih delov' matrik A in B,
O(max(m,n)*k) dodatnega časa za seštevanje, ter T(n//2, k//2, m//2) dodatnega časa za vsako množenje, ki jih je 7.
Skupna časovna zahtevnost je torej
T(n,k,m) = O(1) + O(k*m) + O(n*k) + O(m*n) + o(1) + O(max(n,m)*k) + 7*T(n//2,k//2,m//2) =
         = O(1) + O(k*m) + O(n*k) + O(m*n) + O(max(n,m)*k) + 7*T(n//2,k//2,m//2)=
         = O(k*m+n*k+m*n) + O(max(n,m)*k) + 7*T(n//2,k//2, m//2)=...
V naslednjem koraku definiramo novo oznako M=max(n,k,m).
S to oznako dobimo sedaj, da je časovna zahtevnost metode FastMatrix enaka:
T(M) = O(3*M^2) + O(M^2) + 7*T(M//2) =
     = 3*O(M^2) + O(M^2) + 7*T(M//2) =
     = O(M^2) + 7*T(M//2) =
     = 7*T(M//2) + O(M^2)
Za nadaljno izpeljavo potrebujemo Krovni izrek, ki pravi:
    n...velikost vhoda
    a...število enako velikih podproblemov, na katere delimo problem
    b...velikost posameznega podproblema je n/b
    d...razdelitev na podprobleme in združitev porabita O(n^d)
    Če je T(n) = a*T(n/b) + O(n^d), potem je T(n) enak:
        1. O(n^d), če d>log_{b}(a)
        2. O(n^d*log_{b}(n)), če d=log_{b}(a)
        3. O(n^(log_{b}(a))), če d<log_{b}(a)
v našem primeru je n=M, a=7, b=2, d=2 (torej d<log_{b}(a))
Iz tega lahko do konca izpeljemo našo formulo:
T(M) = O(M^(log_{2}(7)))
(natančnejša izpeljava v komentarjih v kodi)

###Podatkovna zahtevnost algoritma:
Tudi pri študijo podatkovne zahtevnosti bomo vzeli najslabši možni primer, torej primer, ko so vse tri dimenzije liha števila. Opazimo, da pri "popravljanju" matrik
porabimo konstantno dodatno prostora. Tudi za shranjevanje dimenzij porabimo konstantno dodatnega prostora. Za zapis 'četrtinskih delov' matrik A in B porabimo
O(n//2*k//2+k//2*m//2)=O(n*k+m*k)=O(k*(m+n)) dodatnega prostora. Matrike P1,P2,P3,P4,P5,P6,P7 so velikosti n//2*m//2, za zapis vsake od njih porabimo O(n/2*m/2)=O(n*m)
dodatnega prostora, zaradi rekurzivnega klica pa v tem koraku porabimo še 7*P(n//2,k//2,m//2).
Skupna podatkovna zahtevnost je torej:
P(n,k,m) = O(1) + O(1) + O(k*(n+m)) + O(n*m) + 7*P(n//2,k//2,m//2)=
         = O(1) + O(k*n + k*m + n*m) + 7*P(n//2,k//2,m//2)=
         = O(k*n + k*m + n*m) + 7*P(n//2, k//2, m//2)=...
(natančnejša izpeljava v komentarjih v kodi)
Spet si definiramo oznako M=max(n,k,m).
S to oznako dobimo sedaj, da je prostorska zahtevnost metode FastMatrix enaka:
P(M) = O(3*M^2) + 7*P(M//2) =
     = 3*O(M^2) + 7*P(M//2) =
     = O(M^2) + 7*P(M//2) =
     = 7*P(M//2) + O(M^2)
Po krovnem izreku je to torej spet enako:
P(M) = O(M^(log_{2}(7)))

###Primerjava dejanskih časov izvajanja algoritmov pri vhodih različne velikost:
velikosti vhodnih matrik:
1x1 * 1x1 : 0.000s
5x5 * 5x5 : 0.005s
10x10 * 10x10 : 0.036s
15x15 * 15x15 : 0.059s
20x20 * 20x20 : 0.276s
25x25 * 25x25 : 0.375s
30x30 * 30x30 : 0.439s
35x35 * 35x35 : 1.610s
40x40 * 40x40 : 1.732s
45x45 * 45x45 : 2.209s
50x50 * 50x50 : 2.597s
55x55 * 55x55 : 2.552s
60x60 * 60x60 : 2.832s
65x65 * 65x65 : 10.459s
70x70 * 70x70 : 10.772s
75x75 * 75x75 : 10.876s
80x80 * 80x80 : 12.187s
85x85 * 85x85 : 13.665s
90x90 * 90x90 : 14.492s
95x95 * 95x95 : 14.624s
100x100 * 100x100 : 17.824s
125x125 * 125x125 : 23.127s
150x150 * 150x150 : 81.869s
175x175 * 175x175 : 84.372s
200x200 * 200x200 : 119.964s
225x225 * 225x225 : 71.574s
250x250 * 250x250 : 105.487s
275x275 * 275x275 : 149.519s
300x300 * 300x300 : 207.473s
350x350 * 350x350 : 359.316s
400x400 * 400x400 : 596.140s
450x450 * 450x450 : 944.968s
500x500 * 500x500 : 1392.869s

##3.del: CheapMatrix:


vzorec
Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
