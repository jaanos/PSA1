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
