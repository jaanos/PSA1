# Poročilo
*Jan Golob*

Množimo matiki velikosti **m** x **k** in **k** x **n**
** g := max{m, n, k} **

## SlowMatrix
Uporablja naivno množenje matrik.

### Čas
Za vsak element v ciljni matriki porabimo k množenj. V ciljni matriki je m vrstic in n stolpcev.
Torej: Časovna zahtevnost je **T(k,n,m) = O(kmn) = O(g^3).**

### Prostor
Poleg vhodnih in končne matrike, SlowMatrix še prostor za začasno vsoto (spremenljivka vs v kodi).
To je dodatnega **O(ln(_N_))** prostora.


## FastMatrix
Rekurzivno uporablja [Strassenov algoritem](http://wiki.fmf.uni-lj.si/wiki/Strassenovo_mno%C5%BEenje_matrik) za bločne matrika. Ko naleti na liho dimenzijo matrike, jo osami in izračuna z algoritmom SlowMatrix

### Čas
Na nekem nivoju rekurzije za (m, k, n) velike matrike pomnnožimo 7 podmatrik, ki jih dobivamo s seštevanjem in odštevanjem, ne smemo pozabiti pa tudi na množenje "osamljenih" stolpcev oziroma vrstic. Za seštevanje in odštevanje porabimo O(g^2). In pravtako porabimo O(g^2) za množenje osamljenih stolpcev in vrstic (glej časovno zahtevnost SlowMatrix, le da je eden izmed m, k, n enak 1).
Torej: T(g) = 7 x T(g/2) + O(g^2). Po Krovnem izreku sledi **T(g) = O(g^[log_2(7)])**

### Prostor
Poleg vhodnih in končne matrike, FastMatrix porabi še 7 matrik velikosti m/2 x n/2 za izračun teh pa še 10 matrik iste velikosti. Spet ne smemo pozabiti prostor porabljen pri osamljenih vrsticah oz stolpcih, ki je O(ln(g)).
Torej: Dodatno porabimo **17 x O(mn/4) + O(ln(g))**

## CheapMatrix
Rekurzivno poteka CheapMatrix podobno kot FastMatrix, le da se porabi največ še ena matrika prostora.

### Čas
Algoritem je enak kot pri Fastmatrix, le da se shranjujjo stvari malce drugače. Zato po podobnem sklepu kot zgoraj pridemo do časovne zahtevosti **T(g) = O(g^[log_2(7)])**

### Prostor
Ko množimo naivno porabimo tako kot pri SlowMatrix O(log(g)) prostora, kar je ravno ena komponenta v matriki work
Pri Strassenovem algoritmu pa si bomo označili kam si bomo spravili kateri vmesni produkt. Namesto seštevanja, pa bomo komponente A-G le začasno popravili (več o tem v komentarjih)

| self: |    |   | work: |    |
|-------|----|---|-------|----|
| P6    | P2 |   | P3    | P5 |
| P4    | P1 |   | P7    | M  |

Vmesne rezultate smo postavili v matriko self kot kaže tabela, zato, ker se te ne pojavljajo več v enačbah po tem, ko smo opravili z tisto podmatriko(da ne bi prišlo do napak(prištevanje, že popravljene matrike))
Podmatrika M pa je delovna matrika za množenja pri katerih dobimo vmesne podmatrike P.
Torej: Vidimo da poleg vhodnih in končne matrike potrebujemo še eno matriko, ki je istih dimenzij kot končna. Sledi da porabimo še dodatnega **O(mn)** prostora.

## Testiranje:
1. Pri majhnih velikostih je SlowMatrix hitrejši od FastMatrix in CheapMatrix. Koeficienti pri časovni zahtevnosti teh 2 algoritmov so veliki.
2. CheapMatrix je pribljižno 2krat hitrejša od FastMatrix. Seštevanje je pri njej bolj časovno ugodno.
3. CheapMatrix in FastMatrix naraščata skokovito pri potencah števila 2, medtem pa SlowMatrix narašča bolj zvezno

### Tabela časov
Spodaj je tabela časov za matrike z naključno generiranimi elementi (men 0 in 9) ter časom potrebnim za množenje matrik velikosti m x n in n x m:

| m | k | n | Slow | Fast | Cheap |
|---|---|---|------|------|-------|
| 2 | 2 | 2 | 6.457268703628472e-05 | 0.0010814855994355234 | 0.00038016634950501405 |
| 3 | 3 | 3 | 0.00012615193824969532 | 0.0016433962667578952 | 0.0007628985011439199 |
| 4 | 4 | 4 | 0.00022878402360537948 | 0.007767965960358357 | 0.003687912933780922 |
| 5 | 5 | 5 | 0.00041565994569052293 | 0.008602279287562272 | 0.0033244242981462085 |
| 7 | 7 | 7 | 0.0015903696893241233 | 0.030732750326070684 | 0.007177831469563169 |
| 8 | 8 | 8 | 0.0015476063204259288 | 0.07114327866749341 | 0.029523829887318526 |
| 9 | 9 | 9 | 0.0021582672282922377 | 0.05923539096410016 | 0.03757061301289316 |
| 15 | 15 | 15 | 0.009413072761872143 | 0.09451345977036074 | 0.048323034488657046 |
| 16 | 16 | 16 | 0.011940815497444857 | 0.39406914836750834 | 0.16811905321901255 |
| 17 | 17 | 17 | 0.014901323526267385 | 0.397028373495264 | 0.17123607517800266 |
| 31 | 31 | 31 | 0.091391306207103 | 0.69895400799675 | 0.3797532553614573 |
| 32 | 32 | 32 | 0.10017875088199446 | 3.018772691312621 | 1.0332258547328355 |
| 33 | 33 | 33 | 0.11169578139365832 | 2.845287262930574 | 1.0622249780837745 |
| 100 | 100 | 100 | 3.7262874981290963 | 30.22643417648443 | 14.785279565524178 |
|   |   |   |      |      |       |
| 28 | 32 | 32 | 0.10262481558297162 | 0.5537296072184567 | 0.27958861639119925 |
| 40 | 43 | 46 | 0.25838653809147083 | 3.1590536466462824 | 1.3148068164810027 |
| 49 | 54 | 47 | 0.4310979494964613 | 4.014014411255318 | 1.877762192905557 |
| 62 | 59 | 52 | 0.7738685881673764 | 4.823242746263553 | 2.378529795377279 |
| 63 | 70 | 61 | 0.9405405289828757 | 4.460101776817979 | 2.3208834912014353 |
| 72 | 73 | 75 | 1.385250914067008 | 19.98685325749963 | 7.976849622613273 |
| 84 | 77 | 84 | 2.0269742778336095 | 21.580232632726812 | 8.84283093502107 |
