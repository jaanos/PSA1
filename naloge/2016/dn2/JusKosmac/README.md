# Poročilo

*Juš Kosmač*

## Časovna in prostorska zahtevnost

### Generiranje vseh možnosti za podmnožice na ciklu in ujemanj med njimi
Vsako število med 1 in `2^k` pretvorimo v niz ničel in enic dolžine `k`, ki ustreza njegovemu dvojiškemu zapisu. Nato pa niz spremenimo v seznam ničel in enic. Za to porabimo `2 * O(k)` operacij. Še enkrat pregledamo celoten seznam, da preverimo, če se kje pojavita dve zaporednici enici - zahtevnost `O(k)`. Če je seznam ustrezen, ga dodamo v slovar možnosti. Preštejmo, koliko je ustreznih seznamov. Naj `a_k` označuje število nizov dolžine `k` iz ničel in enic, ki nimajo dveh zaporednih enic. Če je na prvem mestu enica, mora biti naslednja ničla in nato utrezen niz dolžine `k-2`. Če je prva ničla, pa ji sledi utrezen niz dolžine `k-1`. Torej velja rekurzivna formula `a_k = a_(k-1) + a_(k-2)`. Z `b_k` pa označimo take ustrezne nize, pri katerih tudi prva in zadnja številka nista obe enici. Če je prva enica, sta druga in zadnja ničli, če pa je prva ničla, nima vpliva na druge. Torej je `b_k = a_(k-1) + a_(k-3)`. Asimptotično gledano narašča `a_k` eksponentno z osnovo, ki je enaka večji ničli karakterističnega polinoma `x^2 - x - 1`. To pa je ravno vrednost zlatega reza `A = (1 + sqrt(5))/2`. Ker je `b_k` samo vsota dveh členov `a_k`, velja `b_k = O(a_k)`. Vrnimo se nazaj na naš slovar vseh možnosti. Pravkar smo izpeljali, da ima slovar `O(A^k)` vnosov, vsak izmed njih pa je seznam dolžine `k`. Torej je skupna prostorska zahtevnost `O(k * A^k)`.

Časovna zahtevnost : `O(k * 2^k)`  
Prostorska zahtevnost: `O(k * A^k)`

Za vsako število v slovarju možnosti gremo še enkrat skozi isti slovar, da pregledamo s katerimi preostalimi možnostmi se ujema. Predpostavljamo, da so števila tako majhna, da je operacija `&` konstantna in da je potreben prostor za hranjenje posameznega števila tudi konstanten. Za oceno velikosti slovarja ujemanj definiramo `c_k` kot število ujemanj med vsemi nizi, ki smo jih prešteli z `a_k`. Potrebovali bomo tudi `d_k` - definirano enako kot `c_k`, le da od enega izmed nizov zahtevamo, da se začne z ničlo. Poiščimo rekurzivne zveze. Pri `c_k`, se lahko niza začneta z `(0,0), (0,1)` ali `(1,0)`. Pri zadnjih dveh primerih moramo v naslednjem koraku od enega izmed nizov zahtevati, da se začne z ničlo (da bo ustrezal zahtevi `a_k`). Torej velja `c_k = c_(k-1) + 2 * d_(k-1)`. Pri `d_k` pa izbiramo le začetek drugega niza (drugi se mora začeti z ničlo), torej `d_k = d_(k-1) + c_(k-1)`. Iz teh dveh rekurzivnih zvez lahko izrazimo `c_k = 2 * c_(k-1) + c_(k-2)`. Enako kot prej označimo večjo ničlo karakterističnega polinoma `x^2 - 2 * x - 1` z `B = 1 + sqrt(2)`. V resnici pa je vseh ujemanj (označimo z `g_k`) manj, saj nismo upoštevali, da morata začetka in konca obeh nizov ustrezati isti zahtevi kot pri zaporedju `b_k`. Lahko pa ocenimo: `c_(k-1) <= g_k <= c_k`, saj vsakemu izmed nizov dolžine `k-1` lahko na konec dodamo ničlo in dobimo ujemanje dveh nizov dolžine `k`. Torej velja `g_k = O(c_k)`.

Časovna zahtevnost : `O((A^k)^2) = O((A^2)^k)`  
Prostorska zahtevnost: `O(B^k)`  

### Prvi obhod drevesa z DFS-jem
Oglejmo si funkcijo _izracunaj_, ki jo uporabljamo v postvisitu. označimo število sosedov vozlišča _u_ s `s(u)`. Najprej naredimo seznam vseh sosedov, porabimo `O(s(u))` prostora in časa. Nato za vsako možnost iz slovarja možnosti v slovar tež zapisemo težo in vozlišča ustrezne podmnožice na ciklu. Tukaj spet predpostavljamo, da so teže dovolj majhne, da so osnovne aritmetične operacije z njimi konstantne. Opravimo `O(A^k)` klicev funkcije _teza_, ki ima časovno in prostorsko zahtevnost `O(k)`. Skupaj porabimo `O(k * A^k)` časa in prostora (prostor se sešteva, ker vse zapisujemo v slovar tež). Nato pa za vsako možnost in vsako ujemanje izračunamo maksimalno težo vozlišča skupaj z otroci in jo skupaj z uporabljenimi vozlišči shranimo v slovar rezultatov. Za vsakega otroka porabimo le konstantno operacij (poizvedbe v slovar in prištevanje). Porabimo `O(s(u) * B^k)` časa in `O(s(u) * k * B^k)` prostora. 

Časovna zahtevnost : `O(s(u)) + O(k * A^k) + O(s(u) * B^k)`  
Prostorska zahtevnost: `O(s(u)) + O(k * A^k) + O(s(u) * k * B^k)`  

Skupna zahtevnost DFS-ja je seštevek teh zahtevnosti po vseh vozliščih. Pri tem štejemo prostorsko zahtevnost za ustvarjanje seznama sosedov in slovarja tež le enkrat (pri vozlišču z največ sosedi), saj ju pri vsakem vozlišču na novo prepišemo. V resnici s tem v splošnem nič ne prihranimo, saj ima lahko v najslabšem primeru eno vozlišče vsa ostala vozlišča za sosede.

Časovna zahtevnost za celoten DFS: `O(n) + O(k * A^k) + O(n * B^k) = O(n * B^k)`  
Prostorska zahtevnost za celoten DFS: `O(n) + O(k * A^k) + O(n * k * B^k) = O(n * k * B^k)`  

### Drugi obhod drevesa z DFS-jem
Najprej ustvarimo seznam predhodnikov - prostorska in časovna zahtevnost `O(n)`. Sedaj kot previsit funkcijo kličemo _dodaj_vozlisca_. Vask klic funkcije popravi vrednost v seznamu predhodnikov in seznamu optimalno doda seznam velikosti največ `k`. Torej ima časovno in prostorsko zahtevnost `O(k)`. 

Časovna zahtevnost za celoten DFS: `O(n * k)`  
Prostorska zahtevnost za celoten DFS: `O(n * k)`

### Skupaj
Seštejemo vse prostorske in časovne zahtevnosti.
Skupna časovna zahtevnost : `O(k * 2^k) + O((A^2)^k) + O(n * B^k) + O(n * k) = O(n * B^k)`  
Skupna prostorska zahtevnost: `O(k * A^k) + O(B^k) + O(n * k * B^k) + O(n * k) = O(n * k * B^k)`  

