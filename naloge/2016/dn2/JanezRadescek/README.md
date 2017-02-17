# Poročilo

*Ime Priimek*

## Opis algoritma

Algoritem vzame prvo pozlišče v drevesu. Zanj najde vse *delne cikle* z lastnostjo, da za vsaka sosednja vozlišča v ciklu nista oba hkrati v *delnem cikluu*. Za vsak *delen cikel* algoritem rekorzivno najde težo in uporabljena vozlišča na *pod drevesih*, ki nastanejo, če iz drevesa odstranimo prvo vozlišče. Seveda pri računanju teže *pod drevesa* izpustimo cikle, ki ne sovpadajo s ciklom vozlišča *predhodnika*.
Na koncu izberemo za prvo vozlišče v drevesu cikelj pri katerem bo skupna teža največja.

## Časovna zahtevnost

T = O(n*2^k)

## Prostorska zahtevnost

P = O(n*2^k)

## Primerjava časov

to do
