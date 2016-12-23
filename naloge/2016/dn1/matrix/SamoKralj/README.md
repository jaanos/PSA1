# Poročilo

Samo Kralj

# SlowMatrix

SlowMatrix ima implementirano navadno množenje matrik. Torej za (i,j) člen v matriki bo izračunal 
skalarni produkt i-te vrstice in j-tega stolpca.

## Časovna Zahtevnost:

Če množimo matriki velikosti n x m in m x k, bo ciljna matrika velikosti n x k. Za vsak element v ciljni
matriki pa opravimo m operacij. Skupna časovna zahtevnost bo torej O(n*k*m).

## Prostorska Zahtevnost:

Prostor, ki ga porabi je velikost ciljne matrike.

# FastMatrix

FastMatrix ima implementirano Strassenovo množenje matrik. 
