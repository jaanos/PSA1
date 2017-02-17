# Poročilo



*Jure Hostnik*



### Kratek opis algoritma
`maxCycleTreeIndependentSet` kot argumenta sprejme drevo `T` in tabelo tež `w` ter tri neobvezne parametre:
`z` pove, na katerem vozlišču drevesa se nahajamo, `i` je seznam vseh dopustnih neodvisnih množic cikla pri trenutnem vozlišču drevesa,
`I` pa je seznam vozlišč, ki se nahajajo v poddrevesu drevesa `T` in imajo za koren trenutno vozlišlče.
Algoritem za vse možne neodvisne množice v ciklu pri korenu drevesa `T` rekurzivno reši problem za vsa poddrevesa, katerih koren je sin korena prvotnega drevesa
in pri tem upošteva le množice na ciklu, neodvisne od tiste, ki je bila izbrana prej, nato vrne maksimum vseh možnosti.



### Analiza časovne in prostorske zahtevnosti

`independentSets`, ` cycleIndependentSets`  in `independentNeighbours` imajo eksponentno časovno in prostorsko zahtevnost,
saj se število neodvisnih množic v ciklu povečuje sorazmerno kot narašča Fibonaccijevo zaporedje.
`decimate` in `subtrees` pa delujeta v polinomskem času, saj vsebujeta le `for` zanke dolžin kvečjemu `n`.
`decimate` zavzame malo manj prostora kot `T`, ker ima le eno vozlišče manj (manjkajo tudi ustrezne povezave).
`subtrees` zavzame trikrat toliko prostora kot `decimate`, ker vsebuje še dva seznama indeksov.
Torej imata `decimate` in `subtrees` polinomsko prostorsko časovn zahtevnost.
`maxCycleTreeIndependentSet` uporablja navedene funkcije in posledično sta časovna in prostorska zahtevnost polinomski v `n` in eksponentni v `k`.


### Primerjava dejanskih časov izvajanja algoritmov

|  k  | n   | čas |
| --- | --- | --- |
| 5 | 14 | 3.8515059144676798 |
| 4   | 14  | 0.42828725414712676  |
| 3  | 14 | 0.03168159865617781  |
| 2 | 14 | 0.008269405753480896 |
| 10 | 5 | 7.4499996500314865 |
| 5 | 5 | 0.008946594806502617 |
| 4 | 5 | 0.0029974802266679035 |
| 3 | 5 | 0.0008413242808273935 |
| 2 | 5 | 0.00046720795126020676|
| 10 | 1 | 0.001146496815294995 |
| 20 | 1 | 0.2869598236159163 |
| 30 | 1 | 124.04066074053333 |

S povečevanjem `k` se čas hitro veča, s povečevanjem `n` pa je naraščanje počasnejše.
Lahko sklepamo, da rezultati ustrezajo pričakovanim časovnim zahtevnostim.