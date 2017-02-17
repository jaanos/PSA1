# Poročilo

*Nina Slivnik*

## Kratek opis algoritma
Z dinamičnim programiranjem poiščemo najtežjo množico v drevesu. 
Ker imamo produkt drevesa in cikla, imamo na vsakem vozlišču drevesa še en cikel.
Zato na vsakem koraku dinamičnega programiranja pregledamo neodvisne množice cikla v nekem vozlišču in jih primerjamo z rešitvami sinov; na koncu izberemo unijo z največjo težo.
V algoritmu imamo 4 funkcije, to so:
* *dfs_usmerjeno_drevo* (iz neusmerjenega drevesa naredimo usmerjeno drevo z vrhom v 0)
* *combinations* (vse kombinacije števil od 0 do *k*)
* *vsi_neodvisni_cikli* (vrne vse neodvisne podmnožice cikla dolžine *k*)
* *dfs* (glavna funkcija, ki drevo obhodi v globino; na vsakem koraku pogleda, ali so sinovi trenutnega vozlišča že 'rešeni' in nato izračuna rešitev za trenutno vozlišče).

## Časovna in prostorska zahtevnost
### Časovna zahtevnost
* *dfs_usmerjeno_drevo*: *n^3*
* *combinations*: pri vseh klicih skupaj *2^k*, vsaka je dolga največ *k*, torej skupaj *k 2^k*
* *vsi_neodvsni_cikli*: *k 2^k*
* *dfs*: za vsako od *n* vozlišč izračunamo vse neodvisne podmnožice, torej *n k 2^k*, nato vsako vozlišče (razen korena) pripnemo očetu, kjer naredimo *2^k 2^k k* primerjanj, torej skupaj *2^(2k) k n* operacij, na koncu še poiščemo najboljšo rešitev (pri korenskem vozlišču), torej med vsemi njegovimi *2^k* podmnožicami. To je skupaj *O(2^k k n)*.
Skupaj je časovna zahtevnost *O(n^3 + 2^k k n)* oz. *O(2^k k n)*.

### Prostorska zahtevnost
* *dfs_usmerjeno_drevo*: *2n*
* *combinations*: pri vseh klicih skupaj *2^k*, vsaka je dolga največ *k*
* *vsi_neodvsni_cikli*: *2^k* ciklov, vsak dolžine *k*
* *dfs*: Podobno kot pri časovni zahtevnosti. Na začetku poiščemo neodvisne podmnožice za vsako vozlišče (vsakič je prepišemo, zato ni *n*), torej *k 2^k*. Nato z *dfs* na vsakem vozlišču primerjamo neodvisne podmnožice, ampak si ne zapomnimo vseh rešitev, samo tisto od očeta, (ki pa ima največ *k n* vozlišč), torej *2^k k n* prostora. Skupaj je to *2^k k n*.
Skupna prostorska zahtevnost: *O(2^k k n)*.

## Primerjava dejanskih časov
Najprej si oglejmo čase za pot (pri dolžinah cikla 2, 5 in 10):
| n      | 100    | 200      | 300      | 400      | 500       | 600       | 700       | 800       | 900       |
|--------|--------|----------|----------|----------|-----------|-----------|-----------|-----------|-----------|
| k = 2  | 0.0    | 0.0      | 0.0      | 0.03125  | 0.015625  | 0.015625  | 0.03125   | 0.03125   | 0.0625    |
| k = 5  | 0.0625 | 0.046875 | 0.09375  | 0.109375 | 0.140625  | 0.171875  | 0.21875   | 0.265625  | 0.34375   |
| k = 10 | 2.3125 | 4.65625  | 7.265625 | 9.921875 | 12.734375 | 15.734375 | 19.140625 | 22.484375 | 25.921875 |
ter za binarno kopico:
| n      | 100      | 200      | 300      | 400      | 500      | 600       | 700      | 800       | 900      |
|--------|----------|----------|----------|----------|----------|-----------|----------|-----------|----------|
| k= 2   | 0.0      | 0.0      | 0.0      | 0.015625 | 0.015625 | 0.03125   | 0.03125  | 0.046875  | 0.0625   |
| k = 5  | 0.03125  | 0.046875 | 0.078125 | 0.078125 | 0.09375  | 0.125     | 0.140625 | 0.171875  | 0.1875   |
| k = 10 | 2.171875 | 4.390625 | 6.625    | 9.125    | 11.4375  | 13.421875 | 15.65625 | 17.890625 | 20.21875 |

![Graf pot]
(https://github.com/SlivnikN/PSA1/blob/master/naloge/2016/dn2/pot.jpg)
![Graf binarna kopica]
(https://github.com/SlivnikN/PSA1/blob/master/naloge/2016/dn2/binarna_kopica.jpg)

Na grafih rdeča predstavlja *k = 10*, modra *k = 5* in zelena *k = 2*.
Vidimo, da čas za konstanten *k* linearno narašča in da algoritem bolje deluje za binarne kopice kot za pot (največji čas za pot je prbl. 25, za binarno kopico pa prbl. 20).