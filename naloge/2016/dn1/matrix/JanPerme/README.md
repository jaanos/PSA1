# Poroƒçilo

*Jan Perme*

## Kratek opis algoritmov
### slowmatrix.py
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
###fastmatrix.py
Algoritem v fastmatrix.py je algoritem ki za mnoûenje matrik uporablja Strassenov algoritem.
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
»asovna zahtevnost:
