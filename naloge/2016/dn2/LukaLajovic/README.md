# Poročilo

*Luka Lajovic*

Funkcija vse_neodvisne_na_ciklu sprejme celo število k in vrne vse neodvisne množice
v ciklu z dolžino k, izvede se samo enkrat, dobljene množice se shranijo.

funkcija komplemente sprejme seznam A in seznam seznamov in vrne indekse vseh seznamov, ki so disjunktni od A.

funkcija neodvisna je glavna funkcija po drevesu se sprehodi z iskanjem v globino.
Ko pride do listov shrani težo od vsake neodvisne množice na tem vozlišču.
Ko gre nazaj za vsako vozlišče drevesa, za vsako neodvisno množico na ciklu tega drevesa poišče največjo vrednost
svojih prednikov. Množica komplemente vrne vse disjunktne množice zato,
ko računamo vrednost neke neodvisne množice, na vozlišču, ki ni list ji moramo prišteti še največjo vrednost njegovih prednikov, ob čemer moramo ohraniti neodvisnost. hkrati se hranijo vsi elementi, za vsako vozlišče.

n je dolžina grafa, k je dolžina cikla

Prostorska zahtevnost bi morala biti 2^k  (n)2+2^k, ker imamo 2 slovarja 

Časovna zahtevnost je enaka sepravi O(n2^k) 
Testni primer
T, w iz navodil porabi 0.015624761581420898s
vrsta dolga 5001 z ciklom dolžine 2 potrebuje 1.6406400203704834s da reši nalogo
vrsta dolga 10001 z ciklom dolžine 2,  potrebuje 6.34376335144043s, da se reši nalogo
vrsta dolga 10001 z ciklom dolžine 4,  potrebuje 19.281786918640137s da se reši nalogo


drevo=[[1, 46, 47, 48], [0, 2, 28, 40, 44], [1, 3, 21, 25, 27], [2, 4, 20], [3, 5, 6, 12, 16, 18, 19], [4], [4, 7, 8, 9], [6], [6], [6, 10], [9, 11], [10], [4, 13], [12, 14], [13, 15], [14], [4, 17], [16], [4], [4], [3], [2, 22], [21, 23], [22, 24], [23], [2, 26], [25], [2], [1, 29, 33], [28, 30, 31], [29], [29, 32], [31], [28, 34, 36, 38, 39], [33, 35], [34], [33, 37], [36], [33], [33], [1, 41, 42], [40], [40, 43], [42], [1, 45], [44], [0], [0], [0]]


teze=[[4, 6, 0, 5, 15, 17, 18, 19, 10, 13, 6, 3, 1, 6, 0, 7, 18, 0, 7, 11, 6, 18, 11, 12, 3, 16, 4, 20, 0, 12, 7, 20, 14, 5, 14, 20, 2, 19, 6, 17, 11, 11, 5, 5, 10, 17, 18, 12, 19], [17, 17, 14, 9, 15, 12, 5, 19, 13, 9, 2, 6, 0, 18, 10, 13, 10, 20, 5, 6, 12, 16, 19, 14, 14, 8, 12, 19, 18, 13, 18, 17, 19, 15, 11, 17, 18, 13, 10, 18, 2, 7, 2, 7, 11, 13, 17, 12, 4], [15, 13, 17, 13, 8, 16, 8, 18, 8, 0, 4, 7, 17, 11, 9, 9, 11, 18, 13, 15, 8, 16, 5, 4, 9, 8, 11, 16, 6, 9, 0, 13, 6, 3, 16, 14, 4, 7, 13, 16, 17, 12, 18, 11, 16, 10, 18, 5, 0], [18, 0, 1, 4, 20, 8, 7, 17, 19, 20, 13, 15, 4, 7, 9, 0, 10, 9, 2, 0, 5, 5, 15, 5, 9, 6, 0, 7, 11, 3, 7, 0, 1, 20, 17, 6, 0, 16, 0, 13, 16, 17, 12, 18, 0, 15, 19, 19, 20], [12, 9, 15, 3, 17, 19, 2, 3, 0, 11, 10, 11, 4, 16, 19, 3, 17, 1, 19, 16, 13, 4, 1, 14, 10, 13, 4, 16, 19, 15, 16, 10, 17, 10, 2, 2, 9, 3, 19, 3, 5, 3, 11, 17, 11, 8, 19, 5, 10], [1, 15, 18, 5, 0, 17, 17, 17, 13, 0, 17, 7, 11, 18, 14, 14, 5, 11, 14, 15, 18, 18, 3, 5, 20, 10, 12, 6, 20, 13, 1, 14, 20, 17, 0, 13, 17, 12, 12, 19, 13, 19, 9, 20, 13, 1, 9, 4, 10], [16, 20, 12, 6, 18, 12, 9, 17, 8, 20, 0, 18, 0, 19, 0, 17, 6, 14, 16, 3, 1, 19, 8, 19, 12, 19, 17, 17, 0, 11, 15, 13, 8, 13, 17, 0, 20, 9, 10, 7, 1, 8, 8, 17, 18, 12, 13, 15, 8], [15, 11, 13, 7, 10, 14, 0, 17, 18, 6, 16, 19, 10, 3, 20, 11, 2, 14, 8, 8, 15, 16, 19, 11, 5, 3, 18, 19, 5, 4, 7, 3, 18, 2, 5, 9, 12, 13, 3, 13, 14, 3, 16, 7, 18, 14, 9, 8, 15], [17, 18, 15, 10, 0, 19, 0, 16, 17, 1, 4, 13, 17, 3, 13, 9, 16, 20, 1, 3, 8, 12, 13, 6, 5, 19, 12, 13, 4, 4, 1, 4, 6, 9, 9, 5, 20, 0, 13, 9, 10, 13, 17, 15, 4, 11, 11, 20, 2], [9, 9, 2, 19, 2, 15, 7, 6, 17, 19, 10, 3, 19, 0, 1, 11, 17, 3, 17, 10, 4, 4, 17, 19, 16, 11, 14, 17, 20, 10, 9, 11, 10, 16, 8, 0, 19, 5, 9, 7, 9, 7, 2, 1, 15, 0, 9, 11, 17]]


to drevo je ima 49 vozlišč
cikel pa ima dolžino 10
teža njegove najtežje neodvisne množice je 2789
in porabi 0.6406257152557373s
