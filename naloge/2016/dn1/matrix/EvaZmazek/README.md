# Poročilo

*Eva Zmazek*

1.del: SlowMatrix:
Dve matriki A in B lahko množimo med seboj, če je število stolpcev leve matrike enako številu vrstic desne matrike.
Njun produkt je enak matriki C velikosti nXm, pri čemer je n enako številu vrstic prve matrike in m številu stolpcev druge matrike.
(i,j)-ti element matrike c je enak skalarnemu produktu i-te vrstice matrike A in j-tega stolpca matrike B.
V metodi SlowMatrix si najprej sharnimo velikosti matrik A in B, ki jih dobimo s pomočjo ukazov ".ncol" in ".nrow", nato pa se sprehodimo čez tri for zanke.
Torej sprehodimo se čez vse vrstice prve matrike (prva for zanka) in vse stolpce druge matrike (druga for zanka), nato pa s tretjo for zanko izvedemo skalarni produkt,
izbran vrstice matrike A in izbranega stolpca matrike B. ta skalarni produkt nato shranimo v element matrike C, ki leži v isti vrstici, kot izbrana vrstica v prvi for zanki,
in istem stolpcu kot izbran stolpec druge for zanke.
Vrnemo matriko C.

2.del: FastMatrix:

3.del: CheapMatrix:

vzorec
Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

Če se odločite za pisanje poročila v LaTeXu, to omenite tukaj in na repozitorij naložite datoteko `.tex`.
