# Poročilo

*Filip Koprivec, 27141059*

## Kratek opis algoritmov

1. Naivno množenje

    V razredu `Slowmatrix` je implementirano naivno množenje matrik, ki matrike zmnoži po šolsko, torej *j*-ti element 
    ciljne matrike v *i*-t i vrstici je skalarni produkt *i*-te vrstice prve in *j*-tega stolpca druge matrike. 
    ~~V ta namen si v razredu SlowMatrix definiramo pomožno statično metodo dot_product, ki sprejme dva vektorja (matriko z eno samo vrstico in matriko z enim samim stolpcem), ter vrne vrednost njunega skalarnega produkta.~~ Ker ta način vsebuje dodatno kopiranje podmatrik je veliko počasnejši, zato skaralno množenje izpeljemo kar v še eni zanki.

2. Strassenovo množenje

    V razredu `FastMatrix` je implementiran Strassenov algoritem za množenje matrik (natančneje Winogradova variacija algoritma, ki namesto 18 opravi zgolj 15 matričnih seštevanj). V rekurzivnem algoritmu najprej poskrbimo za bazični primer, ki se primeri takrat, kadar ima katerakoli od matrik vsaj eno izmed dimenzij enako 1, tako v tem primeru matrike zmnožimo kar z naivnim matričnim množenjem. 

    V glavnem delu algoritma najprej predpostavimo, da je leva matrika oblike *2n × 2m*, desna pa *2m × 2k*, in jo kot v klasičnem Strassnovem algoritmu razdelimo na 4 bločne matrike, katerih seštevke potem primerno pomnožimo, da ob pravilnem seštevanju za ciljno matriko potrebujemo zgolj 7 množenj manjših matrik.
      
    V zadnjem delu poskrbimo za matrike lihih dimenzij, kjer primernim bločnim matrikam v ciljni matriki prištejemo dele, ki jih je rekurzivni algoritem zaradi predpostavke o sodosti stranic preskočil. 
    
3. Strassenovo množenje z manjšo porabo spomina

    V razredu `CheapMatrix` je implementirana varainta Strassenovega algoritma, ki porabi manj spomina (dodatnega spomina porabi zgolj dovolj za vzdrževanje sklada ob rekurziji).
    
    Postopamo podobno kot pri standardni implementaciji Strassenovega algoritma, la da moramo biti pri vseh operacija pazljivi in namesto ustvarjanja novih matrik uporabljati spomin, ki nam je na voljo (leva(`A`) in desna(`B`) matrika, ki ju moramo po končanem opravljanju vrniti nazaj na prvotno stanje, matrika rezultata(`C`), ki mora na koncu vsebovati rezultat in delovna matrika(`D`), ki je enakih dimenzij kot `C`, o njej pa nimamo nobenih pogojev) in zato vse operacije izvajamo *na mestu*. 
    
    Tako za računanje produktov vsto bločnih matrik, kjer smo lahko pri `FastMatrix` uporabljali normalno seštevanje najprej *popravimo* osnovno matriko, opravimo množenje rekurzivno, kjer mu za delovno matriko podamo primerno bločno matriko v `D` nato pa prvotno matriko popravimo nazaj (odštejemo/prištejemo kar smo prej prišteli/odšteli). V svoji implementaciji sem za delovno matriko v rekurziji vseskozi uporabljal `D22` saj sem tako imel proste roke za shranjevanje ostalih vmesnih matrik na ostala mesta v delovni matriki.              
    
    Ko smo izračunali vseh 7 rekurzivnih množenj, ki si jih sranjujemo tako v `C` kot v `D` je potrebno vse te bločne matrike še zgolj sestaviti v `C` na pravilen način.
    
    Zadnji del je spet podoben delu v `FastMatrix`, la da je potrebno zopet paziti da na ustvarjamo novih matrik. Tako zopet sledimo isti ideji kot prej, na željeni matriki množimo levo in desno in to matriko. Za razliko od prej si je potrebno nekajkrat pred množenjem *pospraviti* ciljno matriko, čemur bi se sicer lahko izognili, če bi ob vsakem doprištevanju prepisali pravi del ciljne matrike, a se mi zdi da je zaradi jasnosti, za katero bločno matriko rezultata gre vredno žrtvovati nekaj dodatnih operacij.
      
    Ob obravnavanju robnih primerv zaradi lažjega zapisa/razumevanja do dvakrat usvarimo novo `1 × 1` matriko, da lahko normalno kličemo množenje.  
    
    Zgolj zaradi preprostosti večino algoritma implementiramo v *privatni* metodi `_multiply`, kjer lahko eksplicitno zahtevamo podajanje delovne matrike.
    
    
## Analiza časovne zahtevnosti

### Za lažjo analizo bomo predpostavili naslednje:

+ Kot prej poimenujmo levo matriko ki jo množimo: `A`, desno: `B`, trenutno (self): `C` in po potrebi delovno `D`
+ Naj za te matrike velja: `A` je `N × M` matrika, `B` je `M × K` matrika, iz tega torej sledi da sta `C` in `D` `N × K` matriki
+ Nadalje naj velja `n := N // 2`, `m := M // 2`, `k := K // 2` in `L = max{N, M, K}` ter `l = L // 2 = max{n, m, k}`
+ Seštevanje in množenje skalarjev ima konstantno časovno in prostorsko zahtevnost
+ Dostop do posamezne matrike/podmatrike ima konstantno časovno zahtevnosz (če ne pride do kopiranja), v nasprotnem primeru je njegova časovna zahtevnost `O(NK)`, če dostopamo do matrike `N × M`
+ Prepisovanje posamezne matrike/podmatrike velikosti `N × M` ima časovno zahtevnost `O(NM)` in porabi `O(1)` dodatnega prostora.
+ Seštevanje/odštevanje dveh `N × M` matrik ima časovno zahtevnost `O(NM)`, ter ob ustvarjanju nove matrike porabi `O(NM)` dodatnega spomina
+ Prištevanje/odštevanje (z operatorjema `+=` in `-=`) dveh `N × M` matrik, ki se v nadmatriki ne prekrivata ima časovno zahtevnost `O(NM)`, ter porabi `O(1)` dodatnega spomina (po popravku, matrik, ki se prekrivaju ne bomo prištevali in se zato z njihovo prostorsko zahtevnostjo ne bomo ukvarjali)
+ Pomnoževanje matrike s skalarjem (`A *= k`, za skalarni `k`), kjer je `A` `N × M` matrika ima časovno zahtevnost `O(NM)` in porabi `O(1)` dodatnega prostora.
+ `log₂7 ~ 2.80735`

### Analiza

1. Naivno množenje

    Metoda `dot_product` sešteje `a` produktov (opravi `2*a` osnovnih operacij), torej je njena časovna zahtevnost `O(a)`, ker jo uporabljamo za skalarnih produt dveh vektorjev je to kar enako dolžini enega izmed njih, v primeru naše matrike pa kar številu stolpcev v `A` in številu vrstic v `B` torej `O(M)`.

    Metoda `multiply` vsebuje dve gnezdeni `for` zanki, ki se izvedeta do konca, zunanja se izvede `N`-krat, notranja `K` krat, v notranji ~~pa `dot_product` na vektorju dolžine `M`.~~ zanki pa `M` produktov, `M` seštevanj in zapis v matriko. Torej je časovna zahtevnost metode `multiply` v razredu `SlowMatrix` `O(NMK)` oziroma `O(L³)`.

    Dodatna prostorska zahtevnost je neodvisna od velikosti matrike in torej konstantna `O(1)` (če uporabljamo python3, v python2 nam dejstvo, da `range` ni generator pokvari časovno zahtevnost v `O(L)`), drugače pa ob klicu ustvarimo zgolj nekaj dodatnih spremenljivk.

2. Strassenovo množenje

    Najprej se osredotočimo na primer, ko so vse dimenzije tako `A` in `B` matrike deljive z `2`, v baznem primeru v najslabšem primeru opravimo `N × M × K` operacij, kjer je vsaj ena izmed konstant enaka `1`, kar nas v tem primeru še vedno pusti v časovni zahtevnosti `O(L²)`.

    Za analizo časovne zahtevnosti bomo uporabili krovni izrek (Master Theorem), kjer se bomo pri končni analizi, zaradi omejitev le-tega na zgolj eno spremenljivko v rekurzivni zvezi, omejili na največjo izmed dimenzij matrik (`L`).

    Priprava primernih podmatrik zahteva konstantno časovno zahtevnost, nato sledi 8 seštevanj matrik (4 × `n × m` in 4 × `m × k`), kar lahko skupno omejimo z `O(l²) = O(L²)`.

    Sledi 7 rekurzivnih množenj na matrikah pol manjših velikosti (`n × m` × `m × k` matrike), kar lahko na podlagi krovnega izreka zapišemo kot `7T(L/2)`. Potem pa je potrebno dobljene produkte še sestaviti nazaj v skupno matriko, kar vsebuje 7 seštevanj `n × k` matrik in kreiranje treh novih `n × k` matrik, kar lahko spet omejimo z `O(l²) = O(L²)`

    Ob predpostavki, da imamo matrike sodih dimenzij tako velja oblika krovnega izreka: `T(L) = 7×T(L/2) + O(L²)`. Tako imamo verzijo krovnega izreka za `log₂7 > 2` in torej velja ocena časovne zahtevnosti `O(n^(log₂7))`.

    Da bo časovna ocena res veljala, se je potrebno prepričati, da tudi obravnavanje dodatne vrstice (preveč) ne poveča časovne zahtevnosti, da še vedno ustreza izpeljavi časovne zahtevnosti s pomočjo krovnega izreka je dovolj, če pokažamo, da ima časovno zahtevnost `O(L²)`.

    Največja časovna zahtevnost bo dosežena, ko se bo izvedla vsa koda (ko bodo vse dimenzije lihe). Najpomembnejša je ugotovitev, da so vse dodatne matrike, ki pri tem nastanjejo zgolj stolpci ali pa vrstice (lahko je tudi zgolj `1 × 1` matrika v primeru `A33` ali `B33`), tako da ja seštevanje ali pa množenje takih matrik z ustreznimi matrikami vedno  `O(L²)`, število teh operacij pa je konstantno (do 19 množenj in do 14 seštevanj). Tako ocena da je časovna zahtevnost za razdelitev podproblema in njegovo kombiniranje `O(L²)` velja in zato velja tudi izpeljava celotne časovne zahtevnosti s krovnim izrekom.

    Prostorska zahtevnost navadnega strassenovega množenja je dominirana z ustvarjanjem novih matrik (dodatek rekurzije je minimalen) med samim postopkom. Ker naredimo največ konstantno število novih (pod)matrik (konstanta sicer ni majhna) med seštevanjem in vmesnim množenjem je torej omejeno z `O(L²)`, ob predpostavki, da se med ustvarjenjem novih podmatrik skopira zgolj smiselni del nadmatrike.

3. Strassenovo množenje z manjšo porabo spomina

    Za analizo razreda `CheapMatrix` se bomo posvetili bolj prostorski zahtevnosti, saj je izpeljava časovne zahtevnosti podobna kot pri razredu `FastMatrix`. Enako kot pri `FastMatrix` opravimo `7` klicev rekurzije, ki razpolovi naš problem, poleg tega pa še `O(L²)` dodatnega časa za urejanje in pripravo. Tako z enakim argumentom uporabimo krovni izrek.

    Implementirana je standardna oblika Strassenovega algoritma, le da namesto navadnega množenja na željeni rezultatni matriki kličemo metodo `_multiply` in ji kot primerno delovno matriko podamo referneco na ustrezno podmatriko delovne matrike `D`, prav tako ne opravljamo nobenih direktnih seštevanj ali odštevanj, ampak samo doprištevamo k neki matriki. To prispeva k nekoliko več prištevanjem med samim algoritmom (najprej prištejemo, da množimo pravi matriki, nato odštejemo, da *pospravimo za sabo*).
    
    Vse matrike najprej poindeksiramo s primernimi bločnimi matrikami (operacija je konstantna v času, prav tako pa ne porabi dodatnega spomina (`self._data` je zgolj referenca na `_data` nadmatrike)), je pa zato skozi kodo veliko bolj očitno, katere operacije uporabljamo, pa tudi koda je bolj samo-dokumentativna. Nato primerno z zmnožki napolnimo`C` in `D`, kar nam zaradi množenja na sami matriki in uporabi delovne matrike ne doda porabe prostora.
    
    V delu kode, ki poskrbi za ne-sode matrike je zadeva povsem enaka, le da zato, ker določenim podmatrikam prištevamo (recimo `C13`), jih moramo najprej počistiti (to v `O(L²)` naredimo kar tako, da jih pomnožimo s skalarjem `0` ). Nekoliko smo *šlampasti* le v primeru, ko sta obe dimenziji matrike lihi, saj takrat konstruiramo novo matriko, da jo lahko z uporabo metode `multiply` pomnožimo direktno na željeni matriki, kar pa porabi zgolj `O(1)` dodatnega prostora. Tako posamezni klic brez upoštevanja rekurzivnih klicev porabi konstantno dodatnega prostora.
    
    Natančnejši argument, da je prostorska zahtevnost `O(log(MNK)) = O(log(L)) = O(3log(L)) = O(L)`, si pogledamo malo drugače. Posamezni klic metode `multiply` ob ignoriranju cene rekurzije porabi zgolj konstantno dodatnega prostora, zanima nas, kakšna pa je cena za vzdrževanje sklada. Sklad se gradi rekurzivno, a v nobenem primeru ni večji kot `O(log(L))`, saj se polni le do največje globine rekurzije, potem pa se ob končanju rekurzivnega klica *zniža* za en nivo. Z razliko od časovne zahtevnosti, pri prostorski lahko ponovno uporabimo že porabljen spomin. 
    
    Časovna zahtevnost je tako enaka kot pri standardnem Strassenovem algoritmu (`O(n^(log₂7))`), prostorska pa je mnogo manjšana, saj porabi zgolj prostor za vzdrževanja sklada pri rekurziji.
    
### Primerjava dejanskih časov izvajanja

#### Direktna primerjava časov

| Algoritem    |   16   |   32   |   64   |   128   |   256   |    512   |
|:------------:|:------:|:------:|:------:|:-------:|:-------:|:--------:|
| SlowMatrix   | 0.01 s | 0.11 s | 1.00 s |  8.95 s |  94.6 s | 1025.6 s |
| FastMatrix   | 0.22 s | 1.45 s | 10.2 s |  70.3 s | 496.1 s | 3471.6 s |
| CheapMatrix  | 0.16 s | 1.17 s | 7.86 s |  53.6 s | 374.1 s | 2654.6 s |

#### Primerjava dvojiškega logaritma razmerja zaporednih časov

Z logaritiranjem razmerja zaporednih časov in dejstva, da velikosti matrik, na katerih testiramo algoritem naraščajo s faktorjem 2 lahko hitro pridemo do eksponenta pri časovni zahtevnosti.

| Algoritem    |  16  |  32  |  64  | 128  | 256  |  
|:------------:|:----:|:----:|:----:|:----:|:----:|  
| SlowMatrix   | 3.46 | 3.18 | 3.16 | 3.40 | 3.44 |
| FastMatrix   | 2.72 | 2.81 | 2.78 | 2.82 | 2.81 |
| CheapMatrix  | 2.87 | 2.75 | 2.77 | 2.80 | 2.83 |  

#### Komentar na rezultate

Naivni algoritem za množenje matrik se obnaša dokaj pričakovano, saj narašča *približno* s pravilnim eksponentom (eksponen je nekoliko večji), prav tako pa zaradi dokaj majhne natančnosti lahko pride do večjih napak pri izračunu, a vseeno sledi pravilnem trendu.

Obe implementaciji Strassenovega algoritma imata veliko bolj konstanten eksponent, ki je zelo blizu pravilnemu (2.8). Pomembno je omeniti predvsem nepričakovano dejstvo, da je `CheapMatrix` opazno hitrejši od `FastMatrix`. Natančnejša analiza ppkaže, da je eden izmed poglavitnih vzrokov za to predvsem priprava podmatrik, ki se uporabljajo v metodi multiply, ki opravi sicer dodatne klice `__init__` in s tem porabi dodaten čas, a se mi zdi, da je za samo implementacijo in lažje branje kode bolje, da kljub *overheadu* teh dodatnih klicev uporabljamo dodatne matrike, saj asimptotska hitrost ostane enaka, algoritem pa je bolj razumljiv. 
