# Poročilo

*Sara Korat*



##SlowMatrix##

OPIS: Algoritem računana produkt dveh matrik po običajnem postopku.  Vzamemo i-to vrstico leve matrike in k-ti stolpec desne matrike, izračunamo njun skalarni produkt in dobimo element (i, k) v novi matriki. 

ANALIZA ZAHTEVNOSTI:  Če imamo matriki z dimenzijama `n x m` in `m x k`, imamo  časovno zahtevnost `O(nmk)`, v posebnem primeru, ko imamo kvadratni matriki dimenzije `n x n`, je časovna `O(n^3).`