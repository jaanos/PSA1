# Poročilo

*Jure Hostnik*

### Kratek opis algoritmov
SlowMatrix dela skalarne produkte vrstic prve matrike in stolpcev druge matrike z uporabo `for` zank
in vgrajene funkcije `sum` ter množenjem ustreznih elementov podanih matrik.
FastMatrix najprej preveri, če je katera od dimenzij matrik enaka 0 in v tem primeru naredi enako kot SlowMatrix.
Nato preveri, če so vse dimenzije enake 1 in v tem primeru zmnoži skalarja podanih matrik.
Sicer pa razdeli podani matriki vsako na 4 bloke za polovico manjših dimenzij. Če je katera dimenzija liha,
se zaokroži navzdol. Potem izvede Strassenov algoritem z uporabo rekurzivnega množenja ustreznih blokov oz. njihovih vsot/razlik.
Pri tem se ustvarjajo nove matrike `P1`, ... , `P7`. Nove matrike se ustvarjajo tudi pri seštevanju blokov. V primeru,
da je bila katera dimenzija podanih matrik liha, se na koncu poračuna še zadnja vrstica/stolpec produkta oz.
se vsakemu elementu prišteje ustrezna vrednost.
CheapMatrix deluje po enakem principu kot FastMatrix, ampak bloke prišteva enega k drugemu (`+=`) in namesto `*`
uporablja metodo `multiply`. Poleg tega uporablja delovno matriko oz. njene bloke. Po vsaki uporabi `+=` se izvede
še `-=`, da se ohranja prvotno stanje podanih matrik in po vsaki uporabi delovne matrike oz. njenega bloke se ta
pomnoži z 0 (`*= 0`), da ne pride do napak pri rekurzivnem računanju.

### Analiza časovne in prostorske zahtevnosti
SlowMatrix izvede 3 for zanke dolžin `m` (višina leve matrike), `o` (dolžina desne matrike) in 
`n` (dolžina leve matrike oz. višina desne matrike) ter vsakič naredi en produkt skalarjev, to pomeni,
 da ima časovno zahtevnost `O(mon)`. Produkt ima dimenziju `m` in `o`, torej je prostorska zahtevnost `O(mo)`.
FastMatrix rekurzivno reši 7 problemov za polovico manjših dimenzij, na vsakem koraku rekurzije pa porabi še 
`5*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), `5*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov), 
`8*O((m//2)(o//2))` (vsote/razlike (m//2)x(o//2) blokov) in `O(1)` (ostale elementarne operacije) časa. To skupaj nanese 
`O(mn + on + mo)` časa na vsakem koraku rekurzije. Če s `k` označimo `k = max(m, o, n)`, po znanem izreku dobimo časovno zahtevnost 
`O(k^(log_2(7))) = O(k^2,81)`.
Prostorsko pa na vsakem koraku porabi `5*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), 
`5*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov), `15*O((m//2)(o//2))` (matrike `P1`, ... , `P7` in njihove vsote/razlike)
in `O(1)` (ostale spremenljivke), kar skupaj nanese `O(mn + on + mo)` prostora. Podobno kot pri časovni zahtevnosti, sedaj dobimo
`O(k^2,81), k = max(m, o, n)` prostorsko zahtevnost.
CheapMatrix rekurzivno reši 7 problemov za polovico manjših dimenzij, na vsakem koraku rekurzije pa porabi še 
`10*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), `10*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov), 
`23*O((m//2)(o//2))` (vsote/razlike (m//2)x(o//2) blokov oz. množenje s skalarjem) in `O(1)` (ostale elementarne operacije) časa.
Od tu naprej dobimo enako kot pri FastMatrix časovno zahtevnost `O(k^2,81)`.
CheapMatrix ne porabi nič dodatnega prostora, poleg matrike `self` pa ustvari  še matriko `work` enakih dimenzija, torej
je prostorska zahtevnost `O(mo)`.
Pri vseh izračunih sem upošteval, da se notranje spremenljivke metode po njenem koncu pobrišejo.

### Primerjava dejanskih časov izvajanja algoritmov
```
>>> a = rand(32, 32)
>>> b = rand(32, 32)
>>> A = CheapMatrix(a)
>>> B = CheapMatrix(b)
>>> C = FastMatrix(a)
>>> D = FastMatrix(b)
>>> E = SlowMatrix(a)
>>> F = SlowMatrix(b)
>>> cas(A, B)
1.598481627184984
>>> cas(C, D)
2.400012808842721
>>> cas(E, F)
0.1827674869575553
>>> a = rand(10, 100)
>>> b = rand(100, 10)
>>> A = CheapMatrix(a)
>>> B = CheapMatrix(b)
>>> C = FastMatrix(a)
>>> D = FastMatrix(b)
>>> E = SlowMatrix(a)
>>> F = SlowMatrix(b)
>>> cas(A, B)
0.29896468854039426
>>> cas(C, D)
0.37934997572969564
>>> cas(E, F)
0.05271398729125565
>>> a = rand(100, 100)
>>> b = rand(100, 100)
>>> A = CheapMatrix(a)
>>> B = CheapMatrix(b)
>>> C = FastMatrix(a)
>>> D = FastMatrix(b)
>>> E = SlowMatrix(a)
>>> F = SlowMatrix(b)
>>> cas(A, B)
15.738194254149136
>>> cas(C, D)
21.208754039072574
>>> cas(E, F)
6.113708926398488
```
Rezultati se ne ujemajo z izračunanimi časovnimi zahtevnostmi...
Ali imam vse narobe ali pa pisanje in brisanje iz spomina porabi toliko več časa.
