*Jan Golob*
# Poročilo

Kot vhodni podatek dobimo utežen kartezičen produkt drevesa z n vozlišči in ciklja s k vozlišči. To je v programu podano z tabelo tež in tabelo sosedov drevesa.
Algoritem vrne tisto množico nepovezanih vozlišč, ki ima največjo "ceno" ter le-to ceno.

Algoritem poteka na podoben način kot algoritem "sahovnica" pri 11 sklopu vaj. Na vsakem vozlišču drevesa T izračunamo maximalno "težko" neodvisno množico vozlišč poddrevesa s korenom v tem vozlišču. In to za vsako možno neodvisen možno podmnožico cikla. Ko tako izračunamo maximalne vrednosti v korenu drevesa. Zdaj izmed teh izberemo maximalno, ki jo vrnemo skupaj z seznamom vozlišč, ki prispevajo k njej.

Poglejmo sedaj dele kode posebej.

## 1 Vse možne neodvisne množice vozlišč cikla Ck:
Na vsakem vozlišči drevesa T se nahaja 1 cikelj dolžine k. Zanimajo nas vse možne neodvisne podmnožice vozlišč, in kakšni sta lahko te množici na sosednjih vozliščih drevesa, da bo njuna unija neodvisna množica. Po definiciji kartezičnega produkta grafov. Bo to takrat ko se podmnožici ne bosta sekali(ne bosta vsebovali vozlišč na istih mestih).
Torej če sta u, v sosednji vozlišči v T. U, V neodvisna podgrafa cikla dolžine k. Bo bo Unija kartezičnih produktov u * U in v * V neodvisna množica vozlišč natanko takrat ko bo presek U in V prazen.
Opazimo da je število različnih neodvisnih podmnožic vozlišč cikla dolžine *k* ravno *Lk* kjer je *Lk* k-to [Lucasovo število](https://en.wikipedia.org/wiki/Lucas_number).
Lukasova števila so podana z rekurzino formulo *L(n) = L(n-1) + L(n-2)* in začetnima številoma *L(0) = 2, L(1) = 1*

Tabela Lucasovih števil:

n| L(n)
--- | --- 
1|1
2|3
