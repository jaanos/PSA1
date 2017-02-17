# Poročilo

Jure Markun

********************************************
*Napišite tudi poročilo, v katerega vključite sledeče:

Kratek opis vaših algoritmov.
Natančna analiza časovne in prostorske zahtevnosti vaših algoritmov v odvisnosti od dimenzij vhodnih matrik.
Primerjava dejanskih časov izvajanja vaših algoritmov pri vhodih različnih velikosti.
Poročilo imate lahko kar v datoteki README.md v mapi z vašimi programi (v obliki Markdown), lahko pa naredite tudi poročilo v LaTeXu (na repozitorij naložite datoteko .tex - datoteke .pdf so izključene v .gitignore in jih torej ne nalagajte).
*******************************************

1.SlowMatrix

Prva vrsta množenja matrik, ki ga poznamo, je naivno množenje. To je običajno množenje matrik, kjer vrstice leve matrike množimo z stolpci desne in produkte seštevamo. Za implementacijo tega algoritma je poleg preverjanja ustreznosti dimenzij matrik potrebna le for zanka, ki gre skozi koeficiente obeh prvotnih matrik in zmnožke zapiše v ciljno matriko.

*Prostorska zahtevnost* 
Prostor, ki ga algoritem porabi je enak O(nm + ml + nl) =< O(3max(nm,ml,nl)) =< O(3max(n^2,m^2,l^2)), ker porabi zgolj prostor za vhodne matrike ter O(1) za konstante, ki so dimenzije teh matrik. 

*Časovna zahtevnost*
Časovna zahtevnost algoritma je enaka O(mln). Mest v ciljni matriki je nxl, za vsako mesto pa algoritem izvede m množenj (seštevanja nimajo velikega vpliva). Za majhne matrike je to sprejemljivo, za večje pa je algoritem počasen in neučinkovit.

Kot osnoven primer vzemimo, matriko oblike (n,m,l) = (51,23,45). V tem primeru algoritem izvede kar 52785 množenj.

2.FastMatrix

To matriko sem vzel kot vmesno stopnjo po hitrosti od SlowMatrix in FastMatrix. Algoritem najprej izračuna velikosti matrik n,m,l. Potem pa izračuna koeficiente n2,m2,l2, ki povejo, kaj je največje število, ki je potenca števila 2, hkrati pa je manjše od posamezne velikosti. Naprimer, v primerih n=11,m=5,l=4, so koeficienti enaki n2=8,m2=4,l2=4. 

Te koeficiente potem uporabimo, da izberemo dimenzije največjega bloka (podmatrike sode velikosti), ki ga razdelimo na štiri enake dele.
Najprej si pogledamo primer, ko je eden od koeficientov m2,n2,l2 enak 1: v tem primeru na matrikah uporabimo kar počasno množenje, saj Strassnovega algoritma na taki matriki ne moremo uporabiti. Če pa je matrika večja, pa podmatriko razdelimo na 4 bloke, ki so velikosti n2/2,m2/2,l2/2. Potem definiramo nove matrike, ki jih imenujemo M1,M2,...,M7.Te matrike so sestavljene iz seštevanja posameznih blokov in enim množenjem med temi vsotami v vsakem Mi (za i=1,....,7). Z ta množenja prav tako rekurzivno uporabimo Fastmatrix na določenih blokih. Potem definiramo C11,C12,C21 in C22 kot vsote in razlike M-jev, in jih vstavimo v ciljno matriko, kot po osnovnem Strassnovem algoritmu.

Kjer pa se pojavi problem, pa je, da s tem, ko smo vzeli bloke, nismo zmnožili cele matrike. Ne samo, da moramo dodati še robne dele, dodati moramo tudi produkt bločnih delov z robnimi. Če že bloki vedno zasedajo več kot 1/2 celih matrik, se izkaže, da v najslabšem primeru (npr, da so vrstice, stolpci velikosti 2^n-1)  potem večino množenja matrik še zmerom poteka z SlowMatrix. Algoritem je za velike matrik hitrejši, kot metoda SlowMatrix, ni pa optimalen. 

*Prostorska zahtevnost*

Osnovni prostor, ki ga potrebujemo, je O(nm + ml + nl) za shrambo matrik, poleg tega pa še O(8x(n2xm2 + m2xl2)) za shrambo blokov (ker so lahko največ te velikosti), O(7xn2xl2) za matrike Mi, O(4(n2xl2)) za matrike C. Vse to lahko le na približno združimo in upoštevamo, je n2<=n, m2<=m in l2<=l, tako da dobimo maksimalni zadeseden prostor O(5x(nm+ml)+(15/2)nl)

*Časovna zahtevnost*

Za časovno zahtevnost moramo v tem primeru izračunati, koliko potrebuje za izračun del, ki računa po Strassnovem algoritmu, in pa tisti, ki računa po standerdnem množenju.

Strassnov algoritem v ciljni matriki zaobjema n2xl2, za računanje z bloki pa je bilo potrebno 7 T(n2/2) množenje. pri tem upoštevamo tudi rekurzivno množenje blokov. Zahtevnost za Strassna izračunamo kar po Krovnem izreku:
T(n,m,l) =< O(max(n2,l2)) + 7T(max(n2,l2)/2) = O((max(n2,l2))^log2(7))
Brez uporabe maksimuma bi to precej težko izračunali, tako pa dobimo zgornjo vrednost časovne zahtevnosti.

Izračunajmo še zahtevnost računanja preostalih vrednosti z SlowMatrix. Zahtevnost računanja cele matrike na ta način bi bila O(n^3), ker pa tako izračunamo le nekatere vrednosti, je zahtevnost enaka kar O(max(n2,l2,m2)^3), ker s počasnim množenjem računamo manj kot polovico matrike. Tu je morda vrednost precej večja, kot bi bila v resnici, vendar bi bilo spet točno vrednost težko izračunati in bi bila odvisna od posameznih stolpcev/vrstic. 

Torej, skupna zahtevnost operacij je največ O((max(n2,l2))^log2(7) + (max(n2,l2,m2)^3).
To bi v že omenjenem primeru (n,m,l) = (51,23,45) pomenilo 24029.

3.FastMatrix2

Ta verzija FastMatrix je zgolj optimizirana verzija prejšnje. Edina razlika je, da za vrednosti n2,m2,l2, ki so velikosti blokov, ne vzamemo potence števila 2, pač pa največje sode podmatrike. Torej so te vrednosti bodisi n,m,l, ali pa n-1,m-1 ali l-1. To izjemno poveča količino mest v ciljni matriki, ki jih izračunamo z Strassnovim algoritmom. Opisal bom zgolj razlike v primerjavi s prejšnjim fast algoritmom.

*Prostorska zahtevnost* 

Prostorska zahtevnost je v tem primeru večja, ker so bloki toliko večji, zavzamejo več prostora, je pa zgornji približek tak kot prejšnji, torej O(5x(nm+ml)+(15/2)nl).

*Časovna zahtevnost* 

V tem primeru po Strassnovem algoritmu izračunamo vse, razen mogoče zadnje vrstice in stolpca. Če pa teh ni, pa imamo v celoti Strassnov algoritem, torej dobimo v tem primeru, ko je največ računanja zahtevnost O(max(n2,l2,m2)^(log2(7))
Mest, ki štejejo pod zadnjo vrstico ali stolpec je največ n+2m+l. na teh mestih pa za izračun potrebujemo m množenj, torej je zahtevnost tam O(mx(n+2m+l)). 

Skupaj O(max(n2,l2,m2)^(log2(7))) + mx(n+2m+l))
Za primer  (n,m,l) = (51,23,45) je to 11804, kar je bistvena izboljšava v primerjavi z FastMatrix.4

4.CheapMatrix

Pri Cheap Matrix moramo upoštevati še zahtevo, da algoritem porabi le O(log(lmn)) dodatnega spomina, kar pomeni, da imamo poleg prostora za vhodne matrike prostor samo še za eno "work" matriko velikosti nxl, torej takšne, kot ciljna matrika.

Ideja metode je, da Mi dobimo s tem, da rekurzivno kličemo množenje podmatrik vsot A in B, za ciljno matriko damo eno izmed delov v delovni matriki, drugo pa vzamemo kot novo delovno matriko. To ponavljamo, ter dobimo bločni del, potem pa zunanji del še dopolnemo z števili s počasnega množenja.

*Prostorska zahtevnost*

Prostorska zahtevnost algoritma je O(nm + ml + nl + log(lmn))

*Časovna zahtevnost*

Časovna zahtevnost je večja, kot pri FastMatrix, ker je metoda narejena zgolj za to, da prihrani prostor, pri tem pa izgubi na hitrosti.

5.Meritve

Če poskusimo izmeriti dejanski čas izvajanja algoritma pri množenju matrik velikosti (n,m,l) = (5,11,7), dobimo naslednje

Slow

0.002000093460083008 

Fast2

0.007000446319580078

Cheap

0.013000726699829102 

to je v splošnem presenetljivo, saj je Fast matrika narejena, da bi bila hitrejša od Slow. to bi lahko pojasnili s tem, da pri manjših algoritmih SlowMatrix vseeno deluje hitreje, saj mora FastMatrix izvajati dokaj veliko operacij, pri veliko večjih matrikah pa bi bil čas hitrejši. CheapMatrix je pričakovano počasnejša od obeh.
