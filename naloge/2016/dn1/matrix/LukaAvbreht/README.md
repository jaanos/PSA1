# Poročilo

*Luka Avbreht*

Sem napišite poročilo o vaši domači nalogi. Za oblikovanje uporabite [Markdown](https://guides.github.com/features/mastering-markdown/).

## SlowMatrix

Gre za običajno množenje matrik, kot ga ponavadi izvajamo na roke.

### Časovna zahtevbnost 

Če zmnožimo matriki `(n x m)` in `(m x k)`, je časovna zahtevnost `O(n*m*k)` oziroma približno 
`O(n^3)`. 

### Prostorska zahtevnost

Če zmnožimo matriki `(n x m)` in `(m x k)` je prostorska zahtevnost 
`O(n*m)+O(m*n)+O(n*k)` Kar lahko ocenimo z `O(max{m,n,k})`. Z drugimi besedami 
ne potrebujemo nobenega dodatnega prostora kot velikosi ciljne matrike.

## FastMatrix

Pomagali si bomo z tako imenovanim Strassenovim algoritmom.

### Časovna zahtevnost

Z krovnim izrekom lahko dokažemo da ...
