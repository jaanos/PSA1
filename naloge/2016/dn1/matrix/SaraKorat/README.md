# Poročilo

*Sara Korat*



## SlowMatrix

### Opis 

Algoritem računa produkt dveh matrik po običajnem postopku. Vzamemo i-to vrstico leve matrike in 
k-ti stolpec desne matrike, izračunamo njun skalarni produkt in dobimo element (i, k) v novi matriki. 
 

### Analiza zahtevnosti

* **Časovna zahtevnost**  pri običajnem množenju matrik v primeru množenja dveh matrik dimenzije `n x n`, 
je `O(n^3)` (`n^2` elementov in `n množenj + n seštevanj = 2n => O(n)` nam da `n^2 * n => O(n^3).` 
Če imamo matriki z dimenzijama `n x m` in `m x k`, imamo časovno zahtevnost`O(nmk)` (torej `n x k` elementov in `m 
množenj + m seštevanj => O(m)`, iz česar pa dobimo `O(nmk)`). Algoritem je časovno zelo zahteven za matrike
velikih dimenzij.

* __Prostorska zahtevnost__
Poleg vhodnih podatkov (torej matrike left in matrike right) porabimo konstanten prostor s številom `l`, kateremu
v vsaki tretji for zanki v algoritmu prištevamo produkte, nato pa število znova vrnemo na nič. Število je vedno
samo eno, zato je naša prostorska zahtevnost `O(1)`, ne glede na velikost vhodnih matrik.


### Primerjava dejanskih časovi pri vhodih različnih velikosti

--------------




## FastMatrix

### Opis

Algoritem uporablja Strassenovo metodo množenja matrik, pri kateri obe matriki razdelimo na 4 dele (v primeru,
ko so dimenzije matrik `n x m` in `m x k` sode). Namesto osmih produktov podmatrik, ki bi jih uporabili pri navadnem množenju, porabimo 
7 produktov, ki so v algoritmu definirani kot `P1, P2, P3, P4, P5, P6, P7`. 
V primeru, da matrike niso (v celoti ali pa sploh ne) sodih dimenzij, ločimo (kakor v algoritmu):

1.__če `m` lihe, `k` in `n` pa sode dimenzije__    

   Matrika left je dimnezij `n x m`, in če jo razdelimo na 4 dele, po delitvi
    ostane desni stolpec `left[0:n, m-1:m]` (če upoštevamo zamaknjenost indeksov
    v Pythonu - tudi v vseh naslednjih primerih):     
     
     A |  B |/// 
   ---|---|---
     C |  D |/// 
    
   Matrika right je dimnezij `m x k`, in če jo, kot matriko left, razdelimo
    na 4 dele, nam tokrat ostane spodnja vrstica `left[n-1:n, 0:m]`:
    
   E | F 
   ---|---
   G | H
    /// | /// 

   V tem primeru izračunamo zmnožek označenih podmatrik s pomočjo sedmih 
    produktov po Strassenovem algoritmu, na koncu pa `[i,j]`-temu elementu nove matrike prištejemo še
    zmnožek `i`-tega elementa zadnjega stolpca matrike left in `j`-tega elementa
    zadnje vrstice matrike right.    
    
    
    
2.__če `m` in `k` lihe, `n` pa sode dimenzije__    
        
   Matrika left je dimenzije `n x m` in po tem, ko jo razdelimo na 4 dele,
   nam znova ostane zadnji stolpec:
    
   |  A |  B |///| 
   |---|---|---|
   |  C |  D |/// |

   Pri matriki right nam po razdelitvi na podmatrike, kot prej ostane zadnja,
   vrstica, tokrat dobimo pa še prost zadnji stolpec:
   
   |  E |  F |///| 
   |---|---|---|
   |  G |  H |/// |
   |///|///|///|

   Če ignoriramo zadnji stolpec matrike right, je postopek isti, kot če je 
   lih samo `m`. Ko dobimo novo matriko, ji dodamo zadnji stolpec, ki je 
   zmnožek matrike left in zadnjega stolpca matrike right. 
   
3.__če `m`, `k` in `n` lihe dimenzije__
   
   Po razdelitvi matrike left na podmatrike, nam ostaneta zadnji stolpec in 
   zadnja vrstica:
   
   |  A |  B |///| 
   |---|---|---|
   |  C |  D |/// |
   |///|///|///|

   Prav tako nam ostaneta zadnji stolpec in zadnja vrstica pri matriki right:

   |  E |  F |///| 
   |---|---|---|
   |  G |  H |/// |
   |///|///|///|
   
   Če ignoriramo zadnjo vrstico matrike left, je postopek isti kot pri
   prejšnjem primeru, ko sta `m` in `k` liha. Tokrat novi matriki dodamo 
   vrstico, ki je produkt zadnje vrstice matrike left in celotne matrike right. 
   
4.__če `m` in `n` lihe, `k` pa sode dimenzije__ 
   
   Znova nam po razdelitvi matrike left na podmatrike, ostaneta zadnji stolpec in zadnja
   vrstica:
   
   |  A |  B |///| 
   |---|---|---|
   |  C |  D |/// |
   |///|///|///|
   
   Pri matriki right pa nam ostane samo zadnja vrstica:
   
   |E | F |
   |---|---|
   |G | H|
   | /// | /// |
   
  Če ignoriramo zadnjo vrstico matrike left, lahko za matriko left dimenzije 
  `n-1 x m` in matriko right istih dimenzij, ponovimo postopek, če je samo `m`
  lih, nato pa znova novi matriki dodamo vrstico, ki jo dobimo z množenjem
  zadnje vrstice v matriki left in matrike right. 


5.__če `m` sode in `k` lihe dimenzije__  
 
   Matriko left lahko razdelimo na podmatrike po Strassenovem algoritmu.

   |A | B |
   |---|---|
   |C | D|
   
   Pri matriki right nam po razdelitvi na podmatrike ostane zadnji stolpec. 
   
   |  E |  F |///| 
   |---|---|---|
   |  G |  H |/// |
 
   Podmatrike pomnožimo s pomočjo sedmih produktov, nato pa zmnožimo matriko
   left in zadnji stolpec matrike right, ter dobljen vektor pridružimo k novi
   matriki, da dobimo zadnji stolpec.
   
   
6.__če `m` sode, `k` in `n` pa  lihe dimenzije__ 
    
   Pri matriki left nam po razdelitvi na podmatrike ostane zadnja vrstica
   za posebno obravnavo:
   
   |  A |  B | 
   |---|---|
   |  C |  D |
   |///|///|///|
   
   Pri matriki right kot v prejšnjem primeru, ko je lih samo `k`, nam 
   po razdelitvi na podmatrike ostane zadnji stolpec:
   
   |  E |  F |///| 
   |---|---|---|
   |  G |  H |/// |
   
   Najprej novi matriki, ki jo dobimo s pomočjo sedmih produktov, dodamo 
   vrstico, ki je produkt zadnje vrstice matrike left in matrike right brez 
   zadnjega stolpca, nato pa novi matriki dodamo še zadnji stolpec, ki ga 
   dobimo s produktom matrike left in zadnjim stolpcem matrike right.
   
7.__če `m` in `k` sode, `n` in `k` pa lihe dimenzije__

   Matrika left po razdelitvi izgleda takole: 

   |  A |  B | 
   |---|---|
   |  C |  D |
   |///|///|///|
   
   Matrika right je sode dimenzije in jo lahko normalno razdelimo:
    
   |E | F |
   |---|---|
   |G | H|
   
   Množimo podmatrike, nato pa novi matriki dodamo zadnjo vrstico, ki jo dobimo
   z množenjem zadnje vrstice matrike left in matrike right.
   
   **
   
   Za opis delovanja tega algoritma z lihimi dimenzijami bi lahko izpostavili le tri primere, nato
   pa jih med sabo kombinirali, da bi dobili vse zgoraj napisane možnosti:
   
   * ko je `m` lih, `k` in `n` pa soda
   * ko je `k` lih, `m` in `n` pa soda
   * ko je `n` lih, `m` in `k` pa soda
   
   
### Analiza zahtevnosti

* __Časovna zahtevnost__ `T(n,m,k)` Strassenovega algoritma je manjša kot pri navadnem množenju matrik, 
    vendar sem nam ga splača uporabljati le pri večjih matrikah. Pri izračunu si časovne
    zahtevnosti si pomagamo s krovnim izrekom. 
    * Definiranje novih spremenljivk (`N`, `M`, `K`, `N2`,`M2`, `K2`) nam vzame konstanten čas
    `O(1)`.
    * Če imamo eno od dimenzij matrik enako `1`, je časovna zahtevnost
    enaka časovni zahtevnosti v `SlowMatrix`.
    * Za definiranje novih podmatrik (`A`, `B`, `C`, `D`,`E`, `F`, `G`, `H`)
     porabimo konstanten čas `O(1)`.
    * Računanje sedmih produktov. Za vsak produkt porabimo eno ali dve 
    __seštevanji__ (upoštevamo oznake iz algoritma: `N = n//2`, `M = m//2`,
    `K = k//2`):
        ```
        P1 : F - H => O(M*K)
        P2 : A + B => O(N*M)
        P3 : C + D => O(N*M)
        P4 : G - E => O(M*K)
        P5 : A + D => O(N*M) , E + H => O(M*K)
        P6 : B - D => O(N*M) , G + H => O(M*K)
        P7 : A - C => O(N*M) , E + F => O(M*K)
        ```

        Za seštevanja torej porabimo `O(M*K)`, `O(N*M)` ali `O(N*M) + O(M*K)`.
        Skupno je časovna zahtevnost seštevanj enaka `O(L*M)`, pri čemer smo za
        `L` vzeli maksimum od `N` in `K`: `L = max{K, N}`.
        
        Za vsak __produkt__ porabimo `T(N,M,K)` (po krovnem izreku), torej `7*T(N,M,K)`. 
     * V primeru, ko so __vse dimenzije sode__, s seštevanjem matrik `Pi` 
        za `i = 1, ..., 7` dobimo časovno zahtevnost `O(N*K)`:
            
        ```
            C1 : P4 + P5 + P6 - P2 => O(N*K)
            C2 : P1 + P2 => O(N*K)
            C3 : P3 + P4 => O(N*K)
            C4 : P1 + P5 - P3 - P7 => O(N*K)
        ```
         
         Skupni čas za matriki sodih dimenzij je 
         ```
         T(n, m, k) = O(1) + O(L*M) + 7*T(N, M, K) + O(N*K) 
         T(n, m, k) = O(L*M) + 7*T(N, M, K)
         ```
        
          Vzamemo maksimalno dimnezijo `s = max{n, m, k}` in upoštevamo krovni izrek:
          ```
           T(s) = 7*T(s//2) + O((s//2)^2) = 7*T(s//2) + O(s^2)
           2 < log_2 (7) => T(s) = O(s^(log_2 (7))
          ```
        
      * V (časovno najzahtevnejšem) primeru - ko so vse dimenzije lihe, porabimo
        še dodaten čas za računanje za:
        
        * množenje in prištevanje k novi matriki: `O(n*k)` množenj +
        `O(n*k)` prištevanj `=> O(n*k)`
        * računanje in dodajanje stolpca: `O(n*m)`
        * računanje in dodajanje vrstice: `O(m*k)`
        
        Skupni seštevek časa dobimo z upoštevanjem krovnega izreka:
           
         ```
           T(n, m, k) = O(1) + O(L*M) + 7*T(N, M, K) + O(N*K) + O(n*k) + O(n*m) + O(m*k)
           T(n, m, k) = 5*O(s^2) + 7*T(s//2) = O(s^2) + 7*T(s//2)
           2 < log_2 (7) => 
           T(s) = O(s^(log_2 (7))
         ```


* __Prostorska zahtevnost__

### Primerjava dejanskih časovi pri vhodih različnih velikosti

--------------


## CheapMatrix

### Opis

### Analiza zahtevnosti


### Primerjava dejanskih časovi pri vhodih različnih velikosti

--------------


## Zaključki




--------------
--------------