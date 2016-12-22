# Poročilo

*Janez Radešček*

A = M^(a,c)
B = M^(c,b)
C = A * B

## SlowMatrix

Matrični produkt po definiciji. Časovna zahtevnost je O(a*b*c). Prostorska zahtevnost je O(a*b).

## FastMatrix

Če je ena izmed matrika vektor, ju zmnožimo na običajen način. V naprotnem primeru preverimo ali so dimenzije matrik lihe. Če so lihe, največji sodi podmatriki in ostanek zmnožimo posebej, in iz njuju sestavimo produkt prvotnih matrik. Če so dimenzije sode, levo in desno matriko razdelimo vsako na 4 podmatrike, rekurzivno izračunamo 7 produktov, ki jin nato uporabimo za izračun prvotnega produkta. Časovna zahtevnost je O(). Prostorska zahtevnost je O().
