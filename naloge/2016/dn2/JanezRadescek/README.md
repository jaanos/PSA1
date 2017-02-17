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

Tabela časov za drevo z n elementi in cikli dolžine k.

n\k | 2 | 4 | 6 | 8 | 10 |
----|----|---|----|---|---|
5 |0.00199|0.00400|0.03602|0.29321|2.05245
10 |0.00100|0.00798|0.05407|0.59841|4.14690
15 |0.00200|0.01303|0.07713|0.78458|6.32449
20 |0.00300|0.01301|0.10110|0.89761|9.44086
25 |0.00600|0.01701|0.12980|1.14730|10.98793
30 |0.00300|0.01954|0.15261|1.42254|13.01337
35 |0.00500|0.02201|0.17316|1.96289|15.16936
40 |0.00500|0.02701|0.22084|2.04642|16.47726
45 |0.00500|0.02902|0.27820|2.05198|20.76434

![Image](https://github.com/JanezRadescek/PSA1/blob/janezDN2/naloge/2016/dn2/JanezRadescek/k5n5100.jpg)



