# Poročilo

*Janez Radešček*

A = M^(a,c)
B = M^(c,b)
C = A * B

Za lažje računanje nekje privzamemo, da so matrike kvadratne in definiramo n = max(a,b,c), m = n^2.

## SlowMatrix

Matrični produkt po definiciji. Časovna zahtevnost je O(a*b*c). Prostorska zahtevnost je O(a*b).

## FastMatrix

Če je ena izmed matrika vektor, ju zmnožimo na običajen način. V naprotnem primeru preverimo ali so dimenzije matrik lihe. Če so lihe, največji sodi podmatriki in ostanek zmnožimo posebej, in iz njuju sestavimo produkt prvotnih matrik. Če so dimenzije sode uporabimo običajen Strassenov algoritem, se pravi levo in desno matriko razdelimo vsako na 4 podmatrike, rekurzivno izračunamo 7 produktov, ki jin nato uporabimo za izračun prvotnega produkta. Če predpostavimo da so matrike približno kvadratne, potem je časovna zahtevnost T(m) = 7*T(m/4) + O(m). Po krovnem izreku je T(m) = O(m^(log4(7))), kar je O(n^2,807). Podobno je prostorska zahtevnost je O(n^2,807).

## CheapMatrix

Nadgranja FasrMatrix. povsod pazimo da ne ustvarjamo novih matrik ampak zapisujemo v A,B,C ali WORK. V glavnem delu namesto, da najprej poračunamo vseh 7 produktov in jih nato seštejemo v C, poračunamo najprej en produkt, ga  prištejemu pravemu delu matrike C in nato računamo naslednjega. Časovna zahtevnost se ne spremeni torej O(n^2,807). Prostorska zahtevnost je O(a*b) saj imamo ves čas le 2 matriki, C in WORK.
