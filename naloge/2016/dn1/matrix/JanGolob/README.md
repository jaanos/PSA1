# Poročilo

*Jan Golob*

Množimo matiki velikosti **m** x **k** in **k** x **n**

## SlowMatrix
Uporablja naivno množenje matrik.

### Čas
Za vsak element v ciljni matriki porabimo k množenj. V ciljni matriki je m vrstic in n stolpcev.
Torej je časovna zahtevnost O(kmn).

### Prostor
Poleg vhodnih in končne matrike, SlowMatrix še prostor za začasno vsoto (spremenljivka vs v kodi).
To je dodatnega O(ln(vs)) prostora.

## FastMatrix
Rekurzivno uporablja Strassenov algoritem za bločne matrika. Ko naleti na liho dimenzijo matrike, jo osami in izračuna z algoritmom SlowMatrix

### Čas
Na nekem nivoju rekurzije za (m, k, n) velike matrike pomnnožimo 7 podmatrik, ki jih dobivamo s seštevanjem in odštevanjem, ne smemo pozabiti pa tudi na množenje "osamljenih" stolpcev oziroma vrstic. Za seštevanje in odštevanje porabimo O(g^2), kjer je g := max{m, n, k}. In pravtako porabimo O(g^2) za množenje osamljenih stolpcev in vrstic (glej časovno zahtevnost SlowMatrix, le da je eden izmed m, k, n enak 1).
Torej: T(g) = 7 x T(g/2) + O(g^2). Po Krovnem izreku sledi T(g) = O(g log_2(7))
