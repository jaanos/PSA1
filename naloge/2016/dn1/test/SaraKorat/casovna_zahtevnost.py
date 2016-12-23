from matrix.SaraKorat import SlowMatrix
from matrix.SaraKorat import FastMatrix
from matrix.SaraKorat import CheapMatrix
import time

# Za vsak algoritem posebej je definirana funkcija, ki računa povprečje desetih izračunov, ki da rezultat za primerjavo
# med samimi algoritmi in vhodnimi velikostmi, ter pa za primerjavo med algoritmi

def zahtevnostSM(n, m, k):                                                  # naredimo matriko s samimi enicami
    left = SlowMatrix([[1 for j in range(m)] for i in range(n)])            # n število vrstic, m št. stolpcev matrike left
    right = SlowMatrix([[1 for j in range(k)] for i in range(m)])           # m število vrstic, k št. stolpcev matrike right
    s = []                                                                  # prazen seznam, v katerega shranjujemo rezultate
    for i in range(10):                                                     # izračunamo čas za 10 poskusov
        start = time.time()
        left*right
        end = time.time()
        s.append((end-start))
    povprecje = sum(s)/10                                                   # izračunamo povprečje
    return (povprecje)                                                      # vrnemo povprečje


# Komentarji v naslednjih dveh algoritmih so enaki kot v prejšnjem.
def zahtevnostFM(n, m, k):
    left = FastMatrix([[1 for j in range(m)] for i in range(n)])
    right = FastMatrix([[1 for j in range(k)] for i in range(m)])
    s = []
    for i in range(10):
        start = time.time()
        left*right
        end = time.time()
        s.append((end-start))
    povprecje = sum(s)/10
    return (povprecje)


def zahtevnostCM(n, m, k):
    left = CheapMatrix([[1 for j in range(m)] for i in range(n)])
    right = CheapMatrix([[1 for j in range(k)] for i in range(m)])
    s = []
    for i in range(10):
        start = time.time()
        left*right
        end = time.time()
        s.append((end-start))
    povprecje = sum(s)/10
    return (povprecje)


# Kličemo funkcije za različne vhodne dimenzije
# print(zahtevnostSM(x,y,z))
# print(zahtevnostFM(x,y,z))
# print(zahtevnostCM(x,y,z))




