# Poročilo

*Juš Kosmač*

## Opis algoritma
Podmnožice na ciklu predstavimo kot nize ničel in enic oziroma kot dvojiške zapise števil manjših od `2^k`. Enice ustrezajo izbranim vozliščem, ničle pa tistim, ki jih nismo izbrali. Možni so le nizi, ki nimajo dveh zaporednih enic (torej nismo izbrali sosednih vozlišč na ciklu). Vse možne podmnožice shranimo v slovar. Prav tako si shranimo, katere podmnožice se ujemajo med sabo (to pomeni, da lahko ti dve množici uporabimo pri ciklih dveh sosednih vozlišč v drevesu in bo unija še vedno neodvisna). To so ravno vsi pari nizov, ki nimajo podvojenih enic na istem mestu. Nato pa z DFS-jem pregledamo celotno drevo - vemo, da se bo funkcija postvisit klicala najprej na otrocih in šele nato na starših. Za vsako vozlišče drevesa in vsako možno izbiro podmnožice na pripadajočem ciklu izračunamo maksimalno težo poddrevesa, ki ima dano vozlišče za koren in se dejanska podmnožica cikla pri korenu ujema z izbrano podmnožico. Pri tem uporabljamo že izračunane vrednosti za otroke vozlišča. Shranjujemo si teže in tudi katero podmnožico smo dejansko izbrali. Optimalno rešitev preberemo pri korenu drevesa. Naredimo še en obhod drevesa z DFS-jem in rekonstruiramo celotno množico izbranih vozlišč.   
Podrobnejši komentarji o delovanju algoritma so v datoteki z algoritmom. 

## Časovna in prostorska zahtevnost

### Generiranje vseh možnosti za podmnožice na ciklu in ujemanj med njimi
Vsako število med 1 in `2^k` pretvorimo v niz ničel in enic dolžine `k`, ki ustreza njegovemu dvojiškemu zapisu. Za to porabimo `O(k)` operacij in prostora. Še enkrat pregledamo celoten niz, da preverimo, če se kje pojavita dve zaporednici enici - časovna zahtevnost `O(k)`. Če je niz ustrezen, ga dodamo v slovar možnosti. Preštejmo, koliko je ustreznih nizov. Naj `a_k` označuje število nizov dolžine `k` iz ničel in enic, ki nimajo dveh zaporednih enic. Če je na prvem mestu enica, mora biti naslednja ničla in nato utrezen niz dolžine `k-2`. Če je prva ničla, pa ji sledi utrezen niz dolžine `k-1`. Torej velja rekurzivna formula `a_k = a_(k-1) + a_(k-2)`. Z `b_k` pa označimo take ustrezne nize, pri katerih tudi prva in zadnja številka nista obe enici. Če je prva enica, sta druga in zadnja ničli, če pa je prva ničla, nima vpliva na druge. Torej je `b_k = a_(k-1) + a_(k-3)`. Asimptotično gledano narašča `a_k` eksponentno z osnovo, ki je enaka večji ničli karakterističnega polinoma `x^2 - x - 1`. To pa je ravno vrednost zlatega reza `A = (1 + sqrt(5))/2`. Ker je `b_k` samo vsota dveh členov `a_k`, velja `b_k = O(a_k)`. Vrnimo se nazaj na naš slovar vseh možnosti. Pravkar smo izpeljali, da ima slovar `O(A^k)` vnosov, vsak izmed njih pa je niz dolžine `k`. Torej je skupna prostorska zahtevnost `O(k * A^k)`.

Časovna zahtevnost : `O(k * 2^k)`  
Prostorska zahtevnost: `O(k) + O(k * A^k) = O(k * A^k)`

Za vsako število v slovarju možnosti gremo še enkrat skozi isti slovar, da pregledamo s katerimi preostalimi možnostmi se ujema. Predpostavljamo, da so števila tako majhna, da je operacija `&` konstantna in da je potreben prostor za hranjenje posameznega števila tudi konstanten. V resnici je časovna zahtevnost `&` odvisna od `k`, vendar računalnik lahko dela z `32` oziroma `64` biti hkrati. Že pri taki velikosti `k` pa bo algoritem praktično neuporaben, saj se bo izvajal več milijard let. Za oceno velikosti slovarja ujemanj definiramo `c_k` kot število ujemanj med vsemi nizi, ki smo jih prešteli z `a_k`. Potrebovali bomo tudi `d_k` - definiramo ga enako kot `c_k`, le da od enega izmed nizov zahtevamo, da se začne z ničlo. Poiščimo rekurzivne zveze. Pri `c_k` se lahko niza začneta z `(0,0), (0,1)` ali `(1,0)`. Pri zadnjih dveh primerih moramo v naslednjem koraku od enega izmed nizov zahtevati, da se začne z ničlo (da bo ustrezal zahtevi `a_k`). Torej velja `c_k = c_(k-1) + 2 * d_(k-1)`. Pri `d_k` pa izbiramo le začetek drugega niza (drugi se mora začeti z ničlo), torej `d_k = d_(k-1) + c_(k-1)`. Iz teh dveh rekurzivnih zvez lahko izrazimo `c_k = 2 * c_(k-1) + c_(k-2)`. Enako kot prej označimo večjo ničlo karakterističnega polinoma `x^2 - 2 * x - 1` z `B = 1 + sqrt(2)`. V resnici pa je vseh ujemanj (označimo z `g_k`) manj, saj nismo upoštevali, da morata začetka in konca obeh nizov ustrezati dodatni zahtevi kot pri zaporedju `b_k`. Lahko pa ocenimo: `c_(k-1) <= g_k <= c_k`, saj vsakemu izmed nizov dolžine `k-1` lahko na konec dodamo ničlo in dobimo ujemanje dveh nizov dolžine `k`. Torej velja `g_k = O(c_k)`. Vsako ujemanje pa v slovarju ujemanj ustreza enemu število, torej `O(1)` prostora. 

Časovna zahtevnost : `O(A^k * A^k) = O((A^2)^k)`  
Prostorska zahtevnost: `O(B^k)`  

### Prvi obhod drevesa z DFS-jem
Oglejmo si funkcijo _izracunaj_, ki jo uporabljamo v postvisitu. označimo število sosedov vozlišča _u_ s `s(u)`. Najprej naredimo seznam vseh sosedov, porabimo `O(s(u))` prostora in časa. Nato za vsako možnost iz slovarja možnosti v slovar tež zapisemo težo ustrezne podmnožice na ciklu. Tukaj spet predpostavljamo, da so teže dovolj majhne, da so osnovne aritmetične operacije z njimi konstantne. Opravimo `O(A^k)` klicev funkcije _teza_, ki ima časovno zahtevnost `O(k)` in prostorsko zahtevnost `O(1)`. Skupaj porabimo `O(k * A^k)` časa in `O(A^k)` prostora (prostor se sešteva, ker vse zapisujemo v slovar tež). Nato pa za vsako možnost in vsako ujemanje izračunamo maksimalno težo vozlišča skupaj z otroci in jo shranimo v slovar rezultatov. Za vsakega otroka porabimo le konstantno operacij (poizvedbe v slovar in prištevanje). Porabimo `O(s(u) * B^k)` časa in `O(s(u) * B^k)` prostora. 

Časovna zahtevnost : `O(s(u)) + O(k * A^k) + O(s(u) * B^k)`  
Prostorska zahtevnost: `O(s(u)) + O(A^k) + O(s(u) * B^k)`  

Skupna zahtevnost DFS-ja je seštevek teh zahtevnosti po vseh vozliščih. Pri tem štejemo prostorsko zahtevnost za ustvarjanje seznama sosedov in slovarja tež le enkrat (pri vozlišču z največ sosedi), saj ju pri vsakem vozlišču na novo prepišemo. V resnici s tem v splošnem nič ne prihranimo, saj ima lahko v najslabšem primeru eno vozlišče vsa ostala vozlišča za sosede.

Časovna zahtevnost za celoten DFS: `O(n) + O(n * k * A^k) + O(n * B^k) = O(n * B^k)`  
Prostorska zahtevnost za celoten DFS: `O(n) + O(A^k) + O(n * B^k) = O(n * B^k)`  

### Drugi obhod drevesa z DFS-jem
Najprej ustvarimo seznam izbranih podmnožic - prostorska in časovna zahtevnost `O(n)`. Sedaj kot previsit funkcijo kličemo _dodaj_vozlisca_. Vask klic funkcije popravi vrednost v seznamu predhodnikov in seznamu optimalno doda največ `k` vozlišč. Torej ima časovno in prostorsko zahtevnost `O(k)`. 

Časovna zahtevnost za celoten DFS: `O(n * k)`  
Prostorska zahtevnost za celoten DFS: `O(n * k)`

### Skupaj
Seštejemo vse prostorske in časovne zahtevnosti.  
Skupna časovna zahtevnost : `O(k * 2^k) + O((A^2)^k) + O(n * B^k) + O(n * k) = O(n * B^k + (A^2)^k)`  
Skupna prostorska zahtevnost: `O(k * A^k) + O(B^k) + O(n * B^k) + O(n * k) = O(n * B^k)`

## Primerjava časov izvajanja algoritma
Algoritem bomo testirali na naključno generiranih drevesih s težami vozlišč med `0` in `100`. Pri prvem testu bomo preverjali odvisnost od števila vozlišč v drevesu `n`. Omejili se bomo na nekaj izbranih velikosti cikla `k`, `n` pa bomo povečevali. 

|`k` \ `n`  |100|200|300|400|500|1000|2000|3000|4000|5000|10000|
|---|---|---|---|---|---|---|---|---|---|---|---|
|4   |0.02  |0.02   |0.02  |0.03  |0.03  |0.08  |0.17 |0.25 |0.33 |0.42 |0.86|
|8   |0.13  |0.25   |0.36  |0.50 |0.63  |1.22 |2.49|3.72|5.03 |6.19|12.39|
|12  |3.52  |6.95  |10.36  |13.92  |17.30   |34.72  |69.19 |104.00 |138.13 |173.88|347.22|

Sedaj pa bomo preverjali še odvisnost od dolžine cikla `k`.

|`n` \ `k`  |10|11|12|13|14|15|16|17|18|19|20|
|---|---|---|---|---|---|---|---|---|---|---|---|
|100   |0.64  |1.48   |3.50 |8.30  |19.84  |48.13 |117.48|287.38 |691.20 |1707.73 |4239.5|
|200   |1.27  |2.94  |6.94  |16.63|39.39  |95.19 |234.47|568.94|1382.05 |3424.84|8520.6|
|300  |1.89  |4.41  |40.45  |24.55 |58.91  |142.02 |347.08 |850.58 |2089.97 |5070.50|12570.6|

Povprečno razmerje

|10|11|12|13|14|15|16|17|18|19|
|---|---|---|---|---|---|---|---|---|---|
|2.32 |2.37  |2.37 |2.39  |2.42 |2.44 |2.43|2.45 |2.46 |2.48|

Oglejmo si še odvisnost od oblike drevesa. Algoritem bomo testirali na treh različnih oblikah dreves: poti, razvejanem drevesu in naključnem drevesu.

Pot

|`k` \ `n`  |250|500|750|1000|
|---|---|---|---|---|
|6   |0.08  |0.14  |0.23 |0.30  |
|9   |0.72 |1.48  |2.23 |3.02 |
|12  |9.25  |18.81 |27.88  |37.47|
|15  |127.05 |257.72  |383.31  |513.70  |

Razvejano drevo

|`k` \ `n`  |250|500|750|1000|
|---|---|---|---|---|
|6   |0.06 |0.14  |0.22 |0.28 |
|9   |0.65  |1.33  |2.02  |2.73 |
|12  |8.45 |18.28 |28.55 |38.75 |
|15  |134.44  |279.33 |429.11  |574.75  |

Naključno drevo

|`k` \ `n`  |250|500|750|1000|
|---|---|---|---|---|
|6   |0.06 |0.14  |0.20 |0.28 |
|9   |0.69  |1.39   |2.06 |2.77|
|12  |8.75 |17.356  |26.14 |34.94 |
|15  |118.27 |236.19 |355.77 |476.34 |




