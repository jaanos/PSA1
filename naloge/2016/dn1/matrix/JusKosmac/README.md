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

*Časovna zahtevnost*  
S T(*m,k,n*) označimo časovno zahtevnost množenja matrik. V najslabšem primeru so vsi *m, k* in *n* lihi, torej moramo opravljati dodatno delo.
V datoteki z algoritmom so opisane časovne zahtevnosti posameznih korakov. Če seštejemo zahtevnosti vseh korakov, dobimo rekurzivno formulo
T(*m,k,n*) = 7\*T(*m/2,k/2,n/2*) + 9\*O(*m/2\*k/2*) + 9\*O(*k/2\*n/2*) + 20\*O(*m/2\*n/2*) + 8\*O(*m/2*) + 8*O(*n/2*) + 2*O(*k/2*).
Če upoštevamo, da zadnje 3 člene linearne zahtevnosti lahko zanemarimo, in uvedemo *N* = max(*m,k,n*), se nam formula poenostavi v
T(*N*) = 7\*T(*N/2*) + 38\*O(*N^2*). Krovni izrek nam pove, da je skupna časovna zahtevnost T(*N*) = *N*^(log_2(7)).

*Prostorska zahtevnost*  
S S(*m,k,n*) označimo prostorsko zahtevnost množenja matrik. Spet obravnavamo je najslabši primer.
Velja S(*m,k,n*) = 7\*S(*m/2,k/2,n/2*) + 23\*O(*m/2\*n/2*) + 5\*O(*m/2\*k/2*) + 5\*O(*k/2\*n/2*) + 10\*O(*m/2*) + 10\*O(*n/2*).
Spet lahko enačbo poenostavimo v S(*N*) = 7*S(*N/2*) + 33*O(*N^2*), torej je S(*N*) = *N*^(log_2(7)).

__CheapMatrix__  
Algoritem za množenje je enak kot pri FastMatrix, le da varčuje s prostorom. Pomagamo si z dodatno delovno matriko, v katero shranjujemo vmesne rezultate množenja.
Podrobnejši komentarji so v datoteki z algoritmom.

*Časovna zahtevnost*  
S T(*m,k,n*) spet označimo časovno zahtevnost množenja matrik.
Velja T(*m,k,n*) = 7\*T(*m/2,k/2,n/2*) + 13\*O(*m/2\*k/2*) + 13\*O(*k/2\*n/2*) + 16\*O(*m/2\*n/2*) + 4\*O(*m/2*) + 4\*O(*n/2*) + 2\*O(*k/2*) 
oziroma T(*N*) = 7\*T(*N/2*) + 42\*O(*N^2*), kar nam spet da časovna zahtevnost T(*N*) = *N*^(log_2(7)). Torej je rezultat enak kot pri FastMatrix, razlikuje se le v konstanti. 
Pri CheapMatrix smo opravljali precej več seštevanj, saj smo morali vhodni matriki ves čas popravljati nazaj na prvotno stanje. Nekaj dela pa smo si prihranili, 
ko smo rezultate množenj zapisovali direktno v ciljno matriko in nam jih ni bilo potrebno naknadno prepisovati v ciljno matriko.

*Prostorska zahtevnost*  
Algoritem na začetku ustvari delovno matriko, ki je enakih dimenzij kot ciljna matrika. S tem porabi O(mn) dodatnega prostora. Poleg rekurzivnih klicev smo porabili
le O(1) prostora. Rekurzivne klice opravljamo vedno z deli že obstoječe delovne matrike, torej se ne ustvarjajo nove delovne matrike.
Toda po krovnem izreku iz enačbe S(*m,k,n*) = 7\*S(*m/2,k/2,n/2*) + O(1) še vedno sledi enaka prostorska zahtevnost kot prej, torej S(*N*) = *N*^(log_2(7)).

##Primerjava časov izvajanja algoritmov
