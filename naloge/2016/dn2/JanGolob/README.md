*Jan Golob*
# Poročilo

Kot vhodni podatek dobimo utežen kartezičen produkt drevesa z n vozlišči in ciklja s k vozlišči. To je v programu podano z tabelo tež in tabelo sosedov drevesa.
Algoritem vrne tisto množico nepovezanih vozlišč, ki ima največjo "ceno" ter le-to ceno.

Algoritem poteka na podoben način kot algoritem "sahovnica" pri 11 sklopu vaj. Na vsakem vozlišču drevesa T izračunamo maximalno "težko" neodvisno množico vozlišč poddrevesa s korenom v tem vozlišču. In to za vsako možno neodvisen možno podmnožico cikla. Ko tako izračunamo maximalne vrednosti v korenu drevesa. Zdaj izmed teh izberemo maximalno, ki jo vrnemo skupaj z seznamom vozlišč, ki prispevajo k njej.

Poglejmo sedaj dele kode posebej. _Bolj podrobne komentarje pa se da najti v kodi._

## Vse možne neodvisne množice vozlišč cikla Ck:
Na vsakem vozlišči drevesa T se nahaja 1 cikelj dolžine k. Zanimajo nas vse možne neodvisne podmnožice vozlišč, in kakšni sta lahko te množici na sosednjih vozliščih drevesa, da bo njuna unija neodvisna množica. Po definiciji kartezičnega produkta grafov. Bo to takrat ko se podmnožici ne bosta sekali (ne bosta vsebovali vozlišč na istih mestih).
Torej če sta u, v sosednji vozlišči v T. U, V neodvisna podgrafa cikla dolžine k. Bo bo Unija kartezičnih produktov u * U in v * V neodvisna množica vozlišč natanko takrat ko bo presek U in V prazen.
Opazimo da je [število različnih neodvisnih podmnožic vozlišč cikla dolžine *k* ravno *Lk*](http://mathworld.wolfram.com/IndependentVertexSet.html) kjer je *Lk* k-to [Lucasovo število](https://en.wikipedia.org/wiki/Lucas_number).
Lukasova števila so podana z rekurzino formulo *L(n) = L(n-1) + L(n-2)* in začetnima številoma *L(0) = 2, L(1) = 1*

Tabela Lucasovih števil:

n| L(n)
--- | --- 
1|1
2|3
3|4
4|7
5|11

V kodi prvo naredim vse možne neodvisne podmnožice cikla Ck to naredim v funkciji "vsiNeodPodCik" Nato pa v funkciji "potencialni_rekurzivci" za vsakega od njih zabeležim katere so kompatilne podmnožice. To bom potreboval v dinamičnem programiranju.

Časovna zahtevnost za "vsiNeodPodCik" je *O(k^4)*. Časovna zahrevnost za označevanje pa *O(L(k)^2)* Seznam "legenda", ki ga vrnemo je velikosti *O(L(k))* seznam "sl_kompat" pa *O(L(k)^2)* (saj imamo pod vrednostmi pri ključu 0 cel seznam dolžine L(k))

V kodi ustvarim vse možne nodvisne podmnožice cikla vsakič znova. Ampak ker so odvisne le od dolžine cikla, bi lahko čas potreben za računanje možno zmanjšali z knjižnico ali memorizacijo. Memorizacija je implementirana, a pri posamičnih testih ni posebej uporabna.

## Dinamično programiranje na drevesu T:
Skozi drevo T se sprehodim z DFS algoritmom. Pri previsitu naredim seznam otrok vozlišča. Ta seznam je enak seznamu s katerim bi predstavili usmerjeno DFS drevo. Ker je T povezano *(definicija drevesa)* je enako drevesu DFS, le da je neusmerjeno (morda ima kje drugje koren, a nas to ne moti.)

Nato s postvisit funkcijo izvedemo dinamično programiranje. Zaradi narave postvisita, se bo to zgodilo pri izhodu iz vozlišča, zato bomo takrat že obiskali vse njegove potomce in lahko podobno kot pri vaji za vsako možno izbiro vozlišč cikla u * Ck pri danem vozlišču u.

Na vsakem vozlišču z funkcijo zapeljemo čez vse sosede danega vozlišča torej je njena časovna zahtevnost *O(max(T))*
Na vsakem vozlišču se z postvisit funkcijo zapeljemo čez celoten slovar sl_kompat torej je njena časovna zahtevnost *O(L(k)^2)*.

Po poznavanju DFS algoritma, ki smo ga vzeli na predavanjih in na vajah vemo da bo potem moj DFS algoritem porabil *O(E(T) + nO(max(T) + L(k)^2))*

Za Drevo potomcev bomo porabili še za en T prostora.
Pri dinamičnem programiranju pa bomo porabili *n * L(k)* prostora za tabelo "maxIndependSet". To bi se dalo izboljšati če bi gledali samo po nivojih drevesa T in bi si vedno zapomnili le do zadnjega celega nivoja.

## Skupna časovna in prostorska zahtevnost
Označevanje vseh neodvisnih podmnožic vozlišč cikla k porabi *O(k^4) + O(L(k)^2)* ali pa *O(1)*. Za DFS algoritem pa porabimo 
*O(E(T) + nO(max(T) + L(k)^2))* Vsota tega je:

_**O(k^4) + O(L(k)^2) + O(E(T) + nO(max(T) + L(k)^2))**_ = _**O[(n+1) * L(k)^2]_** Pri čemer vemo da je *L(k)* *fi*^k +(1-*fi*)^k, kjer je *fi* zlati rez.

Torej je **T(n,k) = O[n * L(k)^2] = O[n * *fi*^2k]** 

Prostka zahtevnost pa je *O(n * m)* za "DFSpotomci" (m je število povezav v T), *O(L(k)^2)* za "sl_kompat", *O(L(k))* za "legenda", in *O(n * L(k))* za "maxIndependSet"

Torej je **V(n,k) = O[(n + L(k)) * L(k)] = O[(n + *fi*^k) * *fi*^k]
