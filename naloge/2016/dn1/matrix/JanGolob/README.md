# Poročilo

*Jan Golob*

Množimo matiki velikosti **m** x **k** in **k** x **n**

## SlowMatrix
Uporablja naivno množenje matrik.

### Čas
Za vsak element v ciljni matriki porabimo k množenj. V ciljni matriki je m vrstic in n stolpcev.
Torej je časovna zahtevnost O(kmn)

### Prostor
Poleg vhodnih in končne matrike, SlowMatrix še prostor za začasno vsoto (spremenljivka vs v kodi).
To je dodatnega O(ln(vs)) prostora.
