# Poročilo

*Samo Kralj*

# Opis algoritma

Ideja algoritma je, da se osredotočimo na drevo in z dinamičnim programiranjem poiščemo najtežjo množico. Ker pa nimamo samo drevesa ampak imamo
produkt drevesa in cikla, si lahko ta graf predstavljamo kot drevo, ki ima potem na vsakem vozlišču še cikel. Generiramo si bitmaske, ki nam povedo
katera vozlišča v ciklu imamo v naši množici. Iz tega pa sedaj dinamično programiranje na drevesu sledi. In sicer:

Recimo da imamo v korenu drevesa določeno masko B. Če želimo dobiti najtežjo množico s tem, da smo na korenu uporabili masko B, 
moramo poiskati najtežjo množico na vseh sinovih našega korena, pod pogojem da se maska C od sinova ne prekriva z masko B od korena oziroma, 
da je (B AND C = 0).

Tukaj pa vidimo, da se nam velikokrat ponovi problem, ki ga računamo, saj je vsako vozlišče z določeno bitmasko na korenu sam svoj problem
iskanja najtežje množice. Z memoizacijo pridemo do učinkovitega algoritma.

# Analiza časovne zahtevnosti

# Meritve časovne zahtevnosti

Za prvo merjenje sem generiral naključna drevesa T s k vozlišči in algoritem uporabil na kartezičnem produktu T x C10 (Cikel dolžine 10).

| Število vozlišč v drevesu   | Porabljen čas  |
|-----|----------|
| 10  | 0.43858  |
| 15  | 0.74536  |
| 20  | 1.04644  |
| 25  | 1.37600  |
| 30  | 1.72525  |
| 35  | 2.07384  |
| 40  | 2.47772  |
| 45  | 2.80225  |
| 50  | 3.20433  |
| 55  | 3.57355  |
| 60  | 3.96455  |
| 65  | 4.40207  |
| 70  | 4.85732  |
| 75  | 5.36459  |
| 80  | 5.79920  |
| 85  | 6.24826  |
| 90  | 6.87379  |
| 95  | 7.22393  |
| 100 | 7.82496  |
| 105 | 8.47500  |
| 110 | 8.89144  |
| 115 | 9.49064  |
| 120 | 10.13619 |
| 125 | 10.65953 |
| 130 | 11.14275 |
| 135 | 11.80502 |
| 140 | 12.45661 |
| 145 | 13.17187 |
| 150 | 13.77690 |
| 155 | 14.64177 |
| 160 | 15.99252 |
| 165 | 16.41437 |
| 170 | 16.97465 |
| 175 | 17.68168 |
| 180 | 18.96902 |
| 185 | 20.04530 |
| 190 | 20.83415 |
| 195 | 21.35211 |
| 200 | 21.95483 |

Za merjenje zahtevnosti v dolžini cikla, pa sem si generiral drevesa T z 50 vozlišči in uporabil algoritem na kartezičnem produktu T x Ci (Cikel dolžine i).

| Dolžina cikla | Porabljen čas |
|----|-----------|
| 2  | 0.00256   |
| 3  | 0.00501   |
| 4  | 0.01350   |
| 5  | 0.03150   |
| 6  | 0.08103   |
| 7  | 0.20362   |
| 8  | 0.50153   |
| 9  | 1.27148   |
| 10 | 3.25023   |
| 11 | 8.66683   |
| 12 | 21.19055  |
| 13 | 53.78827  |
| 14 | 134.73871 |



