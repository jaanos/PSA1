# Poročilo

*Vid Megušar*

##**Opis Algoritmov**

**1) SlowMatrix**\n
Običajno množenje matrik, kot če bi ročno računali manjše matrike.
Ker imamo tri for zanke prvi dve po stolpcih(n) in vrsticah(m) prve matrike, tretjo pa po stopcih(k) druge matrike imamo časovno zahtevnost O(m\*n\*k).

**2)FastMatrix**\n
Zdaj za množenje matrik uporabimo Strasseov algoritem. Ker algoritem deluje le za sode matrike, ga moramo najprej prilagoditi, da bo deloval tudi za matrike z liho stolpci oz. vrsticami. To naredio tako, da matriki razdelimo na bloke, kjer je največji blok soda matrika, na kateri lahko za množenje uporabimo Strassov algoritem, ostali bloki pa so vektorji oziroma samo en element. Začetni matriki nato bločno zmnožimo in dobimo želeni rezultat.


