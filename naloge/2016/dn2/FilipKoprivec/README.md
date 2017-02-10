# Poročilo

*Filip Koprivec, 27141059*

## Kratek opis algoritmov

Sama ideja delovanja programa in opisi se večinoma nahajajo že kot komentarji v sami kodi programa, v poročilu si 
bomo pogledali predvsem pot do rešitve in kakšno implementacijsko podrobnost. Prvih nekaj vrstic, ki so namenjene
zgolj temu, da se pripričamo, da so vhodni podatki smiselni bomo pri analizi izpustili, prav tako jih bomo zaradi 
nepotrebne porabe časa odstranili v končni verziji.

Osnovna ideja samega algoritma je najbolje povzeta ob razlagi tebele DP. Z `T(i, m)` tako označimo maksimalno težo 
neodvisne podmnožice(v podgrafu), za katero velja, da se podgraf začne z vozliščem `i` v drevesu (celoten graf je tako 
produkt tega poddrevesa in celotnega cikla), ob pogoju, da smo za ustrezna vozlišča (prižgana, vozlišča, katerih težo 
gledamo) vzeli vozlišča ki ustrezajo bitni maski `m`.

##### Komentar na uporabo bitne maske:
Za lažje shranjevanje uporabljenih vozlišč uporabljamo bitno masko, ki pa jo v programskem jeziku predstavimo kar z 
celoštevilskim tipom (zaradi porabe časa in prostora), za lažjo uporabo in preprečavanje napak, pa jo s pomočjo orodja 
mypy "zapakiramo" v tip `BitMask`, kar je časovno še vedno hitro (ob zagonu programa je maska  tipa `int`, le 
ob inicializaciji nove maske se pokliče navidezni konstruktor, ki zgolj vrne svoj argument, torej za ceno klica 
funkcije(zgolj dve dodatni operaciji: `LOAD_GLOBAL` in `CALL_FUNCTION`) pridobimo nekaj varnosti).

Sama bitno masko razumemo kot seznam prižganih ali ugasnjenih bitov, kjer bit na `i` tem indeksu (gledano z desne) 
predstavlja, da smo v ciklu vzeli vozlišče na indeksu `i` (vsako vozlišče metadrevesa si lahko predstavljamo kot cikel).
Tako lahko hitro zgolj s pomočjo operacij na bitih pridemo do prižganih bitov, prav tako lahko hitro preverimo, ali sta 
dve maski med seboj kompatibilni (če smo masko `a` uporabili na očetu, ali lahko masko `b` uporabimo na sinu).

Za pomoč z delom z bitnimi maskami si v datoteki helpers.py definiramo nekaj pomožnih funkcij, ki pa bodo razložene 
kasneje.


#### Priprava podatkov

Ker nimamo o drevesu nobenih dodatnih podatkov si za začetek pripravimo primerno predstavitve drevesa kot grafa, 
ki jih bomo potrebovali v nadaljevanju. Bolj natančno si za pripravimo seznam, ki za posamezno vozlišče vsebuje 
njegovega očeta (parent, tu smo nekoliko nepazljivi in korenu drevesa za njegovega starša nastavimo kar sebe, a 
tega v resnici nikoli ne potrebujemo, tako da si to lahko privoščimo), v drugem seznamu (children) pa si za posamezno 
vozlišče shranimo njegove otroke (children). Poleg tega si za lažje postopanje pri dinamičnem programiranju pripravimo 
še seznam `levels`, ki na `i` tem mestu hrani seznam vozlišč, za katera velja, da se nahajajo v `i` tem nivoju drevesa.

Funkcija, ki to naredi je preprosta. Z nekoliko prirejenim algoritmom za iskanje v globino iz vaj iterativno prehodimo 
celoto drevo in za posamezno vozlišče sharnimo njegovega starša (in to vozlišče staršu dodamo kot otroka), hkrati pa 
tudi vozlišča dodajamo v primerne nivoje v seznam `levels`, tudi tu smo nepazljivi glede starša korena drevesa, a to ne 
povzroča težav.

Sledi kratek komentar o časovni in prostorski zahtevnosti generiranju bitnih mask, nato pa si pripravimo tabelo vseh 
bitnih mask (torej tabelo vseh veljavnih mask), za to poskrbi funkcija `generate_bitmask`, ki s preporostim algoritmo 
zgenerira vse bitmaske, za katere velja, da če začetek in konec zlepimo skupaj, si poljubna prižgana bita nista 
sosednja (med njima je vsaj en ugasnjen bit), kar ustreza izboru neodvisnih vozlišč v cilku. Poseben primer je bitna 
maska dolžine 1, ki vsebuje tako `0` kot `1`. Maske generiramo iterativno, kjer vsem veljavnim maskam dolžine `n-2` 
prižgemo `n`-ti bit, ali pa jih pustimo take kot so (in s tem efektivno dodamo `0`, ker za osnovo uporabljamo tip 
`int` so vsi biti že vnaprej nastavljeni na `0`), maske dolžine `n-1`, ki pa se končajo z `1` hranimo v seznamu 
`waiting` in jih dodamo za `n` to iteracijo (ali ob koncu, ko moramo preveriti še ciklično ustreznost).

Zgeneriramo tudi slovar seznamov, ki za poljubno masko vsebuje vse maske, ki so z njo kompatibilne, to preprosto 
preverimo z bitno logično operacijo `in (AND, &)` in dve maski štejemo za kompatibilni, če je rezultat operacije `0`, 
torej če nimata skupnih prižganih bitov, kar pomeni, da je monžica, ki jo pokrijeta na očetu in sinu neodvisna. 
Funkcija `make_transitions` se preprosto zapelje čez vse maske in jih doda v seznam če so kompatibilne.

Za konec si pripravimo še ogrodje za tabelo, kjer si bomo shranjevali že izračunane podatke (DP), ki za poljuben indeks 
vozlišča vsebuje slovar, katerega ključi (bitne maske) imajo za vrednost par najtežje podmnožice ki ustreza maski in 
indeksu in seznam mask, ki smo jih za to morali uporabiti na otrocih tega vozlišča. (Vrstni red v seznamu je pomemben, 
saj sovpada z vrstnim redom v seznamu children).

Za lažji izračun teže bitne maske uporabljene na določenem vozlišču definiramo pomožno funkcija `calculate_weight`, ki 
za bitno in indeks `j` izračuna težo uporabe (preprosto sešteje vse teže `w[i][j]`, če je `i` ti bit prižgan).

#### Izračun najtežje množice

Za izračun se poslužimo iterativnega dinamičnega programiranja. Vsako vrednost izračunamo kot vsoto najboljših 
vrednosti njegovih otrok, kjer je najboljša vrednost otroka definirana kot maksimum vseh tež, ki jih lahko dosežemo s 
kompatibilnimi maskami. 
`DP[i][mask] = sum(max(DP[j][comp_mask] for com_mask in compatible[mask]) for j in direct_children(i)) + 
calculate_weight(mask, i)`, končne vrednosti pa smiselno dosežemo pri vozliščih brez otrok, kjer velja 
`DP[i][mask] = calculate_weight(mask, i)` (če bi definirali `max([]) = 0`, bi lahko robne primere kar vključili v prvo 
formulo, za programiranje pa se izkaže, da je bolje, da jih eksplicitno izvzamemo).

Za "bottom up" pristop k temu dinamičnemu problemu je topološka ureditev podproblemov precej očitna, vozlišče je odvisno 
zgolj od vozlišč, ki so nižje od njega(glede na nivoje drevesa), zato začnemo tabelo polniti na dnu drevesa (to je tudi 
razlog za pripravo tabele `levels`). Zgolj zaradi praktičnosti korak za povsem spodnji novo naredimo posebej.

Glavna for zanka povsem sledi formuli za podprobleme: Po vrsti se sprehajamo od spodaj navzgor po nivojih in za 
poljubno vozlišče iz nivoja `level_i` za vsako masko, ki jo na njem lahko uporabimo preverimo, kakšna so najtežja 
ustrezna poddrevesa, za poznejši izpis te množice, pa si kot je bilo prej omenjeno še shranimo, s kakšnimi maskami 
otrok smo do te možnosti prišli.

#### Rekonstrukcija in končni izračun najdražje poti

Ko imamo tabelo izpolnjeno je naš rezultat največja vrednost, ki jo lahko ob poljubni maski dosežemo v korenu drevesa 
(in množica, ki jo ta izbira generira), da pridemo do tega moramo preveriti vse vrednosti maske (to bi sicer kot posebni 
primer lahko naredili že kar v v glavni for zanki, a bi povsem po nepotrebnem zapletli kodo, pa tudi veliko močneje povezali 
delovanje delov programa, tako pa imamo lahko na drugi strani veliko bolj modularen program, čeprav opravimo malo 
dodatnega nepotrebnega dela).

Ko imamo vrednost in bitno masko za najboljši rezultat zgolj rekonstruiramo množico s pomočjo zapomenjnih vrednosti v 
drugem polju DP (poleg teže hranimo tudi maske, ki so bile uporabljene na otrocih). To storimo z iskanjem v širino 
(lahko bi naredili tudi iskanje v globino), po grafu, ki ga generira optimalna pot po DP (Za poljubnega otroka `rtr` 
razširimo s seznamom, ki ga kot produkt s ciklom generira ta otrok, ter to ponovimo za vse njegove otroke ob ustreznih 
bitnih maskah). Za pomoč, kakšno množico dobimo ob produktu `i`-tega vozlišča s cilom, na katerem imamo bitno masko 
`b` si definiramo funkcijo, ki preprosto vrne seznam parov `(i, j)`, kjer je par `(i, k)` vključen natanko tedaj, ko je 
`k`-ti bit v bitni maski prižgan.

Na koncu vrnemo par maksimalne teže, ki jo lahko pri poljubni maski dosežemo s korenom, in podmnožico produkta cikla in 
drevesa, ki tej teži ustreza. Pomembno je še omeniti, da je lahko takih množic več, program pa za enake vhodne podatke 
vselej vrne enako množico, prav s tem namenom nikoli ne iteriramo po ključih slovarja, ampak vedno uporabljamo seznam 
generiranih bitnih mask, katerega vrstni red je vedno enak (za enake vhodne podatke).


## Analiza časovne zahtevnosti

### Za lažjo analizo bomo predpostavili naslednje:

+ Naj bo `k` dolžina cikla in naj bo `n` velikost drevesa (število vozliščv drevesu), prav tako lahko tudi število 
povezav v drevesu določimo z `n`, saj `E = n - 1`, torej `O(n) = O(E) = O(E + n)`.
+ Naj `sq(x)` označuje kvadratni koren števila `x`
+ Naj `sq2` označuje `sq(2)`, `sq21` označuje `sq2 + 1` in `phi` označuje zlati rez (`phi = (sq(5) + 1)/2`)
+ Zgornjim številom ustrezaj opribližne vrednosti: `sq2 =~ 1.414`, `sq21 =~ 2.414`, `phi =~ 1.618`
+ Naj `F(n)` označuje `n` to Fibnoaccijevo število, kjer `F(0) = 0, F(1) = 1`
+ Naj `^` označuje standardno operacijo potenciranja, `|` in `&` pa bitni `ali` in `in`. 
+ Dostop do elementov v seznamu (z indeksiranjem) je neodvisen od dolžine seznama
+ Dostop do elementov v slovarju (z ključi) je (praktično) neodvisen od dolžine slovarja (dostopamo v konstantnem času).
+ Delov programa, ki so namenjeni raznim zagotovilom, ki bi morala držati (smiselnost vhodnih podatkov, pravilna vsota ...) 
ne bomo analizirali, saj se jih lahko po želji odstrani in ne spremenijo delovanja programa, ampak so namenjeni bolj 
programerju samemu za neke vrste samokontrolo, sem spadajo torej vse uporabe besede `assert`.
+ Označimo z `B` število dovoljenih bitnih mask
+ Označimo s `T` vsoto vseh kompatibilnih mask (`sum(len(l) for l in transitions.values())`)
+ Predpostavimo, da so vse računske operacije na celih števili neodvisne od `n` in `k`.
+ Nadalje predpostavimo (ta predpostavka velja zgolj na omejenem območju k), da so vse bitne operacije ma bitnih maskah 
konstantne (torej neodvisne od `n` in predvsem `k`), povsem formalno je sicer bitna maska dolga `k` bitov, kar sicer za 
velike `k` ni konstantno (pravzaprav), saj je najbrž velikostnega reda `O(k/w)`, kjer je `w` širina procesorske besede 
v bitih, kar pa je na večini trenutnih računalnikov vsaj `32` vedno bolj pogosto pa `64`. Za povsem natančno analizo 
bi se bilo potrebno bolj poglobiti v standard jezika, a osnova standarda za jezik python ne predpostavlja kakšne 
posebne omejitve, saj so cela števila na splošno implementirana kot poljubno velika 
([https://docs.python.org/3/c-api/long.html](https://docs.python.org/3/c-api/long.html)), celo več, tudi za bitne 
operacije uporablja neskončna števila ([https://wiki.python.org/moin/BitwiseOperators](https://wiki.python.org/moin/BitwiseOperators)), a jih najbrž razkosa na 
velikost besed za samo uporabo.


### Analiza

#### Analiza delov povezanih z bitnimi maskami

Najprej si poglejmo, kako lahko omejimo število bitnih mask, prvo grobo oceno nam poda kar struktura v kateri jo 
shranjujemo, torej `int`, iz česar dobimo: `B <= 2^k`, vendar pa se da maske omejiti še bolj natančno. Če si pogledamo 
način generacije bitnih mask lepo vidimo reukurzivnost. Za začetek se pri analizi omejimo zgolj na maske, kjer ne 
zahtevamo cikličnosti (dovoljujemo torej vse maske, kjer nobena zaporedna bit nista prižgana, lahko pa sta hkrati 
prižgana prvi in zadnji bit). 

Označimo torej z `A(n)` število ustreznih bitnih mask dolžine natanko `n`, očitno velja 
`B(n) < A(n)`, če je le `n > 1`. Nadalje označimo z `A(n, 0)` in `A(n, 1)` število mask dolžine `n`, ki se končajo s 
prižganim ali ugasnjenim bitom. Očitno velja `A(n) = A(n, 0) + A(n, 1)` in `A(1) = 2`. Hitro pridemo do rekurzivne 
formule `A(n+1, 0) = A(n,0) + A(n,1) = A(n)`, če pa hočemo masko končati z prižganim bitom, potem lahko uporabimo zgolj 
maske, ki so za ena krajše in se končajo z neprižganim bitom: `A(n+1, 1) = A(n, 0) = A(n-1)`, če formuli združimo 
dobimo: `A(n+1) = A(n+1, 0) + A(n+1, 1) = A(n) + A(n-1)`, v čemer zlahka prepoznamo zamaknjeno Fibonaccijevo zaporedje, 
za katerega velja `A(1) = 2` in `A(2) = 3` in torej `A(n) = F(n+2)`

Ker vemo, da `B(n) < A(n)` (saj v `A` dovoljujemo nekatere maske, ki jih v `B` ne), lahko z uporabo znanih dejstev o 
rasti fibbonaccijevih števil torej lahko omejimo `B` z `O(phi^k)`, kar je gleda na `O(2^k)` znatna izboljšava.

<!-- TODO: If time permits, prove that correct masks also grow with same pace -->

Druga pomembna stvar, ki jo je glede bitnih mask potrebno analizirati je število vseh tranzicij med njimi. Natančneje, 
zanima nas, kako v odvisnosti od `k` raste število kompatibilnih mask (Če moramo za vsako masko posebej, in za vsako 
tej maski kompatibilno masko opraviti konstantno dela, kako lahko to izrazimo kot funkcijo k).

Ta analiza nas zanima, da lahko omejimo tako časovno kot prostorsko zahtevnost funkcije make_transitions. Časovna 
zahtevnost je očitno `O(B^2)`, saj moramo za vsako masko izločiti njej nekompatibilne (za `B` mask `B` preverjanj.). 
Ravno tu uporabimo predpostavko o konstantnih bitnih operacijah, saj bi v nasprotnem primeru bila časovna zahtevnost 
posameznega preverjanja `O(B)`, kar bi skupno časovno zahtevnost spremenilo na `O(B^3)`, v realnosti pa so primerjave ali 
sta dve bitni maski kompatibilni konstantne in je torej časovna zahtevnost metode res `O(B^2)`

Poleg časovne zahtevnosti pa nas zanima tudi prostorska zahtevnost te metode. Da jo lažje anlizirajmo moramo pogledati, 
iz česa je sestavljen vrnjeni senzam. Za vsako masko vsebuje vse maske, ki so z njo kompatibilne. Za par mask tako 
preveri, če skupaj tvorita neodvisno množico v nekem podgrafu. Pomemben pa je ta podgraf, saj je pravzaprav produkt 
polnega grafa velikost `2` in cikla dolžine `k`. Če si ključ predstavljamo kot del množice, ki v produktu leži na 
"zgornjem delu", vse možne vrednosti pa kot "spodnji" del neodvisne množice tako dolžina seznama ustreza vsem 
neodvisnim množicam v produktu `K_2 * C_k`, za kar pa lahko s pomočjo OEIS 
([http://oeis.org/A051927]( http://oeis.org/A051927)) s formulo zapišemo število neodvisnih množic 
kot `Y(k) = (1 + sq2)^k + (-1)^k + (1 - sq2)^k` in preprosto omejimo z prostorsko zahtevnostjo: 
`O((sq2 + 1)^k) = O(sq21^k) = O(T)`

##### Analiza pomožnih metod za delo z bitnimi maskami

+ `are_compatible`: O tem je bilo povedano že dovolj. Kljub odvisnosti od `k` predpostavimo, da je operacija konstantna 
za vse smiselne vhodne podatke.
+ `generate_bitmasks_with_multiplication`: V `j` tem koraku opravimo `A(j-2)` korakov. Torej skupaj opravimo 
`A(0) + A(1) + ... + A(n-1)`, kar pa nas privede do vsote fibonaccijevih števil. Pomagamo si z 
[http://mathforum.org/library/drmath/view/52707.html](http://mathforum.org/library/drmath/view/52707.html), in časovno 
zahtevnost spet omejimo s pomočjo formule za rast, torej `O(phi^k)`, kjer je `k` dolžina cikla.
+ `generate_product_with_bitmask`: Funkcija za posamezen bit v maski prever, ali je prižgan in če je, v seznam doda 
ustrezen par. Časovna zahtevnost: `O(k)` (saj preverimo vsak bit posebej), prostorska zahtevnost: `O(k)`, dolžina 
vrnjenega seznama.
+ `make_transitions`: Kot je bilo ugotovljeno zgoraj, časovna zahtevnost: `O(B^2)`, prostorska zahtevnost: `O(T)`.


#### Analiza glavnega dela izračuna najtežje množice


Kot je bilo prej omenjeno se glede na topološko ureditev premikamo od dna dreves navzgor po nivojih, in v zanki za vse 
otrok eposameznega vozlišča preverimo željen maksimum vsote. Zato vsako vozlišče obiščemo največ dvakrat, kot starša, 
ali pa kot otroka nekaga starša (ker pa smo v drevesu torej največ enkrat). Pomembnejše je, da se na podoben način 
"sprehodimo" po bitnih maskak. Tako za vsako vozlišče ne preverimo vseh možnih kombinacij mask (`B^2`) ampak samo vse 
možne prehode (če na "staršu" nastavimo masko na otrocih pregledamo zgolj kompatibilne maske), torej skupaj `O(T)`.

Cena glavne zanke je tako `O(n*T)`, prostorska zahtevnost pa `O(n*B)`, saj izpolnjujemo celotno tabelo `DP`, v 
katero za vozlišče sharnimo vse možne rešitve. Na to lahko pogledamo drugače. Za vsako masko bomo shranili `n` 
vrednosti (vozlišča) in še `n` vrednosti kot maske, ki so bile uporabljene za dosego teh vrednosti na sinovih.

#### Analiza rekonstrukcije poti

Rekonstrukcija poti je preprosto iskanje v širino po optimalnem grafu v DP. Kot je bilo že prej omenjeno najprej 
pogledamo, pri kateri maski je koren drevesa dosegel največjo vrednost, kar je časovno `O(B)`, nato pa to masko dodamo 
v vrsto za izvajanje iskanja. Analiza iskanja je proprosta. Če bi se samo sprehodili po vseh rezultatih 
(in ne bi generirali grafa), bi bila časovna zahtevnost `O(n)`, saj bi morali obiskati vsako vozlišče. Tako pa moramo 
ob obisku posameznega vozlišča še zgenerirati seznam vozlišč, ki jih kot najtežjo množico vzamemo, kar porabi `O(k)` 
časa in `O(B)` prostora. Skupno torej porabimo `O(n*k)` časa in prostora, kar je smiselno, saj na koncu vrnemo celoten 
seznam vzetih vozlišč, katerega velikost je reda `O(n*k)`. Skupna časovna zahtevnost rekonstrukcije množice tako znaša
`O(B + n*k)`, prostorska pa `O(n*k)`.


#### Skupna zahtevnost

Skupna časovna zahtevnost je vsota časovnih zahtevnosti priprav, izračuna in rekonstrukcije:

`O(B^2 + n) + O(n*T) + O(n*k + B) = O(B^2 + n*T + n*k) = O(B^2 + n*T) = O(phi^(2*k) + n*sq21^k) =~ O(2.826^k + n*2.414^k)`

Iz izpeljane časovne zahtevnosti vidimo, da bo pri velikih `k` prevladal prvi člen, za primerno majhne pa je zaradi 
zelo majhne konstante(vse operacije so povsem osnovne, saj zgolj seštevemo, množimo in izvajamo medbitne operacije) 
bolj pomemben drugi člen (če ne bi dodatno omejevali `T` bi tako dobili samo člen `n*B^2`), ki prinaša večjo konstanto.


Skupna prostorska zahtevnost:

`O(T) + O(B*n) + O(n*k) = O(T + n*B) = O(sq21^k + n*phi^k) =~ O(2.414^k + n*1.618^k)` 



## Primerjava dejanskih časov izvajanja

TODO