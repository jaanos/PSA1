# Poročilo

*Luka Avbreht*

V nalogi smo implementirali tri načine za množenje matrik.
Množenje matrik je velikosti `A = m x n` in `B = k x l` je mogoce le v primeru, ko je število stoplcev prve matrike (n) enako stevilu vrstic druge matrike (k). 
Nujin produkt `AB` bo bila matrika velikosti `m x l`, torej imela enako stevilo vrstic, kot prva matrika, ter stevilo stoplcev druge matrike. 

## SlowMatrix

Gre za običajno množenje matrik, kot ga ponavadi izvajamo na roke. Za vsak element v ciljni matriki, se moramo z for zanko sprehoditi cez sirino leve matrike, oz visino desne.

### Časovna zahtevbnost 

Če zmnožimo matriki `(n x m)` in `(m x k)`, je časovna zahtevnost `O(n*m*k)` oziroma približno 
`O(n^3)`. 

### Prostorska zahtevnost

Če zmnožimo matriki `(n x m)` in `(m x k)` je prostorska zahtevnost 
`O(n*m)+O(m*n)+O(n*k)` Kar lahko ocenimo z `O(max{m,n,k})`. Z drugimi besedami 
ne potrebujemo nobenega dodatnega prostora kot velikosi ciljne matrike.

## FastMatrix

Pomagali si bomo z tako imenovanim Strassenovim algoritmom.  
To je algoritem pri katerem za mnozenje matrik uporabimo metodo deli in vladaj na sledec nacin:  
```
  X =   in   Y =   
[ A B ]    [ E F ]    
[ C D ]    [ G H ]      
```  
s pomočjo sedmih produktov  

* *P1 = A (F - H)*,
* *P2 = (A + B) H*,
* *P3 = (C + D) E*,
* *P4 = D (G - E)*,
* *P5 = (A + D) (E + H)*,
* *P6 = (B - D) (G + H)* in
* *P7 = (A - C) (E + F)*.

Produkt potem izračunamo kot  
```
                  X*Y =
[ P4 + P5 + P6 - P2         P1 + P2      ]
[      P3 + P4         P1 + P5 - P3 - P7 ]
```



### Časovna zahtevnost

S pomočjo [krovnega izreka] (https://en.wikipedia.org/wiki/Master_theorem) bomo dokazali časovno zahtevnost strassenovega algoritma.

Predpostavimo, da je sirina in visina obeh matrik sodo stevilo.  
Problem razdelimo na sedem delov, ki so vsak pol manjsi od svojega oredhodnika. Iz izracunanih rezultatov resitev nazaj sestavimo v `O(n^2)`. Iz teh podatkov dobimo vrednosti, ki jih uporabimo v krovnem izreku   
* b = 2  
* a = 7  
* d = 2  


Vidimo, da pademo v opcijo, ko je `d < log_b(a)` torej je csovna zahtevnost algoritma enaka:

`O(n^(log_2(7)))`


[Več] (http://wiki.fmf.uni-lj.si/wiki/Strassenovo_mno%C5%BEenje_matrik)

### Prostorska zahtevnost

## CheapMatrix

### Časovna zahtevnost

### Prostorska zahtevnost

