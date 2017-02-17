# Poročilo

*Janez Radešček*

## Opis algoritma

Algoritem vzame prvo pozlišče v drevesu. Zanj najde vse *delne cikle* z lastnostjo, da za vsaka sosednja vozlišča v ciklu nista oba hkrati v *delnem cikluu*. Za vsak *delen cikel* algoritem rekorzivno najde težo in uporabljena vozlišča na *pod drevesih*, ki nastanejo, če iz drevesa odstranimo prvo vozlišče. Seveda pri računanju teže *pod drevesa* izpustimo cikle, ki ne sovpadajo s ciklom vozlišča *predhodnika*.
Na koncu izberemo za prvo vozlišče v drevesu cikelj pri katerem bo skupna teža največja.

## Časovna zahtevnost

T = O(n*2^k)

## Prostorska zahtevnost

P = O(n*2^k)

## Primerjava časov

Globina drevesa\dolzina cikla | 2 | 4 | 6 | 8 | 10 |
----|----|---|----|---|---|
5 |0.00199|
10 |0.00100|
15 |0.00200|
20 |0.00300|
25 |0.00600|
30 |0.00300|
35 |0.00500|
40 |0.00500|
45 |0.00500|


0.00199
0.00100
0.00200
0.00300
0.00600
0.00300
0.00500
0.00500
0.00500
