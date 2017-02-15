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

## Število bitmaskov

Vseh nizov enic in ničel dolžine k je 2^k. Število veljavnih bitmask bo neka podmnožica te množice iz česar lahko predvidevamo, da se bo število
veljavnih bitmaskov povečevalo eksponentno. S pomočjo dinamičnega programiranja izračunamo število veljavnih bitmask. Spodaj je tabela dobljenih vrednosti.

|    2    |   3  |    4    |    5    |    6    |    7    |    8    |    9    |    10   |    11   |    12   |    13   |    14   |    15   |    16   |    17   |    18   |    19   |    20   |    21   |    22   |    23   |    24   |    25   |    26   |    27   |    28   |    29   |
|:-------:|:----:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
|    3    |   4  |    7    |    11   |    18   |    29   |    47   |    76   |   123   |   199   |   322   |   521   |   843   |   1364  |   2207  |   3571  |   5778  |   9349  |  15127  |  24476  |  39603  |  64079  |  103682 |  167761 |  271443 |  439204 |  710647 | 1149851 |
| 1.33333 | 1.75 | 1.57143 | 1.63636 | 1.61111 | 1.62069 | 1.61702 | 1.61842 | 1.61789 | 1.61809 | 1.61801 | 1.61804 | 1.61803 | 1.61804 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 | 1.61803 |         |

V prvi vrstici so dolžine ciklov. V drugi število veljavnih bitmaskov za to dolžino, v tretji vrstici pa imamo kvocient števila veljavnih bitmaskov za dolžino i + 1 in dolžino i.
Kvocienti hitro skonvergirajo k vrednosti 1.618033988749895, kar pa je ravno (1 + koren(5))/2. Število bitmaskov bo torej za primerne k enako ((1 + koren(5))/2)^k.

Označimo B = (1 + koren(5))/2. Število veljavnih bitmaskov za določeno dolžino k je torej B^k.

Zanima nas še pričakovana vrednost bitmaskov, ki se ujemajo z dano bitmasko. 

| Dolžina cikla | Število veljavnih bitmask | Povprečno število ujemanj |
|:--:|:----:|:----------:|
|  2 |   3  |   2.33333  |
|  3 |   4  |   3.25000  |
|  4 |   7  |   5.00000  |
|  5 |  11  |   7.36364  |
|  6 |  18  |  11.05556  |
|  7 |  29  |  16.44828  |
|  8 |  47  |  24.57447  |
|  9 |  76  |  36.64474  |
| 10 |  123 |  54.69106  |
| 11 |  199 |  81.59296  |
| 12 |  322 |  121.74845 |
| 13 |  521 |  181.65259 |
| 14 |  843 |  271.04033 |
| 15 | 1364 |  404.40836 |
| 16 | 2207 |  603.40507 |
| 17 | 3571 |  900.31952 |
| 18 | 5778 | 1343.33662 |
| 19 | 9349 | 2004.34667 |

Opazimo lahko, da razmerje povprečnih ujemajočih se bitmaskov in vseh veljavnih bitmaskov pada. Ker nas v glavnem zanimajo dovolj veliki k bomo privzeli
da je povprečno število ujemanj enako 1/4 vseh veljavnih bitmask.

## Prostorska zahtevnost

Za najtežjo množico bo potrebno izračunati najtežje množice vseh poddreves in to za vsako možno bitmasko, ki jo je imel predhodnik. Ker delamo
rekurzivno in si vsako rešitev shranjujemo v slovar, to pomeni, da bomo imeli n*število_bitmaks ključev v slovarju. Pri vsakem ključu imamo za vrednost
najtežjo množico tega podrevesa in sicer kot nabor vozlišča in bitmaske uporabljene na tem vozlišču. Dolžina tega nabora je odvisna od števila vozlišč
v posameznem podrevesu. Bolj kot je drevo razvejano, manjša bo povprečna dolžina nabora. Najslabši primer pa bo takrat, ko bo drevo kar pot. Ker je pot zelo
zdegeneriran primer naključnega drevesa lahko raje ocenimo kakšna bo povprečna dolžina naključnega drevesa in neka groba ocena bo število_vozlišč v drevesu/2.

Prostor, ki ga vzame memoizacija je torej velikosti O(n^2 * število_bitmask) = O(n^2 * B^k). 

Poleg memoizacije pa si naredimo tudi slovar vseh bitmask in njihovih ujemanj. Za fiksno dolžino k je le teh B^k. Za vsak ključ pa imamo v povprečju 
1/4 * B^k vrednosti. Prostorska zahtevnost tega slovarja je potem O(0.25 * B^(2*k)).

Skupna prostorska zahtevnost algoritma je O(n^2 * B^k + B^(2*k)).

V primeru implementacije algoritma od spodaj navzgor, bi se nam bilo potrebno naenkrat zapomniti samo eno plast največjih neodvisnih množic. S tem 
bi lahko znižali prostorsko zahtevnost.

## Časovna zahtevnost

* V algoritmu najprej generiramo bitmaske. To delamo z naivno metodo in sicer za generiranje bitmask dolžine k, se zapeljemo z zanko do 0 do števila 2^k in
preverimo kateri bitmaski so veljavni. Algoritem bi lahko izboljšali s tem, da bi bitmaske generirali rekurzivno in tako izpustili vse kose števil za katera
recimo binarni zapis vsebuje dve enici na začetku.  Ko generiramo še vse ujemajoče bitmaske nam ta del da časovno zahtevnost O(2^k * B^k). Pri tem predpostavimo,
da operacija AND dveh števil porabi O(1) časa.

* Tekom iskanja največje množice se z funkcijo kličemo enkrat na vsakem vozlišču drevesa in na vsaki možni bitmaski. V primeru večkratnega klicanja
funkcije na istih argumentih zaradi memoizacije dobimo rezultat v O(1). Vseh različnih argumentov za klic funkcije je n * B^k. 


# Meritve časovne zahtevnosti

Za prvo merjenje sem generiral naključna drevesa T s k vozlišči in algoritem uporabil na kartezičnem produktu T x C4, T x C7 in T x C10.

Iz grafa se jasno vidi linearna časovna zahtevnost v številu vozlišč.

 ![Graf izmerjenih časov](Stvozlisc.png)

| Število vozlišč v drevesu | Dolžina cikla: 4 | Dolžina cikla: 7 | Dolžina cikla: 10 |
|:-----:|:---------:|:---------:|:----------:|
|  20 | 0.00154 | 0.01242 | 0.13514 |
| 100 | 0.00700 | 0.06514 | 0.76954 |
| 180 | 0.01350 | 0.12204 | 1.43123 |
| 260 | 0.02001 | 0.19147 | 2.09189 |
| 340 | 0.02700 | 0.23753 | 2.84346 |
| 420 | 0.03302 | 0.28954 | 3.46403 |
| 500 | 0.03900 | 0.37599 | 4.39033 |
| 580 | 0.07058 | 0.43152 | 4.94373 |
| 660 | 0.07901 | 0.50501 | 5.74741 |
| 740 | 0.06054 | 0.58156 | 6.40926 |
| 820 | 0.09851 | 0.62162 | 7.33915 |
| 900 | 0.10700 | 0.66433 | 7.87683 |
| 980 | 0.11949 | 0.72626 | 8.58420 |

Za merjenje zahtevnosti v dolžini cikla pa sem generiral drevesa na 50, 100 in 200 vozliščih in izračunal T x Ck.

Iz grafa lahko preberemo eksponentno rast časa v odvisnosti od dolžine cikla. Za oceno osnove eksponenta pa si poglejmo kvociente sosednjih izmerjenih
časov. 

Poglejmo si nekaj kvocientov v spodnjem delu tabele:

* 470 / 179 = 2.6256
* 224 / 86 = 2.604
* 1023 / 364 = 2.8104
* 364 / 143 = 2.5384
* 143 / 56 = 2.5535
* 179 / 69 = 2.5942
* ...

Lahko sklepamo, da osnova pri eksponentu leži nekje med 2.5 in 2.8.
Iz te tabele prav tako lahko preberemo linearno rast v število vozlišč, če recimo pogledamo določeno vrstico v tabeli.
Čas, ki ga porabimo za drevo z 100 vozlišči je približno 2-krat večji kot čas, ki ga potrebujemo za drevo z 50 vozlišči.

 ![Graf izmerjenih časov2](dolzinacikla.png)

| Dolžina cikla | Vozlišč v drevesu: 50 | Vozlišč v drevesu: 100 | Vozlišč v drevesu: 200 |
|:----:|:-----------:|:-----------:|:------------:|
|  2 |  0.00100 |  0.00296 |  0.00500  |
|  3 |  0.00150 |  0.00400 |  0.00750  |
|  4 |  0.00350 |  0.00702 |  0.01505  |
|  5 |  0.00700 |  0.01555 |  0.02956  |
|  6 |  0.01419 |  0.02995 |  0.07080  |
|  7 |  0.03053 |  0.06569 |  0.13400  |
|  8 |  0.06801 |  0.14605 |  0.31313  |
|  9 |  0.16005 |  0.35005 |  0.67514  |
| 10 |  0.43650 |  0.76567 |  1.66729  |
| 11 |  0.86164 |  1.78279 |  3.77038  |
| 12 |  2.10203 |  4.40730 |  9.05810  |
| 13 |  4.72122 | 10.33312 |  22.08986 |
| 14 | 11.50032 | 25.23384 |  53.53822 |
| 15 | 28.78786 | 65.75724 | 137.32453 |



