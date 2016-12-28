# Poročilo

*Luka Lajovic*

Slow matrix izvede naivno množenje preko vmesne metode slabo_mnozenje.
Izvede ga tako, da trenutno matriko pomnoži iz leve z novo matriko (A.slabo_množenje(B))

Fast matrix izvede Strassenov algoritem prav tako preko vmesne metode, ki se tokrat imenuje dobro_mnozenje ta metoda najprej preveri če je kakšen stolpec ali vrstica dolžine 1 in če je izvede naivno množenje.
Sicer preveri če je ima prvotna matrika liho število stolpcev, če jih ima opravi z zadnjo vrstico posebaj množenje z celo matriko in dobljeno vrstico 
prilepi na zadnjo vrstico rezultata, z preostankom matrike pa rekurzivno nadaljujemo.
A-(nxm),B-(mxl)
A*B=[A[:n-1,:m]*B]
	[A[n-1,:m]*B]

Če ima prvotna matrika liho število stolpcev posebaj množino njen zadnjo stolpec z drugo matriko in  rekurzivno preostanek pomnožimo z matriko.
Na koncu pa oba rezultata seštejemo
A*B=A[:n,:m-1]*B[:m-1,:l]+A[:n,m-1]*B[m-1,:l]
Če ima druga matrika liho število stolpcev njen zadnji stolpec posebaj množimo z prvotno matriko in ju prilepimo v zadnji stolpec.
A*B=[A*B[:m,:l-1],A*B[:m,l-1]]
Sicer imamo 2 popolnoma sodi matriki sepravi lahko vsako razdelimo na 4 enako velike dele in izvedemo naš algoritem.

Za Prejšni 2 množenji sem sproti ustvarjal ničelne marike, velikosti nxl, ki so nastale z dodatno metodo nicelna_matrika(sefl,a,b) (a in b sta dimenzije ki jih vrne).

Za zadnjo množenje (poceni množenje) se ustvari ničelno matriko samo enkrat in se jo rekurzivno prenaša naprej, s tem ne polnimo prostora z
dodatnim ustvarjanjem matrik.  

