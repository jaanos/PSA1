# Poročilo

*Luka Avbreht*

## Opis problema

V nalogi implementiramo algoritem za iskanje najtežje neodvisne množice v kartezičnem produktu drevesa in cikla.

Kot vhodne podatke algoritem sprejme drevo T in pa matriko w, ki predstavlja tabelo tež vozlisc v kartezicnem produktu.

```
w = w[index_v_ciklu][index_v_drevesu]
```

Problem si predstavljamo kot drevo na katerem je vsako vozlisce cikel. Na to vsak cikel oznacimo z nizom enic in nicel, 
ki predstavljajo zaporedje izbranih in neizbranih vozlisc v ciklu, ter s pomocjo njih dolocimo mozne oblike potomcev v 
drevesu.

Alogritem deluje na principu rekurzije. V prvem koraku za deblo maximiziramo vrednost glede na obliko debla, ter funkcijo 
rekurzivno pokliceo na njegovih sinovih, ob temu da se zavedamo, da smo za obliko oceta izbrali dolocen vzorec. V vsakem 
koraku rekurzije tako funkcijo razdelimo na toliko delov, kolikor otrok ima posamezno vozlisce.

V nasem primeru ko imamo opravka z binarnim drevsom z 13 vozlisci, in pa ciklom dolzine 4 tako algoritem deluje na 
priblizno sledeci nacin
```python
>>> T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
>>> w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],
...      [3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
...      [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],
...      [5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]
>>> maxCycleTreeIndependentSet(T, w)
(153, [(0, 0), (2, 0), (1, 1), (3, 1), (0, 3), (2, 3), (0, 4), (2, 4), (1, 5), (3, 5), (1, 6), (3, 6), (1, 7), (3, 7), (1, 8), (3, 8), (0, 9), (2, 9), (0, 10), (2, 10), (0, 11), (2, 11), (1, 12), (3, 12), (0, 13), (2, 13)])
```

* V prvem koraku poklicemo funkcijo na izhodiscu, ter za obliko njegovega oceta nastavimo prazen cikel ("0000")
* Nato maximiziramo vse mozne oblike izhodiscnega cikla kot sina navideznega praznega cikla, ter funkcijo rekurzivno 
poklicemo na poddrevesih z ihodisci v 1 in v 2 ter v nasem primeru ocetom oblike "1010"
* Vsako od izracunanih funkciji shranimo v slovar, kajti lahko se nam zgodi da v prihodnje kdaj poklicemo funkcijo na enakem primeru
* Tako isaknje taksne mnozice rekurzivno nadaljujemo dokler ne pridemo do listov drevesa
* V vsakem koraku s seboj vzamemo tudi podatek o temu katera vozlisca smo izbrali, da le to lahko kasneje vremo kot nas izbrani graf

## Časovna zahtevbnost 

## Prostorska zahtevnost

## Tablea časov izvajanja programa pri razlicnih vhoodnih podatkih
 
Za testni primer smo algoritem izvajali na uravnotezenih binarnih drevesih z vedno vecjo globino (polnih binarnih drevesih)

Globina drevesa\dolzina cikla |  3  |  5  |  7  |  10  |  15 
----------------------------------|--------------|-------------|-----------------|-----------------|-----------------
     2 | To be tested | To be tested | To be tested | To be tested | To be tested 
     3 | To be tested | To be tested | To be tested | To be tested | To be tested 
     4 | To be tested | To be tested | To be tested | To be tested | To be tested
     5 | To be tested | To be tested | To be tested | To be tested | To be tested
     6 | To be tested | To be tested | To be tested | To be tested | To be tested
     7 | To be tested | To be tested | To be tested | To be tested | To be tested
     8 | To be tested | To be tested | To be tested | To be tested | To be tested
     9 | To be tested | To be tested | To be tested | To be tested | To be tested
     10 | To be tested | To be tested | To be tested | To be tested | To be tested
     11 | To be tested | To be tested | To be tested | To be tested | To be tested
     12 | To be tested | To be tested | To be tested | To be tested | To be tested