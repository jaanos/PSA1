# Poroƒçilo

*Jan Perme*

## Kratek opis algoritmov
### Slowmatrix
Algoritem v slowmatrix.py je standardno mnoûenje matrix in torej grem po vseh elementih vseh vrstic prve matrike in jih mnoûi z vsemi elementi vseh stolpcev druge matrike.
```python
for i in range(left.nrow()):
  for j in range(right.ncol()):
    for k in range(left.ncol()):
      self[i,j]+=left[i,k]*right[k,j]
```
Leva matrika: `m*n`
Desna matrika: `n*o`
Ta del kode porabi Ëasovno zahtevnost:`O(m*o*n)` saj v vsakem koraku naredimo eno mnoûenje in eno seötevanje torej `2*m*o*n` operacij
Prostorska zahtevnost:`O(1)` saj ne delamo nobenih novih spremenljivk.
### Fastmatrix
Algoritem v fastmatrix.py je algoritem ki za mnoûenje matrik uporablja Strassenov algoritem.»e matrike niso s sodimi stranicami pa Strassenov algoritem uporabi na podmatriki, ki ima sode stranice in ustrezno pomnoûi preostale vrstice.
```python
if left.nrow()==1:
  for j in range(right.ncol()):
    for i in range(left.ncol()):
      self[0,j]+=left[0,i]*right[i,j]
elif right.ncol()==1:
  for i in range(left.nrow()):
    for k in range(left.ncol()):
      self[i,0]+=left[i,k]*right[k,0]
```
Leva matrika:`1*n(oz m*n)`
Desna matrika:`n*o(oz n*1)`
Ta del kode nam porabi Ëasovno zahtevnost:`O(max(o*n,m*n))` saj v obeh primerih v zanki naredimo 2 operaciji (seötevanje in mnoûenje) in to `o*n` krat oz `m*n` krat.
Prostorska zahtevnost:`O(1)` saj ne delamo nobenih novih spremenljivk
```python
A=(left[0:(left.nrow()//2),0:(left.ncol()//2)])
B=(left[0:(left.nrow()//2),(left.ncol()//2):(2*(left.ncol()//2))])
C=(left[(left.nrow()//2):(2*(left.nrow()//2)),0:(left.ncol()//2)])
D=(left[(left.nrow()//2):(2*(left.nrow()//2)),(left.ncol()//2):(2*(left.ncol()//2))])
E=(right[0:(right.nrow()//2),0:(right.ncol()//2)])
F=(right[0:(right.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))])
G=(right[(right.nrow()//2):(2*(right.nrow()//2)),0:(right.ncol()//2)])
H=(right[(right.nrow()//2):(2*(right.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))])
#naredimo P1,P2,...
P1 = A * (F-H)
P2 = (A + B)*H
P3 = (C + D)*E
P4 = D*(G - E)
P5 = (A + D)*(E + H)
P6 = (B - D)*(G + H)
P7 = (A - C)*(E + F)
#v naso matriko zapisemo rezultat Strassenovega algoritma za kvadratno matriko. Ce je katera od zacetnih matrik lihih dimenzij ima nasa matrika se prazen stolpec in/ali vrstico
self[0:(left.nrow()//2),0:(right.ncol()//2)]=P4 + P5 + P6 - P2
self[(left.nrow()//2):(2*(left.nrow()//2)),0:(right.ncol()//2)]=P3 + P4
self[0:(left.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))]=P1+P2
self[(left.nrow()//2):(2*(left.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))]=P1 + P5 - P3 - P7
```
Leva matrika: `m*n`
Desna matrika: `n*o`
»asovna zahtevnost:Na zaËetku kode samo delamo pointerje kar je `O(1)`. Seötevanje matrik ima Ëasovno zahtevnost `O(n*m)`oz `O(n*o)` naredimo pa ga 20 krat. Z rekurzijo pa lahko ugotovimo öe Ëasovno zahtevnost mnoûenja,ki je `7*T(n/2)`. Tako dobimo `T(n)=7*T(n/2)+O(n^2)`. Iz krovnega izreka sledi da je `T(n)=O(n^```{r}log2(7)```)`
Prostorska zahtevnost:Matrike A,B,C,... so samo pointerji tako da porabijo O(1) prostroa medtem ko so P1,P2,P3,... nove matrike in za vsako od njih porabimo `n/2*o/2` prostora. Med raËunanjem P1,P2,P3... tudi seötevamo matrike in vsako seötevanje ustvari novo matriko(pri raËunanju P1,P2,P3,.. drugje se nove matrike ne ustvarijo) to je öe 10 novih matrik. 5 od teh jih je velikosti `m/2*n/2` 5 pa velikosti `n/2*o/2`.Torej je prostorska zahtevnost `O(max{n*m,n*o,o*m})`.
```python
if (left.ncol())%2==1:
    for i in range(2*(left.nrow()//2)): #2*(left.nrow()//2) da ne stejemo tistega zadnjega elementa na mestu(n,n) leve matrike 2-krat ce velja tudi (left.nrow()%2)==1:
        for j in range(2*(right.ncol()//2)): # 2*(right.ncol()//2) da ne stejemo zadnjega stolpca desne matrike 2-krat ce velja tudi (right.ncol()%2)==1
            self[i,j]+=left[i,left.ncol()-1]*right[right.nrow()-1,j]
#obravnavamo primer, ce ima leva matrika liho stevilo vrstic
if (left.nrow()%2)==1:
    for j in range(2*(right.ncol()//2)): # 2*(right.ncol()//2) da ne stejemo zadnjega stolpca desne matrike 2-krat ce velja tudi (right.ncol()%2)==1
        for i in range(left.ncol()):
            self[left.nrow()-1,j]+=left[left.nrow()-1,i]*right[i,j]
#obravnavamo primer, ce ima desna matrika liho stevilo stolpcev
if (right.ncol()%2)==1:
    for i in range(left.nrow()):
        for j in range(left.ncol()):
            self[i,right.ncol()-1]+=left[i,j]*right[j,right.ncol()-1]
```
Leva matrika: `m*n`
Desna matrika: `n*o`
»asovna zahtevnost:Ker tukaj samo mnoûimo 1 vrstiËni stolpec z vrstico/vrsticami je algoritem enkao zahteven kot del kode na zaËetku fastmatrix.py. Torej je Ëasovna zahtevnost `O(max{m*o,o*n,m*n})`
Prostroska zahtevnost: `O(1)` z istim razlogom kot zgoraj.

Celotna Ëasovna zahtevnost:`O(n^```{r}log2(7)```)`
Celotna prostorska zahtevnost:`O(max{n*m,n*o,o*m})`
### Cheapmatrix
Algoritem v cheamatrix.py je samo preoblikovan algoritem iz fastmatrix.py tako, da je njegova prostorska poraba `O(log(m*n*o))`
Prvi del cheapmatrix je identiËen fastmatrix zato je tudi prostorska in Ëasovna poraba enaka. RazliËni je samo del spodaj zato bom samo zanj raËunal prostorsko in Ëasovno porabo.
```python
F-=H
W_1.multiply(A,F,W_2)
F+=H
D_3+=W_1
D_4+=W_1
W_1[:,:]=0
#P2
A+=B
W_1.multiply(A,H,W_2)
A-=B
D_1-=W_1
D_3+=W_1
W_1[:,:]=0
#P3
C+=D
W_1.multiply(C,E,W_2)
C-=D
D_2+=W_1
D_4-=W_1
W_1[:,:]=0
#P4
G-=E
W_1.multiply(D,G,W_2)
G+=E
D_1+=W_1
D_2+=W_1
W_1[:,:]=0
#P5
A+=D
E+=H
W_1.multiply(A,E,W_2)
A-=D
E-=H
D_1+=W_1
D_4+=W_1
W_1[:,:]=0
#P6
B-=D
G+=H
W_1.multiply(B,G,W_2)
B+=D
G-=H
D_1+=W_1
W_1[:,:]=0
#P7
A-=C
E+=F
W_1.multiply(A,E,W_2)
A+=C
E-=F
D_4-=W_1
W_1[:,:]=0
```
Leva matrika: `m*n`
Desna matrika: `n*o`
»asovna zahtevnost: Imamo 32 seötevanj, ki vsako porabi `O(n*m)`oz `O(n*o)` in öe 7 mnoûenj. Z rekurzivno formulo tako dobimo `T(n)=7*T(n/2)+O(n^2)` in podobno kot prej vidimo da je Ëasovna zahtevnost `O(n^```{r}log2(7)```)`
Prostroska zahtevnost:`O(1)` saj ne spreminjamo niËesar drugega kot vhodnih matrik.

Zadnji del je spet identiËen kot pri fastmatrix.

Celotna Ëasovna zahtevnost:`O(n^```{r}log2(7)```)`
Celotna prostroska zahtevnost:`O(1)`

## Testiranje
