# Poročilo

*Žiga Zupančič*

## Opis algoritma
Algoritem najprej preveri, če dimenzije tabel tež ustrezajo številu vozlišč v drevesu, če je podani graf neusmerjen
ter če je k vsaj 2. Nato ustvarimo vse možne neodvisne podmnožice cikla - podmnožice predstavimo v binarnem zapisu, 
če je na `j`-tem mestu v binarnem zapisu `1`, potem je element v ciklu na mestu `j` v tej podmnožici.
Neodvisne podmnožice cikla so tako tiste, ki nimajo dveh zaporednih enic ter na prvem in zadnjem mestu ni enice.
Dobimo jih tako, da vsako število `0 <= i < 2^k` predstavimo v binarnem zapisu 
in preverimo pogoj neodvisnosti. Nato za vsako od neodvisnih podmnožic cikla shranimo kompatibilne podmnožice (to so 
tiste, ki nimajo enic na istem mestu kot prvotna množica) v slovar. Ustvarimo seznam slovarjev, kamor bomo shranjevali 
maksimalne vrednosti ter uporabljene podmnožice za vsako vozlišče v drevesu - na `i`-tem mestu v seznamu je slovar za 
`i`-to vozlišče v drevesu. Ključi v slovarju so števila, ki v binarnem zapisu predstavljajo neodvisne množice ciklov, 
vrednosti pa največjo težo, ki jo dobimo če uporabimo neodvisno podmnožico cikla, ki je v ključu, pri čemer 
upoštevamo vse sinove tega vozlišča (ki so že izračunani) ter si zapišemo katere neodvisne podmnožice smo izbrali pri 
sinovih, da lahko na koncu rekonstruiramo vsa uporabljena vozlišča.
Z DFS-jem nato obiščemo vsa vozlišča in v postvisitu polnimo prej ustvarjene slovarje - za liste si le shranimo 
vrednosti največje teže za vsako neodvisno podmnožico cikla, za ostale pa pri tem upoštevamo tudi največje teže 
njihovih potomcev.
Nato za koren pogledamo pri kateri neodvisni podmnožici cikla smo dobili največjo vrednost, in to je naš rezultat. 
Sedaj le še preberemo katera vozlišča smo pri tem uporabili, tako da od vrha navzdol pogledamo katere neodvisne 
podmnožice smo uporabili za vsakega sina in to sproti dodajamo v seznam uporabljenih vozlišč.