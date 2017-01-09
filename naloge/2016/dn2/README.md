# 2. domača naloga pri PSA1: maksimalna neodvisna množica v kartezičnem produktu cikla in drevesa

Vaša naloga je, da v programskem jeziku *Python 3* napišete algoritem, ki kot vhod dobi:

- neusmerjeno drevo *T* z *n* vozlišči, in
- dvodimenzionalno tabelo tež *w* dimenzij *k*×*n* (*k* ≥ 2),

poišče pa najtežjo neodvisno množico v kartezičnem produktu cikla *Cₖ* in drevesa *T*, kjer so teže vozlišč podane v tabeli *w*. Algoritem naj teče v času, ki je polinomski v *n* in eksponenten v *k* (tj., za fiksen *k* dobite polinomski algoritem).

Cikel *Cₖ* je neusmerjen graf z vozlišči 0, 1, ..., *k*-1, kjer sta vozlišči *i* in *j* sosedni natanko tedaj, ko velja *i*-*j* ≡ ±1 (mod *k*). *Neodvisna množica* *S* v grafu *G* je taka množica vozlišč grafa *G*, da nobeni dve vozlišči iz *S* nista sosedni v *G*. *Kartezični produkt* *G* ▫ *H* grafov *G* in *H* je graf, katerega vozlišča so urejeni pari (*u*, *v*), kjer je *u* vozlišče iz *G* in *v* vozlišče iz *H*, vozlišči (*u*, *v*) in (*x*, *y*) pa sta sosedni v *G* ▫ *H*, če bodisi velja *u* = *x* ter sta *v* in *y* sosedni v *H*, ali pa sta *u* in *x* sosedni v *G* in velja *v* = *y*.

Drevo *T* na vhodu naj bo predstavljeno s seznamom sosednosti, torej kot seznam *n* seznamov, pri čemer seznam *T*[*u*] \(0 ≤ *u* ≤ *n*-1) vsebuje indekse vozlišč, ki so sosedna *u*. Če velja *v* ∊ *G*[*u*], naj seveda velja tudi *u* ∊ *G*[*v*]. Teža *w*[*i*][*u*] \(0 ≤ *i* ≤ *k*-1, 0 ≤ *u* ≤ *n*-1) predstavlja težo vozlišča (*i*, *u*) v kartezičnem produktu *Cₖ* ▫ *T*.

Algoritem naj vrne par (*c*, *s*), kjer je *c* cena najdene neodvisne množice, *s* pa seznam parov (*i*, *u*) (0 ≤ *i* ≤ *k*-1, 0 ≤ *u* ≤ *n*-1), ki predstavljajo vozlišča v najdeni neodvisni množici.

## Orodja

Za izdelavo naloge boste uporabili git repozitorij, ki bo kopija (*fork*) repozitorija predmeta na [GitHub](https://github.com/jaanos/PSA1)u oziroma [Bitbucket](https://bitbucket.org/jaanos/psa1)u (uporabite seveda isti repozitorij kot za prvo domačo nalogo). Toplo priporočam, da si naredite novo vejo (*branch*) ter vse delo v zvezi z nalogo poteka v tej veji (seveda lahko po potrebi naredite še več vej). Pazite, da v svoji veji na začetku nimate commitov, ki niso bili sprejeti v glavni repozitorij - najbolje bo, če nadaljujete kar iz veje za 1. domačo nalogo. Vse vaše spremembe (vključno z morebitnimi testi) naj bodo v mapi `naloge/2016/dn2/ImePriimek`, kjer `ImePriimek` nadomestite s svojim imenom in priimkom. Ko boste z nalogo zaključili, boste naredili *pull request* svoje veje na vejo `dn2-2016-oddaje` na originalnem repozitoriju, potem pa bom vaše spremembe potegnil vanj.

## Implementacija

Implementirali boste modul z imenom `ImePriimek` - v mapi `naloge/2016/dn2/ImePriimek` naj bo torej program `__init__.py` s funkcijo `maxCycleTreeIndependentSet(T, w)`, ki izvede zahtevani algoritem. Samo funkcijo (in morebitne pomožne funkcije) lahko seveda definirate drugje - v ta namen uporabite relativno uvažanje (glej [vzorec](vzorec/__init__.py)). Potem bo ob poganjanju Pythonove konzole iz mape `naloge/2016/dn2/` možno uvoziti vašo funkcijo, npr.
```python
>>> from ImePriimek import maxCycleTreeIndependentSet
>>> T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
>>> w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],
...      [3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],
...      [8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],
...      [5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]
>>> maxCycleTreeIndependentSet(T, w)
(153, [(0, 0), (2, 0), (1, 1), (3, 1), (0, 3), (2, 3), (0, 4), (2, 4), (1, 5), (3, 5), (1, 6), (3, 6), (1, 7), (3, 7), (1, 8), (3, 8), (0, 9), (2, 9), (0, 10), (2, 10), (0, 11), (2, 11), (1, 12), (3, 12), (0, 13), (2, 13)])
```
Poskrbite, da bo koda berljiva in komentirana. Lahko si pomagate z algoritmi in strukturami, ki ste jih srečali na [vajah](../../../vaje/) - v tem primeru kar skopirajte želeno kodo k sebi, in jo po potrebi priredite. Lahko pa seveda sami poskrbite za implementacijo potrebnih algoritmov in struktur.

**_Namig_**: spremenljivih podatkovnih tipov, kot so seznami, slovarji in množice, ni mogoče uporabiti v ključih slovarjev in v elementih množic. V ta namen jih lahko nadomestite z nespremenljivimi tipi, kot so terice (`tuple`) in zamrznjene množice (`frozenset`).

## Poročilo

Napišite tudi poročilo, v katerega vključite sledeče:

1. Kratek opis vašega algoritma.
2. Natančna analiza časovne in prostorske zahtevnosti vašega algoritma v odvisnosti od parametrov *n* in *k*.
3. Primerjava dejanskih časov izvajanja vašega algoritma pri vhodih različnih velikosti.

Poročilo imate lahko kar v datoteki `README.md` v mapi z vašimi programi (v obliki [Markdown](https://guides.github.com/features/mastering-markdown/)), lahko pa naredite tudi poročilo v LaTeXu (na repozitorij naložite datoteko `.tex` - datoteke `.pdf` so izključene v `.gitignore` in jih torej ne nalagajte).

## Rok za oddajo

Svojo nalogo oddajte (odprite *pull request* na vejo `dn2-2016-oddaje`) najmanj **3 dni** pred pristopom k ustnemu izpitu. Zadnji rok za oddajo domače naloge (tudi, če boste ustni izpit opravljali kasneje) je **petek, 17. februar**. V pull requestu prosim napišite, kdaj nameravate iti na ustni izpit.

**Nalogo delajte samostojno!**

### Vso srečo!
