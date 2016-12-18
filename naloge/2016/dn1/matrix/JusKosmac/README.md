#Poročilo

*Juš Kosmač*

##Opis algoritmov, prostorska in časovna zahtevnost
Implementirane so tri metode za množenje matrik poljubnih velikosti. Prostorska in časovna zahtevnost bosta vedno izračunani
za množenje matrik velikosti *m x k* in *k x n*.
  

__SlowMatrix__  
Matrike množimo na običajen način, *(i, j)*-ti element ciljne matrike izračunamo kot skalarni produkt *i*-te vrstice in *j*-tega stolpca vhodnih matrik.

*Časovna zahtevnost*  
Za izračun posameznega elementa porabimo O(*k*) operacij, velikost ciljne matrike je *m x n*, torej skupno porabimo O(*mnk*) operacij. 

*Prostorska zahtevnost*  
Pri računanju skalarnih produktov vmesne produkte vedno prištevamo isti spremenljivki, torej ne porabljamo nič novega prostora. 
Prostorska zahtevnost je torej O(1).


__FastMatrix__  
Matrike množimo z uporabo Strassenovega algoritma. Algoritem razpolovi stranici obeh matrik (če sta večji kot 1) in s tem vsako razdeli na 4 podmatrike.
Podmatrike rekurzivno zmnožimo s 7 množenji in nato s seštevanjem/odštevanjem skonstruiramo ustrezne podmatrike v ciljni matriki.
Če matriki nimata stranic sodih dolžin, zadnji stolpec oz. zadnjo vrstico obravnavamo posebej.

Skica deljenja matrik (zadnji stolpec in zadnja vrstica nastopita samo, če so dimenzije lihe):
```
[ A B x]    [ E F c]
[ C D y]    [ G H d]
[ a b alfa] [ u w beta]
```

*Časovna zahtevnost*  
S T(*m,k,n*) označimo časovno zahtevnost množenja matrik. V najslabšem primeru so vsi *m, k* in *n* lihi, torej moramo opravljati dodatno delo.
V datoteki z algoritmom so opisane časovne zahtevnosti posameznih korakov. Če seštejemo zahtevnosti vseh korakov, dobimo rekurzivno formulo  
T(*m,k,n*) = 7\*T(*m/2,k/2,n/2*) + 9\*O(*m/2*\**k/2*) + 9\*O(*k/2*\**n/2*) + 20\*O(*m/2*\**n/2*) + 8\*O(*m/2*) + 8\*O(*n/2*) + 2\*O(*k/2*).  
Če upoštevamo, da zadnje 3 člene linearne zahtevnosti lahko zanemarimo, in uvedemo *N* = max(*m,k,n*), se nam formula poenostavi v
T(*N*) = 7\*T(*N/2*) + 38\*O(*N^2*). Krovni izrek nam pove, da je skupna časovna zahtevnost T(*N*) = O(*N*^(log_2(7))).

*Prostorska zahtevnost*  
S S(*m,k,n*) označimo prostorsko zahtevnost množenja matrik. Spet obravnavamo le najslabši primer.
Velja  
S(*m,k,n*) = 7\*S(*m/2,k/2,n/2*) + 23\*O(*m/2*\**n/2*) + 5\*O(*m/2*\**k/2*) + 5\*O(*k/2*\**n/2*) + 10\*O(*m/2*) + 10\*O(*n/2*).  
Spet lahko enačbo poenostavimo v S(*N*) = 7\*S(*N/2*) + 33\*O(*N^2*), torej je S(*N*) = O(*N*^(log_2(7))).

__CheapMatrix__  
Algoritem za množenje je enak kot pri FastMatrix, le da varčuje s prostorom. Pomagamo si z dodatno delovno matriko, v katero shranjujemo vmesne rezultate množenja.
Podrobnejši komentarji so v datoteki z algoritmom.

*Časovna zahtevnost*  
S T(*m,k,n*) spet označimo časovno zahtevnost množenja matrik.
Velja  
T(*m,k,n*) = 7\*T(*m/2,k/2,n/2*) + 13\*O(*m/2*\**k/2*) + 13\*O(*k/2*\**n/2*) + 16\*O(*m/2*\**n/2*) + 4\*O(*m/2*) + 4\*O(*n/2*) + 2\*O(*k/2*)   
oziroma T(*N*) = 7\*T(*N/2*) + 42\*O(*N^2*), kar nam spet da časovna zahtevnost T(*N*) = O(*N*^(log_2(7))). Torej je rezultat enak kot pri FastMatrix, razlikuje se le v konstanti. 
Pri CheapMatrix smo opravljali precej več seštevanj, saj smo morali vhodni matriki ves čas popravljati nazaj na prvotno stanje. Nekaj dela pa smo si prihranili, 
ko smo rezultate množenj zapisovali direktno v ciljno matriko in nam jih ni bilo potrebno naknadno prepisovati.

*Prostorska zahtevnost*  
Algoritem na začetku ustvari delovno matriko, ki je enakih dimenzij kot ciljna matrika. S tem porabi O(mn) dodatnega prostora. Poleg rekurzivnih klicev smo porabili
le O(1) prostora. Rekurzivne klice opravljamo vedno z deli že obstoječe delovne matrike, torej se ne ustvarjajo nove delovne matrike.
Toda po krovnem izreku iz enačbe S(*m,k,n*) = 7\*S(*m/2,k/2,n/2*) + O(1) še vedno sledi enaka prostorska zahtevnost kot prej, torej S(*N*) = O(*N*^(log_2(7))).

##Primerjava časov izvajanja algoritmov
Primerjali bomo samo množenje kvadratnih matrik. Če bi množili matrike, ki imajo eno dimenzijo precej večjo ali manjšo od ostalih dveh, bi lahko naredili sorazmerno malo razpolavlanj, preden bi prišli do stranice z velikostjo 1. V tem primeru pa vsi trije algoritmi delujejo enako. Zato bi tudi pri FastMatrix in CheapMatrix večino dela opravili z običajnim množenjem in bi zmanjšali razliko med časovno zahtevnostjo SlowMatrixa in Fast/CheapMatrixa.  

Za *m*=*k*=*n*=1, ..., 150 smo generirali naključne matrike s celoštevilskimi elementi med -100 in 100. Za vsakega izmed treh razredov smo ustvarili dve matriki in izmerili koliko časa potrebujemo za množenje. Graf je prikazan na spodnji sliki (čas smo merili v sekundah): modra barva predstavlja SlowMatrix, rdeča in zelena pa FastMatrix in CheapMatrix.  

![graf2](https://cloud.githubusercontent.com/assets/13056585/21294589/80555c9e-c540-11e6-9cbd-1b07fd183025.png)

Vidimo lahko, da med Fast in CheapMatrix ni skoraj nobene razlike, SlowMatrix pa je precej hitrejši od obeh. Kljub temu, da ima običajno množenje asimptotično slabšo časovno zahtevnost, pa so konstante pri Strassenovem algoritmu tako velike, da je za manjše matrike tako množenje veliko počasnejše. Opazimo tudi, da čas za množenje s SlowMatrixom, narašča zelo enakomerno, pri Fast/CheapMatrixu pa imamo na nekaterih mestih občutne skoke. Največji skok se zgodi pri dimenziji 128 = 2^7, ko moramo matriko še sedmič razpoloviti in s tem povečamo globino rekurzije (ostali večji skoki so pri 64 = 2^6 in 96 = 64 + 32). Če pa ostajamo na istem nivoju rekurzije, čas tudi tukaj narašča dokaj enakomerno.  

Če si ogledamo matrike malo večjih dimenzij (*m*=*k*=*n*=100, 200, ..., 600), opazimo, da čas (spet merjen v sekundah) za množenje narašča v skladu z izračunano časovno zahtevnostjo. Modre točke pripadajo FastMatrixu, rdeče pa SlowMatrixu.

![graf1](https://cloud.githubusercontent.com/assets/13056585/21294588/753710be-c540-11e6-9de7-9f9494fbd323.png)

Z modro in rdečo krivuljo, smo poskusili točke najbolje aproksimirati po metodi najmanjših kvadratov. Za rdečo krivuljo smo izbrali najbolj prilegajoč polinom tretje stopnje (2.2311e-005\*x^3 - 3.2437e-003\*x^2 + 2.3498e-002\*x + 6.5569e+000). Modre točke nismo mogli aproksimirati s polinomom, saj je časovna zahtevnost O(*m*^(log_2(7))). Lahko bi jih aproksimirali z racionalno funkcijo, pri kateri se razmerje stopenj polinomov v števcu in imenovalcu čimbolj približa log_2(7) = 2,81. Z razlogom poenostavitve pa smo jih aproksimirali kar s funkcijo oblike *a*\*x^2,81 (a = 1.2169e-004). S tem lahko ocenimo približno velikost matrike, pri kateri bi FastMatrix množil hitreje kot SlowMatrix. Izkaže se, da se to zgodi pri približno *m*=*k*=*n*=8300. 

