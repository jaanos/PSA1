# Poročilo
*Žiga Zupančič*

## Opis algoritmov
### Razred `SlowMatrix`

Razred `SlowMatrix` v metodi `multiply` implementira naivno množenje matrik - vrstice leve matrike skalarno množimo 
z vrsticami desne matrike. Skalarni produkt računamo s pomočjo spremenljivke `temp`, katere vrednost po izračunu 
zapišemo na (i, j)-to mesto ciljne matrike, kjer je `i` vrstice leve matrike in `j` stolpec desne.

### Razred `FastMatrix`

Metoda `multiply` v razredu `FastMatrix` najprej preveri, če so matrike ustreznih dimeznij za množenje, nato pa si
jih shrani v spremenljivke. V spremenljivke `ms`,`ns` in `ps` si shrani sodo število, ki je enako ustrezni dimenziji 
matrike, če je matrika soda in za eno manjše od dimenzije matrike, če je matrika liha. Če je katera od dimenzij leve ali
 desne matrike enaka 1, matrike ne moremo razdeliti na 4 podmatrike (torej ne moremo uporabiti Strassenovega algoritma) 
in zato matrike zmnožimo z metodo `multiply` v razredu `SlowMatrix`. Sicer pa razdelimo podmatriko `left[0:ns][0:ms]`, 
ki ima same sode dimenzije, na štiri enako velike podmatrike (`A`, `B`, `C`, `D`), ki jih bomo uporabili pri množenju. 
Podobno tudi `right[0:ms, 0:ps]` na `E`, `F`, `G` in `H`. Sledi rekurzivni izračun produktov `P1` do `P7`.
Ta se nekoč konča, saj se dimenzije matrik, ki jih množimo na vsakem koraku razpolovijo, če pa je katera izmed dimenzij
enaka 1, pa jih zmnožimo z metodo `multiply` v `SlowMatrix`. Nato obravnavamo še primere, če je katera izmed dimenzij 
matrik `left` ali `right` liha (posebej izračunamo produkte z zadnjim stolpcem leve matrike, zadnjo vrstico leve 
matrike in zadnjim stolpecm desne matrike). V tem primeru računamo produkte, kjer ima vsaj ena izmed matrik le eno 
vrstico ali stolpec. Nazadnje še izračunamo potrebne vsote matrik `P1` do `P7` in jih zapišemo v ciljno matriko, ter
prišejemo posebne produkte z zadnjim stolpcem leve matrike (lahko so 0).

### Razred `CheapMatrix`

Metoda `multiply` v tem razredu deluje podobno kot v razredu `FastMatrix`, le da pri delu porabi le O(log(kmn)) 
dodatnega prostora. Izračun `P4 + P5 + P6 - P2` poteka tako, da produkt `P6` takoj zapišemo v končno matriko na mesto 
zgoraj levo, izračunamo ga pa tako, da vhodni podmatriki `B` odštejemo `D` (da se ne ustvari nova matrika) ter 
podmatriki `G` prištejemo `H` in nato zmnožimo `B * G` z neobveznim parametrom delavne matrike, ki je enake 
dimenzije kot produkt (podmatrike naše delavne matrike). Nato `B` in `G` povrnemo v prvotno stanje.
Ostale produkte izračunamo podobno in zapišemo v delavno matriko, pri čemer neuporabljeni del delavne matrike uporabimo 
kot delavno matriko pri rekurzivnem računanju produkta. V delavni matriki so naenkrat le trije produkti izmed `P1` do 
`P7`, saj obstoječe po uporabi prepišemo z drugimi, ki jih bomo potrebovali. Tako izračunamo vse štiri vsote produktov 
Strassenovega algoritma, posebna obravnava zadnjih stolpcev in vrstic lihih matrik pa je enaka kot prej, le da podamo 
še delavno matriko, ki pa se ne uporabi, saj se ponovno kliče metoda `multiply` iz `SlowMatrix`.
  
## Analiza časovne in prostorske zahtevnosti

Naj bo `X` leva matrika in `Y` desna, njun produkt `Z` in delavna `W`. `n x m` je velikost matrike `X`, `m x p` je 
velikost matrike `Y`, `n x p` pa velikost matrike `Z` in `D`.
 
## Primerjava dejanskih časov izvajanja
Čase izvajanja bomo gledali le za kvadratne n x n matrike. V naslednji tabeli so prikazani časi v sekundah za vse tri
implementacije množenja v odvisnosti od velikosti matrik.

| n |SlowMatrix |FastMatrix |CheapMatrix|
|---|---|---|---|
| 5   |0.0005  |0.0084 |0.0050 |
| 10  |0.004   |0.066  |0.042  |
| 100 |5.5     |26.1   |18.9   |
| 200 |57.3    |181.2  |132.8  |
| 250 |127.9   |207.5  |163.0  |
| 300 |262.6   |920.8  |577.6  |
| 400 |828.0   |1256.8 |930.9  |
| 500 |1900.5  |1454.0 |1160.8 |
| 600 |3956.3  |6431.1 |4087.9 |


Spodnji graf prikazuje čas računanja produkta v odvisnosti od velikosti vhodnih matrik (n x n). Rdeča krivulja 
prikazuje množenje s SlowMatrix, zelena s FastMatrix in modra s CheapMatrix.

![graf](graf.png)
