#Poročilo
##Opis algoritma
Algoritem temelji na osnovi dinamičnega programiranja. Ideja je da začnemo v neki točki v drevesu potem pa rekurzivno iščemo maksimum teže neodvisne množice v ciklu na tej točki plus sosedi, ki jih izračunamo rekurzivno. V vsaki točki moramo izračunati vse neodvisne množice v odvisnosti od točke iz katere prihajamo in izbrane množice v tisti točki in pa tudi vrednost v še neobiskanih sosedih v odvisnosti od trenutne točke in izbrane vrednosti. Ker se parametri naše funkcije velikokrat ponovijo uporabljamo memorizacijo.

##Časovna zahtevnost

algoritem drevo porabi `O(n)` za računanje sosedov `O(k)` za konstrukcijo cikla in njegovo prirejanje. Za izračun vseh neodvisnih množic H se porabi približno `O(1.6^k)` kjer sem stevilo 1.6 dobil tako da sem velikost mnozice delil z velikostjo prejsne in je konvergiralo proti 1.6. Za vsak izračun elementa pa porabimo še dodatnih `O(1.6^k)` operacij v najslabšem primeru. Torej računanje neodvisnih množic proabi `O(1,6^2k)`. Pri racunanju maksimuma se izvaja rekurzija zato se algoritem drevo izvede za vsako sosednje vozlisce in to najvec `1.6^k`-krat. Torej se rekurzija izvede najvec `O(1.6^k)` krat za vsako vozlisce. Ker uporabljamo memorizacijo je to najvec n*1.6^k krat saj ce smo neko vozlisce ze obiskali porabimo zanj `O(1)`.
Vse skupaj torej nanese `O(1.6^k*n(n+k+1.6^2k))=O(1.6^(3k)*n+1.6^2k*n^2)`

##Prostorska zahtevnost

V vsakem koraku si zapomnemo listo ze obiskanih vozlisc ki je najvec `O(n)`. Ce se to zgodi za vseh `n*1,6^k` ponovitev, ki niso memorizirane dobimo `O(n^2*1,6^k)`. Po istem principu vidimo da je tudi za seznam moznih sosedov porabljeno `O(1,6^k*n^2)` prostora. Za shranitev ciklov `O(k*n*1,6^k)`. Za shranitev H porabimo najvec `O(1,6^k)` če ga moramo shraniti v vsaki iteraciji to nanese `O(1,6^2k*n)`
Za memorizacijo dreves porabimo `O(1,6^k*n)` za memorizacijo neodvisnih mnozic pa `O(1,6^k)` za eno in `O(2^k)` moznih torej `O(1,6^k*2^k)`
Skupaj imamo torej `O(1,6^k*2^k+1,6^2k*n)`

##Meritve časovne zahtevnosti
| n  | k | čas                   |
|----|---|-----------------------|
| 14 | 2 | 0.0                   |
| 14 | 3 | -0.009999990463256836 |
| 14 | 4 | 0.0                   |
| 14 | 5 | 0.0                   |
| 14 | 6 | -0.009999990463256836 |
| 14 | 7 | -0.03000020980834961  |
| 14 | 8 | -0.07999992370605469  |
| 14 | 9 | -0.17000031471252441  |
| 19 | 2 | -0.009999990463256836 |
| 19 | 3 | 0.0                   |
| 19 | 4 | 0.0                   |
| 19 | 5 | -0.010000228881835938 |
| 19 | 6 | -0.019999980926513672 |
| 19 | 7 | -0.04999995231628418  |
| 19 | 8 | -0.09999990463256836  |
| 19 | 9 | -0.24100041389465332  |
| 74 | 2 | -0.009999990463256836 |
| 74 | 3 | -0.009999990463256836 |
| 74 | 4 | -0.019999980926513672 |
| 74 | 5 | -0.040000200271606445 |
| 74 | 6 | -0.09000015258789062  |
| 74 | 7 | -0.20100021362304688  |
| 74 | 8 | -0.43700313568115234  |
| 74 | 9 | -1.0340015888214111   |

Kot pričakovano časovna zahtevnost narašča zelo hitro za k medtem ko je naraščanje po n počasnejše



