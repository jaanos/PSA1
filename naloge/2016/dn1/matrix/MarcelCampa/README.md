# Poročilo

*Marcel Čampa*

## Opis algoritmov, časovna in prostorska zahtevnost

### SlowMatrix

Tukaj gre za naivno množenje oziroma po domače za množenje "na roke". Element *(i,j)* produkta izračunamo tako, da skalarno pomnožimo *i*-to vrstico leve vhodne matrike z *j*-tim stolpcem desne vhodne matrike.

*Časovna zahtevnost:* Ker potrebujemo *m x n* členov in za vsakega porabimo O(*k*) operacij (skalarno množenje), je skupna časovna zahtevnost O(*mkn*).

*Prostorska zahtevnost:* Pri računanju *(i,j)*-tega člena vedno shranjujemo v eno spremenljivko, na koncu pa vse zapišemo v produktno matriko. Torej je prostorska zahtevnost O(1).

###FastMatrix

Tu množimo matrike s pomočjo Strassenovega algoritma. Algoritem deluje tako, da vhodni matriki vstavimo v matriki velikosti `exp(2,x)`, kjer je *x = max(m,k,n)*. Nato dobljeni matriki razdelimo na 4 bloke enakih dimenzij. Dobimo

```
left = [[A B] [C D]]
right = [[E F] [G H]]
```

Uporabimo formule

* *P1 = A(F-H)*,
* *P2 = (A+B)H*,
* *P3 = (C+D)E*,
* *P4 = D(G-E)*,
* *P5 = (A+D)(E+H)*,
* *P6 = (B-D)(G+H)* in
* *P7 = (A-C)(E+F)*.

Produkt potem izračunamo na način

```
left*right = [[P4 + P5 + P6 - P2  ;  P1 + P2] [P3 + P4  ;  P1 + P5 - P3 - P7]]
```

To seveda storimo rekurzivno. Na koncu vrnemo blok `[0:m, 0:n]`.

*Časovna zahtevnost:* Časovna zahtevnost algoritma je `O(n^2.8)`, kjer je *n* dimenzija vhodne matrike. To dobimo takole: Označimo *n* z dimenzijo vhodnim matrik, kjer je *n = 2^x*. Potem očitno velja `T(x) = 7*T(x-1) + c^x`, kjer prvi del dobimo zaradi sedmih množenj, drugi pa pride iz seštevanja in odštevanja. Torej velja `T(x) = (7 + O(1))^x`, kar nam da po krovnem izreku `O(n^2.8)`.

*Prostorska zahtevnost:* Pri izračunu produkta porabimo precej prostora, saj na vsakem koraku generiramo nove *P_i* matrike. Skupno tako porabimo `O(mn)` prostora, kjer pa so konstante precej velike, namreč na začetku porabimo `7*O(m//2 * n//2)`, na vsakem naslednjem pa `7*O(m//(2^i) * n//(2^i))`.

###CheapMatrix

V tem algoritmu ponovno uporabimo Strassenov postopek, le da tu varčujemo s prostorom kakor se le da.

*Časovna zahtevnost:* Glej komentarje v kodi.

*Prostorska zahtevnost:* Glej komentarje v kodi.

##Primerjava časov izvajanja

Povsem preprosto se lahko prepričamo, da je SlowMatrix daleč najhitrejši način množenja, vsaj pri matrikah, katerih velikosti smo preizkusili. To je po eni strani precej očitno, namreč tri for zanke delujejo precej hitreje kot neka rekurzija z uporabo nekih "zapletenih" formul, vsaj pri majhnih količinah podatkov. Kot smo se v prejšnjem razdelku prepričali, pa je asimptotično hitrejši Strassenov algoritem, saj deluje v `O(n^2.8)`, SlowMatrix pa v `O(n^3)`, kjer smo pri SlowMatrix z *n* označili `max(m,k,n)`. To pomeni torej, da so pri časovni zahtevnosti za Strassena zelo velike konstante.

Na spodnji sliki si lahko še ogledamo graf hitrosti algoritmov, ki sem jih izračunal za matrike dimenzij `m=k=n \in {10,20,30,40,50,80,120,140,200,400}`.

![Slika časov](https://github.com/campovski/PSA1/blob/master/naloge/2016/dn1/matrix/MarcelCampa/graf.png)



