from matrix.JanGolob import SlowMatrix, FastMatrix, CheapMatrix
import random as rd
import timeit as tm

def testing(n_min, n_max=None, ponovitve=1, s=False, f=False, c=True):
    assert True in (s,f,c), "aa"
    if n_max is None:
        n_max = n_min

    for stevc in range(ponovitve):
        m = rd.randint(n_min, n_max)
        k = rd.randint(n_min, n_max)
        n = rd.randint(n_min, n_max)
        leva = [[None for i in range(k)] for j in range(m)]
        for i in range(m):
            for j in range(k):
                leva[i][j] = rd.randint(0, 9)
        if s:
            Sl = SlowMatrix(leva)
        if f:
            Fl = FastMatrix(leva)
        if c:
            Cl = CheapMatrix(leva)

        desna = [[None for i in range(n)] for j in range(k)]
        for i in range(k):
            for j in range(n):
                desna[i][j] = rd.randint(0, 9)

        if s:
            Sd = SlowMatrix(desna)
        if f:
            Fd = FastMatrix(desna)
        if c:
            Cd = CheapMatrix(desna)

        print(m,k,n, ":")
        if s:
            start_s = tm.default_timer()
            S = Sl * Sd
            end_s = tm.default_timer()
            print(end_s - start_s, "slow")
        if f:
            start_f = tm.default_timer()
            F = Fl*Fd
            end_f = tm.default_timer()
            print(end_f-start_f, "fast")
        if c:
            start_c = tm.default_timer()
            C = Cl * Cd
            end_c = tm.default_timer()
            print(end_c-start_c, "cheap")


def markdown_tabela(velikost, kvadratna=False):
    if kvadratna:
        (m,k,n) = (velikost, velikost, velikost)
    else:
        m = rd.randint(velikost-5, velikost+5)
        k = rd.randint(velikost-5, velikost+5)
        n = rd.randint(velikost-5, velikost+5)
    leva = [[None for i in range(k)] for j in range(m)]
    for i in range(m):
        for j in range(k):
            leva[i][j] = rd.randint(0, 9)
    Sl = SlowMatrix(leva)
    Fl = FastMatrix(leva)
    Cl = CheapMatrix(leva)

    desna = [[None for i in range(n)] for j in range(k)]
    for i in range(k):
        for j in range(n):
            desna[i][j] = rd.randint(0, 9)

    Sd = SlowMatrix(desna)
    Fd = FastMatrix(desna)
    Cd = CheapMatrix(desna)

    start_s = tm.default_timer()
    S = Sl * Sd
    end_s = tm.default_timer()

    start_f = tm.default_timer()
    F = Fl*Fd
    end_f = tm.default_timer()

    start_c = tm.default_timer()
    C = Cl * Cd
    end_c = tm.default_timer()

    assert C==S, "jebi se"
    print("|", m, "|", k, "|", n, "|", end_s - start_s, "|", end_f - start_f, "|", end_c - start_c, "|")


markdown_tabela(8,True)

