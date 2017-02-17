# Poročilo



*Jure Hostnik*



### Kratek opis algoritmov

* `SlowMatrix` dela skalarne produkte vrstic prve matrike in stolpcev druge matrike z uporabo `for` zank

	in vgrajene funkcije `sum` ter množenjem ustreznih elementov podanih matrik.

* `FastMatrix` najprej preveri, če je katera od dimenzij matrik enaka 0 in v tem primeru naredi enako kot `SlowMatrix`.

	Nato preveri, če so vse dimenzije enake 1 in v tem primeru zmnoži skalarja podanih matrik.

	Sicer pa razdeli podani matriki vsako na 4 bloke za polovico manjših dimenzij. Če je katera dimenzija liha,

	se zaokroži navzdol. Potem izvede Strassenov algoritem z uporabo rekurzivnega množenja ustreznih blokov oz. njihovih vsot/razlik.

	Pri tem se ustvarjajo nove matrike `P1`, ... , `P7`. Nove matrike se ustvarjajo tudi pri seštevanju blokov. V primeru,

	da je bila katera dimenzija podanih matrik liha, se na koncu poračuna še zadnja vrstica/stolpec produkta oz.

	se vsakemu elementu prišteje ustrezna vrednost.

* `CheapMatrix` deluje po enakem principu kot `FastMatrix`, ampak bloke prišteva enega k drugemu (`+=`) in namesto `*`

	uporablja metodo `multiply`. Poleg tega uporablja delovno matriko oz. njene bloke. Po vsaki uporabi `+=` se izvede

	še `-=`, da se ohranja prvotno stanje podanih matrik in po vsaki uporabi delovne matrike oz. njenega bloke se ta

	pomnoži z 0 (`*= 0`), da ne pride do napak pri rekurzivnem računanju.



### Analiza časovne in prostorske zahtevnosti

* `SlowMatrix` izvede 3 `for` zanke dolžin `m` (višina leve matrike), `o` (dolžina desne matrike) in

	`n` (dolžina leve matrike oz. višina desne matrike) ter vsakič naredi en produkt skalarjev, to pomeni,

	da ima časovno zahtevnost `O(mon)`. Produktna matrika ima dimenziji `m` in `o`, torej je skupna prostorska zahtevnost `O(mo)`.
 
* `FastMatrix` rekurzivno reši 7 problemov za polovico manjših dimenzij, na vsakem koraku rekurzije pa porabi še
	`5*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), `5*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov),

	`8*O((m//2)(o//2))` (vsote/razlike (m//2)x(o//2) blokov), `O(mo)` (če je n liho), `O(m)` (če je o liho), `O(o)` (če je m liho)
	in `O(1)` (ostale elementarne operacije) časa. To skupaj nanese 
`O(mn + on + mo)` časa na vsakem koraku rekurzije. 
	Če s `k` označimo `k = max(m, o, n)`, po znanem izreku dobimo časovno zahtevnost 
`O(k^(log_2(7))) = O(k^2,81)`.

	Prostorsko pa na vsakem koraku porabi `5*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), 
	`5*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov), `15*O((m//2)(o//2))` (matrike `P1`, ... , `P7` in njihove vsote/razlike)

	in `O(1)` (ostale spremenljivke), kar skupaj nanese `O(mn + on + mo)` prostora. Podobno kot pri časovni zahtevnosti, sedaj dobimo

	`O(k^2,81), k = max(m, o, n)` prostorsko zahtevnost.

* `CheapMatrix` rekurzivno reši 7 problemov za polovico manjših dimenzij, na vsakem koraku rekurzije pa porabi še

	`10*O((m//2)(n//2))` (vsote/razlike (m//2)x(n//2) blokov), `10*O((o//2)(n//2))` (vsote/razlike (o//2)x(n//2) blokov),

	`23*O((m//2)(o//2))` (vsote/razlike (m//2)x(o//2) blokov oz. množenje s skalarjem), `O(mo)` (če je n liho),
	`O(m)` (če je o liho), `O(o)` (če je m liho) in `O(1)` (ostale elementarne operacije) časa.

	Od tu naprej dobimo enako kot pri `FastMatrix` časovno zahtevnost `O(k^2,81), k = max(m, o, n)`.

	`CheapMatrix` ne porabi nič dodatnega prostora, poleg matrike `self` pa ustvari  še matriko `work` enakih dimenzij, torej

	je skupna prostorska zahtevnost `O(mo)`.



Pri vseh izračunih sem upošteval, da se notranje spremenljivke metode po njenem koncu pobrišejo.



### Primerjava dejanskih časov izvajanja algoritmov

| m   | n   | o   | CheapMatrix | FastMatrix | SlowMatrix |
| --- | --- | --- | ----------- | ---------- | ---------- |
| 32  | 32  | 32  | 1.59848     | 2.40001    | 0.18277    |
| 10  | 100 | 10  | 0.29896     | 0.37935    | 0.05271    |
| 100 | 100 | 100 | 15.7382     | 21.2088    | 6.11371    |
| 500 | 500 | 500 | 1180.42     | 1420.07    | 1970.04    |
| 600 | 700 | 600 | 4654.98 | / | /

Šele pri dovolj velikih dimenzijah matrik se rezultati začnejo ujemati z izračunanimi časovnimi zahtevnostmi.
To pomeni, da pisanje in brisanje iz spomina (ki se ne upošteva pri računanju časovne zahtevnosti) porabi toliko več časa,
da pri manjših dimenzijah `FastMatrix` in `CheapMatrix` delujeta bistveno počasneje od `SlowMatrix`. Pri velikih dimenzjah
pa pride do izraza časovna zahtevnost računskih operacij in dejanski rezultati se začnejo ujemati z izračunanimi.

Pri dimenzijah trikrat velikosti 500 je `SlowMatrix` že počasnejši. `CheapMatrix` deluje hitreje od `FastMatrix`, saj slednji 
porabi več časa za pisanje/brisanje v spomin. Mogoče pa bi pri še večjih dimenzijah `FastMatrix` prehitel `CheapMatrix`, ki ima večjo
konstanto pri časovni zahtevnosti, vendar nimam več časa, da bi to preveril.