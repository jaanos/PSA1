#Poročilo

##Opis algoritma
Algoritem problem rešuje tako da v vsakem vozlišču poišče maksimalno neodvisno množico naslednjika,
glede na izbrano neodvisno množico v vozlišču. Rezultate shranjuje v slovarje. Da poišče maksimalno
neodvisno množico naslednjika, mora ta imeti slovar že ustvarjen. Tako se algoritem sprehodi do korenov
brez naslednjikov, kjer je maksimalna neodvisna množica v odvisnosti od izbrane neodvisne množice ravno
vsota uteži izbrane neodvisne množice, ker rezultate shranjujemo v slovar, moramo za vsako vozlišče
računati le enkrat. Bolj podroben opis, po korakih, je zapisan v komentarjih kode.


##Analiza časovne in prostorske zahtevnosti
Algoritem najprej ustvari slovar kjer so ključi neodvisne množice cikla C_k, vrednosti pa so seznami neodvisnih
množic iz cikla C_k, ki ne vsebujejo elementov iz ključa. Časovna zahtevnost za ustvarjenje seznama je
O( (1+sqrt(5))/2)^(3k) * k ). V slovarju je Fib(k) ključev , za vsak ključ pa je max Fib(k) vrednosti.
Prav tako ustvari slovar v katerega shranjuje maksimalne neodvisne množice vsakega vozlišča v odvisnosti od naslednika.
Po koncu algoritma ima slovar n ključev v vsakem ključu pa Fib(k) vrednosti.

Nato gre računati v vsako vozlišče. Za izračun maksimalne neodvisne množice v korenih brez naslednjikov imamo časovno 
zahtevnost O( (1+sqrt(5))/2)^k * k ), v vsakem korenu ustvari slovar s Fib(k) ključi vsak ključ pa ima le eno 
vrednost. Enako storimo v primeru vozlišča, ki ima naslednjike, le da tokrat za vsakega naslednjika izračunamo
maksimalno neodvisno množico v odvisnosti od izbrane neodvisne množice vozlišča. Nato sestejemo vrednosti vseh
naslednjikov in ceno izbrane maksimalne neodvisne množice v vozlišču, časovna zahtevnost izračuna cene izbrane
maksimalne neodvisne množice v vozlišču, je O( (1+sqrt(5))/2)^(3k) * k ) enaka je časovna zahtevnost za iskanje
maksimalne neodvisne množice v odvisnosti od naslednjika. Ker se časovne zahtevnosti seštevajo , računamo pa 
vseskupaj n-krat (po vseh korakih algoritma) je tukaj skupna časovna zahtevnost O( (1+sqrt(5))/2)^(3k) * k * n + n). 
Element '+ n' pride iz računanja maksimumuma največ n elementov, kar nam da zahtevnost O(n), skupno torej 
O( (1+sqrt(5))/2)^(3k) * k * n + n).

Časovna zahtevnost algoritma je torej O( (1+sqrt(5))/2)^(3k) * k * n + n) + O( (1+sqrt(5))/2)^(3k) * k ) =
O( (1+sqrt(5))/2)^(3k) * k * n)

Nekoliko bolj podrobna razlaga korakov in časovne zahtevnosti se nahaja znotraj komentarjev kode.


##Primerjava dejanskih časov izvajanja

Dimenzija drevesa|Dimenzija cikla|Porabljeni čas

20------------------|5----------------|0.00176291729648778

20------------------|6----------------|0.0031676656531346766

20------------------|7----------------|0.0066976893565177335

20------------------|8----------------|0.015011328052726938

20------------------|9----------------|0.0308074161217914

20------------------|10---------------|0.06960556034588089

20------------------|11---------------|0.15809074311327703

20------------------|12---------------|0.36443445264036134

20------------------|13---------------|0.842614772897852

20------------------|14---------------|2.009583637334748

20------------------|15---------------|4.907300572162663

20------------------|16---------------|12.148603804410437

20------------------|17---------------|30.53033788666362

20------------------|18---------------|87.61188345894845

20------------------|19---------------|228.79282545024208

Kot pričakovano časovna zahtevnost narašča eksponentno v odvisnosti dimenzije C_k.

Dimenzija drevesa|Dimenzija cikla|Porabljeni cas

10------------------|14---------------|1.2240831957326928

35------------------|14---------------|3.4122922463057286

60------------------|14---------------|5.600585777271982

85------------------|14---------------|7.908996463692629

110-----------------|14---------------|10.042754409911435

135-----------------|14---------------|12.44797159783144

160-----------------|14---------------|14.751280296868295

185-----------------|14---------------|16.863949214018163

210-----------------|14---------------|19.17026290158732

Kot pričakovano časovna zahtevnost narašča linearno v odvisnosti od n.
