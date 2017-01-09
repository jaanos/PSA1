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

* __Prostorska zahtevnost__:
Poleg vhodnih podatkov (torej matrike left in matrike right) porabimo konstanten prostor s številom `l`, kateremu
v vsaki tretji for zanki v algoritmu prištevamo produkte, nato pa število znova vrnemo na nič. Število je vedno
samo eno, zato je naša prostorska zahtevnost `O(1)`, ne glede na velikost vhodnih matrik.


### Primerjava dejanskih časov pri vhodih različnih velikosti


Pri primerjavi časov dejanski dimenzij nas zanimajo primeri, ko so vhodi sodi in lihi (za
nadaljno primerjavo s `FastMatrix` in `CheapMatrix`), 
ter kako se čas spreminja na podlagi velikosti dimenzij. 

Tabela predstavlja izračunano povprečje 10ih poskusov za določene dimenzije (enota: sekunda). Koda za 
izračune se nahaja v mapi `test.SaraKorat.casovna_zahtevnost`.

n|m|k|povprečje
---|---|---|---
10|10|10|0.002727
10|11|10|0.003522
11|11|10|0.003561
10|11|11|0.003613
11|11|11|0.003698
50|50|50|0.415034
51|51|51|0.434669
100|100|100|3.913663
101|101|101|4.077199
200|200|200|41.613351
201|201|201|42.350267
500|500|500|1218.236100

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
    
   A |  B |/// 
   ---|---|---
   C |  D |/// 

   Pri matriki right nam po razdelitvi na podmatrike, kot prej ostane zadnja,
   vrstica, tokrat dobimo pa še prost zadnji stolpec:
   
   E |  F |/// 
   ---|---|---
     G |  H |/// 
   ///|///|///

   Če ignoriramo zadnji stolpec matrike right, je postopek isti, kot če je 
   lih samo `m`. Ko dobimo novo matriko, ji dodamo zadnji stolpec, ki je 
   zmnožek matrike left in zadnjega stolpca matrike right. 
   
3.__če `m`, `k` in `n` lihe dimenzije__
   
   Po razdelitvi matrike left na podmatrike, nam ostaneta zadnji stolpec in 
   zadnja vrstica:
   
   A |  B |/// 
   ---|---|---
    C |  D |/// 
   ///|///|///

   Prav tako nam ostaneta zadnji stolpec in zadnja vrstica pri matriki right:

   E |  F |/// 
   ---|---|---
     G |  H |/// 
   ///|///|///
   
   Če ignoriramo zadnjo vrstico matrike left, je postopek isti kot pri
   prejšnjem primeru, ko sta `m` in `k` liha. Tokrat novi matriki dodamo 
   vrstico, ki je produkt zadnje vrstice matrike left in celotne matrike right. 
   
4.__če `m` in `n` lihe, `k` pa sode dimenzije__ 
   
   Znova nam po razdelitvi matrike left na podmatrike, ostaneta zadnji stolpec in zadnja
   vrstica:
   
   A |  B |///
   ---|---|---
     C |  D |/// 
   ///|///|///
   
   Pri matriki right pa nam ostane samo zadnja vrstica:
   
   E | F 
   ---|---
   G | H
    /// | /// 
   
  Če ignoriramo zadnjo vrstico matrike left, lahko za matriko left dimenzije 
  `n-1 x m` in matriko right istih dimenzij, ponovimo postopek, če je samo `m`
  lih, nato pa znova novi matriki dodamo vrstico, ki jo dobimo z množenjem
  zadnje vrstice v matriki left in matrike right. 


5.__če `m` sode in `k` lihe dimenzije__  
 
   Matriko left lahko razdelimo na podmatrike po Strassenovem algoritmu.

   A | B 
   ---|---
   C | D
   
   Pri matriki right nam po razdelitvi na podmatrike ostane zadnji stolpec. 
   
   E |  F |/// 
   ---|---|---
     G |  H |/// 
 
   Podmatrike pomnožimo s pomočjo sedmih produktov, nato pa zmnožimo matriko
   left in zadnji stolpec matrike right, ter dobljen vektor pridružimo k novi
   matriki, da dobimo zadnji stolpec.
   
   
6.__če `m` sode, `k` in `n` pa  lihe dimenzije__ 
    
   Pri matriki left nam po razdelitvi na podmatrike ostane zadnja vrstica
   za posebno obravnavo:
   
   A |  B 
   ---|---
     C |  D 
   ///|///|///
   
   Pri matriki right kot v prejšnjem primeru, ko je lih samo `k`, nam 
   po razdelitvi na podmatrike ostane zadnji stolpec:
   
   E |  F |///
   ---|---|---
     G |  H |/// 
   
   Najprej novi matriki, ki jo dobimo s pomočjo sedmih produktov, dodamo 
   vrstico, ki je produkt zadnje vrstice matrike left in matrike right brez 
   zadnjega stolpca, nato pa novi matriki dodamo še zadnji stolpec, ki ga 
   dobimo s produktom matrike left in zadnjim stolpcem matrike right.
   
7.__če `m` in `k` sode, `n` in `k` pa lihe dimenzije__

   Matrika left po razdelitvi izgleda takole: 

   A |  B 
   ---|---
   C |  D 
   ///|///|///
   
   Matrika right je sode dimenzije in jo lahko normalno razdelimo:
    
   E | F 
   ---|---
   G | H
   
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
    vendar se nam ga splača uporabljati le pri večjih matrikah. Pri izračunu časovne
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

        Za seštevanja torej porabimo `O(M*K)`, `O(N*M)` ali `O(N*M) + O(M*K)`, torej `5*O(N*M) + 5*O(M*K)`.
        Skupno je časovna zahtevnost seštevanj enaka `O(L*M)`, pri čemer smo za
        `L` vzeli maksimum od `N` in `K`: `L = max{K, N}`.
        
        Za vsak __produkt__ porabimo `T(N,M,K)` (po krovnem izreku), torej skupaj `7*T(N,M,K)`. 
     * V primeru, ko so __vse dimenzije sode__, s seštevanjem matrik `Pi` 
        za `i = 1, ..., 7` dobimo časovno zahtevnost `8*O(N*K)` oz. `O(N*K)`:
            
        ```
            C1 : P4 + P5 + P6 - P2 => 3*O(N*K)
            C2 : P1 + P2 => O(N*K)
            C3 : P3 + P4 => O(N*K)
            C4 : P1 + P5 - P3 - P7 => 3*O(N*K)
        ```
         
         Vzamemo maksimalno dimnezijo `s = max{n, m, k}` in s tem dobimo največjo časovno
         zahtevnost, zanemarimo konstante. Pri izračunu upoštevamo krovni izrek.
         Skupni čas za matriki sodih dimenzij je :
         
         ```
         T(n, m, k) = O(1) + O(L*M) + 7*T(N, M, K) + O(N*K) 
         T(n, m, k) = O((s//2)*(s//2)) + 7*T(N, M, K)
         
         s = max{n,m,k}, s//2 = max{N,M,K}
         
         T(s) = 7*T(s//2) + O((s//2)^2) = 7*T(s//2) + O(s^2)
         2 < log_2 (7) => T(s) = O(s^(log_2 (7))
          ```
        
      * V (časovno najzahtevnejšem) primeru, ko so vse dimenzije lihe, porabimo
        še dodaten čas za računanje za:
        
        * _množenje in prištevanje k novi matriki_: `O(n*k)` množenj +
        `O(n*k)` prištevanj `=> O(n*k)`
        * _računanje in dodajanje stolpca_: `O(n*m)`
        * _računanje in dodajanje vrstice_: `O(m*k)`
        
        Skupni seštevek časa dobimo z upoštevanjem krovnega izreka (kot pri primeru samih lihih dimenzij):
           
         ```
           T(n, m, k) = O(1) + O(L*M) + 7*T(N, M, K) + O(N*K) + O(n*k) + O(n*m) + O(m*k)
           
           s = max{n,m,k}, s//2 = max{N,M,K}
           
           T(n, m, k) = 4*O(s^2) + 7*T(s//2) = O(s^2) + 7*T(s//2)
           2 < log_2 (7) => 
           T(s) = O(s^(log_2 (7))
         ```


* __Prostorska zahtevnost__ je večja kot pri navadnem množenju matrik. 
    * Definiranje novih spremenljivk (`N`, `M`, `K`, `N2`,`M2`, `K2`) nam vzame konstanten 
    prostor `O(1)`. 
    * Če imamo eno od dimenzij matrik enako `1`, je prostorska zahtevnost
    enaka časovni zahtevnosti v `SlowMatrix`.
    * Za definiranje podmatrik (`A`, `B`, `C`, `D`,`E`, `F`, `G`, `H`)
     porabimo `O(1)`.
    * Računanje sedmih produktov. Vsak produkt porabi prostor za vmesno matriko/matriki, ki jo/ju dobimo
     s seštevanjem/odštevanjem, na desni strani porabimo `O(M*K)` prostora, na levi strani
     porabimo `O(N*M)`, rekurzivni klic pa nam doda še `P(N, M, K)`. Skupno za produkte porabimo
     `P(N, M, K) + O(L*M)`, pri čemer `L = max{K, N}`.
    * Za izračun matrike sodih dimenzij porabimo `8` seštevanj/odštevanj, skupno `8*O(N*K)` prostora, ki
    ga porabijo vmesne matrike, iz katerih na koncu sestavimo novo matriko. 
    * Za izračun matrike lihih dimenzij poleg prostora za novo matriko, porabimo še prostor:
        * _pri množenju in prištevanju k novi matriki_: zaradi sprotnega zapisovanja v novo matriko in množenja
        skalarjev, porabimo `O(1)` dodatnega prostora
        * _pri računanju in dodajanju stolpca_: porabimo `O(n)` prostora za vektor, ki ga pridamo novi matriki
        * _pri računanju in dodajanju vrstice_: porabimo `O(k)` prostora za vektor, ki ga pridamo novi matriki
    
        Skupna prostorska zahtevnost:
        
        ```
           P(n, m, k) = O(1) + O(M*K) + O(N*M) + P(N, M, K) + 8*O(N*K) + O(1) + O(n) + O(k)
           P(n, m, k) = P(N, M, K) + O(M*K) + O(N*M) + O(N*K) + O(n) + O(k)
           
           s = max{n, m, k}
           
           P(s) = P(s//2) + O(s^2) + O(s)
           P(s) = P(s//2) + O(s^2)
           P(s) = O(s^2)
         ```
        

### Primerjava dejanskih časov pri vhodih različnih velikosti

n|m|k|povprečje
---|---|---|---
10|10|10|0.035543
10|11|10|0.035235
11|11|10|0.035345
10|11|11|0.035003
11|11|11|0.035538
50|50|50|2.015315
51|51|51|2.063882
100|100|100|14.177991
101|101|101|14.352611
200|200|200|95.032223
201|201|201|97.741663
500|500|500|816.303042

Pri dimenzijah `10x10x10`, `10x11x10`, `11x11x10`, `10x11x11` in `11x11x11` naj
bi bila časovna razlika med `10x10x10` in `11x11x11` večja (sode dimenzije naj
bi porabile manj časa kot lihe, kljub temu da gre za isto časovno zahtevnost), 
vendar se pri majhnih dimenzijah razlike v času ne poznajo. Empirično se s tako
majhnimi dimenzijami ne da dokazati časovne razlike.

--------------

## CheapMatrix


### Opis

Algoritem je enak Strassenovemu, le da tokrat varčujemo s prostorom. Matriki left
in right znova razdelimo na sode podmatrike (kot pri `FastMatrix`), isto definiramo
sedem produktov `P1,...,P3`, le da seštevke/odštevke računamo z operatorjema `+=` in `-=`
(ki nam omogočita, da pri seštevanju/odštevanju matrik ne dobimo nove matrike), 
nato pa pri zmnožkih uporabimo delovno matriko, ki jo razdelimo na iste dimenzije
kot je izhodna matrika, torej matrika `S` (self).   

Delovna matrika:

   D1 |  D2 
   ---|---
   D3 |  D4
 
Delovna matrika nam omogoči, da ne ustvarjamo novih matrik (z množenjem), ampak uporabljamo njene
(pod)matrike za prepis, ki nam ne zavzame dodatnega prostora. 

Izhodna matrika:

   S1 |  S2 
   ---|---
   S3 |  S4

```
    S1 = P4 + P5 + P6 - P2
    S2 = P1 + P2
    S3 = P3 + P4
    S4 = P1 + P5 - P3 - P7
```

V primeru, ko so dimenzije matrik left in right lihe, uporabimo kodo iz algoritma `FastMatrix`, le
da na isti način kot zgoraj zamenjamo način množenja in seštevanja/odštevanja (z delovno matriko
in operatorjema `+=` in `-=`). Primer, ko je lih `k`:

```
    FastMatrix:
    self[0:n, k - 1] = left * right[0:m, k - 1]  
    
    CheapMatrix:
    self[0:n, k - 1].multiply(left, right[0:m, k - 1], work[0:n, k - 1])
```

### Analiza zahtevnosti

* __Časovna zahtevnost__ je ista kot v `FastMatrix`, torej `T(s) = O(s^(log_2 (7))`, kjer
`s = max{n, m, k}`. Sprotne časovne zahtevnosti so zapisane v algoritmu.

* __Prostorska zahtevnost__:
    * Definiranje novih spremenljivk (`N`, `M`, `K`, `N2`,`M2`, `K2`) nam vzame konstanten 
    prostor `O(1)`. 
    * Če imamo eno od dimenzij matrik enako `1`, je prostorska zahtevnost
    enaka časovni zahtevnosti v `SlowMatrix`.
    * Za definiranje podmatrik (`A`, `B`, `C`, `D`,`E`, `F`, `G`, `H`)
     porabimo `O(1)`.
    * Računanje sedmih produktov. Za vsak `Pi` (`i=1,...,7`) za prištevanje/odštevanje
    ne porabimo dodatnega prostora, saj operatorja `+=` in `-=` ne ustvarita nove matrike,
    ampak matriko na levi strani le prepišeta. Rekurzivni klic nam porabi `P(N, M, K)` prostora,
    nadaljne računanje v primeru lihih dimenzij, pa nam v vsakem primeru porabi konstanten prostor
    `O(1)`. Skupno je prostorska zahtevnost torej:
      
         ```
        P(n, m, k) = P(N, M, K) + O(1)
         
         s = max{n, m, k}
         
         P(s) = O(log(s))
        ```

### Primerjava dejanskih časov pri vhodih različnih velikosti

n|m|k|povprečje
---|---|---|---
10|10|10|0.025674
10|11|10|0.025708
11|11|10|0.025694
10|11|11|0.027634
11|11|11|0.026813
50|50|50|1.593188
51|51|51|1.581271
100|100|100|10.964154
101|101|101|11.071894
200|200|200|76.999634
201|201|201|75.218695
500|500|500|636.325036

--------------


## Zaključki

Tabela časovnih zahtevnosti (v sekundah) posameznih algoritmov pri različnih
vhodnih podatkih:

n|m|k|SlowMatrix|FastMatrix|CheapMatrix
---|---|---|---|---|---
10|10|10|0.002727|0.035543|0.025674
10|11|10|0.003522|0.035235|0.025708
11|11|10|0.003561|0.035345|0.025694
10|11|11|0.003613|0.035003|0.027634
11|11|11|0.003698|0.035538|0.026813
50|50|50|0.415034|2.015315|1.593188
51|51|51|0.434669|2.063882|1.581271
100|100|100|3.913663|14.177991|10.964154
101|101|101|4.077199|14.352611|11.071894
200|200|200|41.613351|95.032223|76.999634
201|201|201|42.350266|97.741663|75.218695
500|500|500|1218.236100|816.303042|636.325036

Iz primerjave rezultatov lahko vidimo, da je za matrike majhnih dimenzij občutno
hitrejši algoritem `SlowMatrix`. Ker `CheapMatrix` porabi manj prostora kot
`FastMatrix`, se algoritem hitreje izvede. Ker je časovna zahtevnost obeh
algoritmov enaka, je prostorska zahtevnost tista, ki zmanjša/poveča čas izvedbe
algoritma.

Za matrike velikih velikosti (v našem primeru `500x500x500`) je `FastMatrix`
veliko hitrejši od `SlowMatrix`, kljub temu da porabi veliko več prostora. V tem
primeru je lepo vidno, kako zelo se pozna, da pri `FastMatrix` uporabljamo sedem
množenj namesto osmih.  



--------------
--------------