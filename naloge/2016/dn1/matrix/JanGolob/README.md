# Poročilo
*Jan Golob*

Množimo matiki velikosti **m** x **k** in **k** x **n**
** g := max{m, n, k} **

## SlowMatrix
Uporablja naivno množenje matrik.

### Čas
Za vsak element v ciljni matriki porabimo k množenj. V ciljni matriki je m vrstic in n stolpcev.
Torej: Časovna zahtevnost je **T(k,n,m) = O(kmn) = O(g^3).**

### Prostor
Poleg vhodnih in končne matrike, SlowMatrix še prostor za začasno vsoto (spremenljivka vs v kodi).
To je dodatnega **O(ln(g))** prostora.


## FastMatrix
Rekurzivno uporablja [Strassenov algoritem](http://wiki.fmf.uni-lj.si/wiki/Strassenovo_mno%C5%BEenje_matrik) za bločne matrika. Ko naleti na liho dimenzijo matrike, jo osami in izračuna z algoritmom SlowMatrix

### Čas
Na nekem nivoju rekurzije za (m, k, n) velike matrike pomnnožimo 7 podmatrik, ki jih dobivamo s seštevanjem in odštevanjem, ne smemo pozabiti pa tudi na množenje "osamljenih" stolpcev oziroma vrstic. Za seštevanje in odštevanje porabimo O(g^2). In pravtako porabimo O(g^2) za množenje osamljenih stolpcev in vrstic (glej časovno zahtevnost SlowMatrix, le da je eden izmed m, k, n enak 1).
Torej: T(g) = 7 x T(g/2) + O(g^2). Po Krovnem izreku sledi **T(g) = O(g^[log_2(7)])**

### Prostor
Poleg vhodnih in končne matrike, FastMatrix porabi še 7 matrik velikosti m/2 x n/2 za izračun teh pa še 10 matrik iste velikosti. Spet ne smemo pozabiti prostor porabljen pri osamljenih vrsticah oz stolpcih, ki je O(ln(g)).
Torej: Dodatno porabimo **17 x O(mn/4) + O(ln(g))**

## CheapMatrix
Rekurzivno poteka CheapMatrix podobno kot FastMatrix, le da se porabi največ še ena matrika prostora.

### Čas
Algoritem je enak kot pri Fastmatrix, le da se shranjujjo stvari malce drugače. Zato po podobnem sklepu kot zgoraj pridemo do časovne zahtevosti **T(g) = O(g^[log_2(7)])**

### Prostor
Ko množimo naivno porabimo tako kot pri SlowMatrix O(log(g)) prostora, kar je ravno ena komponenta v matriki work
Pri Strassenovem algoritmu pa si bomo označili kam si bomo spravili kateri vmesni produkt

| self: |    |   | work: |    |
|-------|----|---|-------|----|
| P6    | P2 |   | P3    | P5 |
| P4    | P1 |   | P7    | M  |

