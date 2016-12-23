# Poročilo

Samo Kralj

# SlowMatrix

SlowMatrix ima implementirano navadno množenje matrik. Torej za ( i, j ) člen v matriki bo izračunal 
skalarni produkt i-te vrstice in j-tega stolpca.

## Časovna Zahtevnost:

Če množimo matriki velikosti n x m in m x k, bo ciljna matrika velikosti n x k. Za vsak element v ciljni
matriki pa opravimo m operacij. Skupna časovna zahtevnost bo torej O(n*k*m).

## Prostorska Zahtevnost:

Prostor, ki ga porabi je velikost ciljne matrike.

# FastMatrix

FastMatrix ima implementirano Strassenovo množenje matrik. Delovanje lahko vidimo na primeru:

Naj bo A matrika velikosti ( 2*n + 1) x ( 2*m + 1 ) in naj bo B velikosti ( 2*m + 1) x ( 2*k + 1). 
Algoritem bo najprej vzel največji podmatriko sodih dimenzij obeh matrik in ju zmnožil. V našem primeru 
bi matriko A razdelil na 4 podmatrike velikosti n x m in matriko B na 4 podmatrike velikosti m x k in le-te
s Strassenovim algoritmom zmnožil. 

Lihe vrstice in stolpce obravnava sledeče:
- Če ima leva matrika liho število vrstic bo to zadnjo liho vrstico skalarno množil z vsakim stolpcem desne
matrike in rezultat zapisal v ciljno matriko. 
- Če ima desna matrika liho število stolpcev bo algoritem vsako vrstico leve matrike množil skalarno z zadnjim
stolpcem in rezultat zapisal v ciljno matriko.
- V primeru lihega števila stolpcev leve matrike in seveda tudi liheha števila vrstic desne matrike pa bo
ciljni matriki na ustreznih mestih prištel še matriko, ki jo če skupaj zmnožimo zadnji stolpec leve matrike
in zadnjo vrstico desne matrike. Več o tem in izpeljava pa je napisano med komentarji v kodi.

Matrike velikosti 1 x X ali X x 1 zmnožimo na navaden način. 

## Časovna zahtevnost:

Omejimo se na množenje kvadratnih matrik. 

Za množenje matrike dimenzije n x n porabimo:
- O( 1 ) ... definiranje spremenljivk in pointerjev
- 22 * (n/2)^2 ... seštevanja in odštevanja matrik dimenzij n/2 x n/2
- O( n^2 ) ... generiranje matrik v katere zapisujemo vmesne rezultate. 
- 7 množenj matrik velikosti n/2 x n/2

Sledi: T(n) = 7 * T ( n/2 ) + 22 * (n/2)^2 + O(n^2) + O(1)
Po krovnem izreku sledi, da je časovna zahtevnost algoritma O(n^(log(2, 7))), kar je približno O(n^2.80).
