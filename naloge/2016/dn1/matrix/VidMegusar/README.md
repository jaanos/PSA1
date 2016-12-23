# Poročilo

*Vid Megušar*

##**Opis Algoritmov**

**1) SlowMatrix**

Običajno množenje matrik, kot če bi ročno računali manjše matrike.
Ker imamo tri for zanke prvi dve po stolpcih(n) in vrsticah(m) prve matrike, tretjo pa po stopcih(k) druge matrike imamo časovno zahtevnost O(m\*n\*k).

**2)FastMatrix**

Zdaj za množenje matrik uporabimo Strasseov algoritem. Ker algoritem deluje le za sode matrike, ga moramo najprej prilagoditi, da bo deloval tudi za matrike z liho stolpci oz. vrsticami. To naredio tako, da matriki razdelimo na bloke, kjer je največji blok soda matrika, na kateri lahko za množenje uporabimo Strassov algoritem, ostali bloki pa so vektorji oziroma samo en element. Začetni matriki nato bločno zmnožimo in dobimo želeni rezultat.

Časovna zahtevnost je manjša kot pri SlowMatrix:
Če bi si pri SlowMatrix začetni matriko razdelili vsako na 4 enake bloke, bi za izračun produkta potrebovali 8 produktov teh manjših blokov.
Pri FastMatrix pa za izračun produkta potrebujemo le 7 produktov manjših blokov.

A Strasseov algoritem je učinkovit le za matrike zelo velikih velikosti. Razlog za to je, da pri Strasseovem algoritmu res potrebujemo le 7 produktov, ampak problem je da naredimo veliko več vsot. Časovna zahtevnost seštevanja matrik pa je pri manjših dimenzijah le malo manjša od časovne zahtevnosti za množenje matrik. Zaradi tako velikega števila seštevanj je FastMatrix slabši za manjše matrike.

**3)CheapMatrix**

Tukaj naredimo še malo drugačno implementacijo Strassovega algoritma. Časovna zahtevnost je enaka, prostorska zahtevnost CheapMatrix pa je nižja, saj uporabljamo le začetni matriki, delovno matriko in ciljno matriki, ki jih po potrebi spreminjamo.



