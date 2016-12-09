# 1. domača naloga pri PSA1: Strassenov algoritem

Na predavanjih ste spoznali Strassenov algoritem za množenje matrik
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
Vaša naloga bo implementacija Strassenovega algoritma v programskem jeziku *Python 3*, ki bo delovala za matrike **poljubne velikosti** (torej ne samo za kvadratne).

## Orodja

Za izdelavo naloge boste uporabili git repozitorij, ki bo kopija (*fork*) repozitorija predmeta na [GitHub](https://github.com/jaanos/PSA1)u oziroma [Bitbucket](https://bitbucket.org/jaanos/psa1)u. Toplo priporočam, da si naredite novo vejo (*branch*) ter vse delo v zvezi z nalogo poteka v tej veji (seveda lahko po potrebi naredite še več vej). Vse vaše spremembe naj bodo v mapi `naloge/2016/dn1/matrix/ImePriimek`, kjer `ImePriimek` nadomestite s svojim imenom in priimkom. Po potrebi lahko vključite tudi teste, ki naj bodo v mapi `naloge/2016/dn1/test/ImePriimek`. Ko boste z nalogo zaključili, boste naredili *pull request* svoje veje na originalni repozitorij, potem pa bom vaše spremembe potegnil vanj.

Morebitnih drugih predlogov in izboljšav, ki se ne tičejo naloge, prosim ne vključujte v vejo z nalogo. So pa seveda takšni predlogi dobrodošli, le v svoji veji naj bodo. Izboljšav implementacije matrik (glej spodaj) trenutno sicer ne bom sprejemal.

## Implementacija

Priložen je modul `matrix` z razredom `AbstractMatrix`, ki implementira osnovne funkcionalnosti matrike. Naj bosta `M` in `N` matriki razreda `AbstractMatrix`. Na voljo je sledeča funkcionalnost:

* `M[i, j]` vrne vrednost v vrstici `i` in stolpcu `j`.
* `M[i:k, j:l]` vrne *podmatriko* z vrsticami od `i` do `k-1` in stolpci od `j` do `l-1`. Spreminjanje podmatrike vpliva na originalno matriko. Mogoče je uporabiti tudi druge oblike rezin oziroma rezino na eni dimenziji nadomestiti s številom.
* `M[i:k, j:l] = N` prepiše vrednosti v navedeni podmatriki z istoležnimi vrednostmi v matriki `N`. Tako kot prej je mogoče rezine nadomestiti tudi s posameznimi indeksi; na desni lahko matriko nadomestimo s skalarjem.
* `M + N` in `M - N` vrneta vsoto oziroma razliko matrik `M` in `N` (ustvari se nova matrika).
* `M += N` in `M -= N` matriki `M` prišteje oziroma odšteje matriko `N` (ne ustvari se nova matrika). Mogoče je tudi kombinirati s podmatrikami.
* `M * k` oziroma `k * M` vrne produkt matrike `M` s skalarjem `k`.
* `M *= k` pomnoži matriko `M` s skalarjem `k`.
* `M == N` vrne `True`, če sta matriki enaki (enakih dimenzij z enako vsebino).
* `M.copy()` vrne novo matriko z istimi dimenzijami in vsebino kot `M`.

Natančnejša dokumentacija je na voljo v komentarjih v modulu [`matrix.py`](matrix/matrix.py).

V razredu `AbstractMatrix` je definirana tudi funkcija `multiply`, ki pa ni implementirana. Ta dobi na vhod dve matriki, njun produkt pa naj zapiše v matriko, na kateri je bila klicana. Vaša naloga bo torej, da napišete nekaj podrazredov razreda `AbstractMatrix`, ki bodo čim bolj učinkovito implementirali to metodo.

1. Razred `SlowMatrix` naj v metodi `multiply` implementira naivno množenje matrik.
2. Razred `FastMatrix` naj v metodi `multiply` implementira varianto Strassenovega algoritma, ki bo delovala za matrike poljubnih velikosti.
3. Razred `CheapMatrix` naj v metodi `multiply` implementira varianto Strassenovega algoritma, ki bo delovala za matrike poljubnih velikosti, poleg tega pa sme porabiti le O(log(*kmn*)) dodatnega prostora (poleg vhodnih matrik), kjer sta matriki, ki ju množimo, dimenzij *k × m* in *m × n*. V ta namen naj ima metoda še en neobvezen argument z delovno matriko, katere dimenzije naj bodo enake dimenzijam ciljne matrike (če ta ni podana, sme metoda ustvariti svojo). Metoda sme med delovanjem spreminjati vhodne matrike, a mora ob vrnitvi povrniti prvotno stanje (za delovno matriko to ni potrebno).

*Namig*: če v rekurziji srečaš matriko z lihim številom vrstic oziroma stolpcev, izvedi rekurzijo na podmatrikah enakih dimenzij ter zadnjo vrstico oziroma stolpec obravnavaj posebej.

V podrazredih z implementirano metodo `multiply` bo potem na voljo sledeča dodatna funkcionalnost:

* `M * N` vrne novo matriko s produktom matrik `M` in `N` (ustvari se nova matrika `P` in na njej kliče `P.multiply(M, N)`).
* `M *= N` z desne primnoži matriko `N` k matriki `M` (ustvari se nova matrika s produktom, nato pa se prepiše matrika `M`).

Svojo implementacijo postavite v eno ali več Pythonovih programov znotraj mape `naloge/2016/dn1/matrix/ImePriimek`, kjer `ImePriimek` nadomestite s svojim imenom in priimkom. V tej mapi naj bo tudi program `__init__.py`, kjer uvozite svoje razrede (glej [vzorec](matrix/vzorec/__init__.py)). Potem bo ob poganjanju Pythonove konzole iz mape `naloge/2016/dn1/` možno uvoziti vaše razrede, npr.
```python
>>> from matrix.ImePriimek import CheapMatrix
>>> X = CheapMatrix([[ 1,  2,  3,  4],
...                  [ 5,  6,  7,  8],
...                  [ 9, 10, 11, 12],
...                  [13, 14, 15, 16],
...                  [17, 18, 19, 20]])
>>> Y = CheapMatrix([[ 1,  2,  3,  4,  5,  6],
...                  [ 7,  8,  9, 10, 11, 12],
...                  [13, 14, 15, 16, 17, 18],
...                  [19, 20, 21, 22, 23, 24]])
>>> X * Y
[  130   140   150   160   170   180 ]
[  290   316   342   368   394   420 ]
[  450   492   534   576   618   660 ]
[  610   668   726   784   842   900 ]
[  770   844   918   992  1066  1140 ]
```
Poskrbite, da bo koda berljiva in komentirana.

## Poročilo

Napišite tudi poročilo, v katerega vključite sledeče:

1. Kratek opis vaših algoritmov.
2. Natančna analiza časovne in prostorske zahtevnosti vaših algoritmov v odvisnosti od dimenzij vhodnih matrik.
3. Primerjava dejanskih časov izvajanja vaših algoritmov pri vhodih različnih velikosti.

Poročilo imate lahko kar v datoteki `README.md` v mapi z vašimi programi (v obliki [Markdown](https://guides.github.com/features/mastering-markdown/)), lahko pa naredite tudi poročilo v LaTeXu (na repozitorij naložite datoteko `.tex` - datoteke `.pdf` so izključene v `.gitignore` in jih torej ne nalagajte).

## Rok za oddajo

Svojo nalogo oddajte (odprite *pull request*) do **nedelje, 18. decembra**.

**Nalogo delajte samostojno!**

### Vso srečo!
