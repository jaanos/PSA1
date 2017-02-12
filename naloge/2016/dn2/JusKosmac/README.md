# Poročilo

*Juš Kosmač*

## Časovna in prostorska zahtevnost

### Generiranje vseh možnosti za podmnožice na ciklu in ujemanj med njimi
Vsako število med 1 in `2^k` pretvorimo v niz ničel in enic dolžine `k`, ki ustreza njegovemu dvojiškemu zapisu. Nato pa niz spremenimo v seznam ničel in enic. Za to porabimo `2 * O(k)` operacij. Še enkrat pregledamo celoten seznam, da preverimo, če se kje pojavita dve zaporednici enici - zahtevnost `O(k)`. Če je seznam ustrezen, ga dodamo v slovar možnosti. Preštejmo, koliko je ustreznih seznamov. Naj `a_k` označuje število nizov dolžine `k` iz ničel in enic, ki nimajo dveh zaporednih enic. Če je na prvem mestu enica, mora biti naslednja ničla in nato utrezen niz dolžine `k-2`. Če je prva ničla, pa ji sledi utrezen niz dolžine `k-1`. Torej velja rekurzivna formula `a_k = a_(k-1) + a_(k-2)`. Z `b_k` pa označimo take ustrezne nize, pri katerih tudi prva in zadnja številka nista obe enici. Če je prva enica, sta druga in zadnja ničli, če pa je prva ničla, nima vpliva na druge. Torej je `b_k = a_(k-1) + a_(k-3)`. Asimptotično gledano narašča `a_k` eksponentno z osnovo, ki je enaka večji ničli karakterističnega polinoma `x^2 - x - 1`. To pa je ravno vrednost zlatega reza `A = (1 + sqrt(5))/2`. Ker je `b_k` samo vsota dveh členov `a_k`, velja `b_k = O(a_k)`. Vrnimo se nazaj na naš slovar vseh možnosti. Pravkar smo izpeljali, da ima slovar `O(A^k)` vnosov, vsak izmed njih pa je seznam dolžine `k`. Torej je skupna prostorska zahtevnost `O(k * A^k)`.

Časovna zahtevnost : `O(k * 2^k)`  
Prostorska zahtevnost: `O(k * A^k)`
