# Poročilo

*Sara Korat*



##SlowMatrix##

OPIS: Algoritem računa produkt dveh matrik po običajnem postopku.  Vzamemo i-to vrstico leve matrike in k-ti stolpec desne matrike, izračunamo njun skalarni produkt in dobimo element (i, k) v novi matriki. 

ANALIZA ZAHTEVNOSTI:  
* Če imamo matriki z dimenzijama `n x m` in `m x k`, imamo  __časovno zahtevnost__ `O(nmk)`, v posebnem primeru, ko imamo kvadratni matriki dimenzije `n x n`, je časovna zahtevnost `O(n^3).`
* 
