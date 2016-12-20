# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"

        # Množimo matriki velikosti n x k in k x m
        # T(n, k, m) ... časovna zahtevnost algoritma
        # S(n, k, m) ... prostorska zahtevnost algoritma

        # Če ima katera izmed matrik, ki ju množimo število stolpcev ali vrstic enako ena, ju zmnožimo z izračunom skalarnega produkta
        # Za to porabimo O(1*k*m) ali O(n*1*m) ali O(n*k*1) časa
        if left.nrow() == 1 or left.ncol() == 1 or right.ncol() == 1:
            return super().multiply(left, right)

        # Devet vrednosti izračunamo in shranimo v O(1) časa in prostora
        n0 = left.nrow() % 2    # 1, če je število vrstic leve matrike liho, drugače 0
        n1, n2 = left.nrow() // 2, left.nrow() - n0
        k0 = left.ncol() % 2    # 1, če je število stolpcev leve matrike in število vrstic desne matrike liho, drugače 0
        k1, k2 = left.ncol() // 2, left.ncol() - k0
        m0 = right.ncol() % 2   # 1, če je število stolpcev desne matrike liho, drugače 0
        m1, m2 = right.ncol() // 2, right.ncol() - m0

        # Zaradi preglednosti in lažjega računanja, naredimo reference na dele matrik, ki jih bomo množili in seštevali
        # Časovna in prostorska zahtevnost sta enaki O(1)
        A, B, C, D = left[0: n1, 0: k1], \
                     left[0: n1, k1: k2], \
                     left[n1: n2, 0: k1], \
                     left[n1: n2, k1: k2]
        E, F, G, H = right[0: k1, 0: m1], \
                     right[0: k1, m1: m2], \
                     right[k1: k2, 0: m1], \
                     right[k1: k2, m1: m2]

        # Za vsakega od sledečih elementov opravimo eno ali dve seštevanji ter izvedemo en klic rekurzije na matrikah velikosti n/2 x k/2 in k/2 x m/2
        # Ustvarimo sedem novih matrik dimenzij n/2 x m/2 - za to porabimo 7*O(n/2*m/2) prostora
        # Ko dve matriki seštevamo ali odštevamo nastane nova matrika dimenzije n/2 x k/2 oziroma k/2 x m/2. To naredimo 10-krat in torej porabimo
        # 5*O(n/2*k/2) in 5*O(k/2*m/2) časa in prostora
        # Za vsak rekurzivni klic porabimo še S(n/2, k/2, m/2) prostora in T(n/2, k/2, m/2) časa
        # Torej skupaj:
        # Prostorska zahtevnost: 7* S(n/2, k/2, m/2) + 7*O(n/2*m/2) + 5*O(n/2*k/2) + 5*O(k/2*m/2)
        # Časovna zahtevnost: 7* T(n/2, k/2, m/2) + 5*O(n/2*k/2) + 5*O(k/2*m/2)
        P1 = A * (F - H)
        P2 = (A + B) * H
        P3 = (C + D) * E
        P4 = D * (G - E)
        P5 = (A + D) * (E + H)
        P6 = (B - D) * (G + H)
        P7 = (A - C) * (E + F)

        if k0 == 0:

            # Naredimo 8 operacij seštevanja oziroma odštevanja in rezultate prepišemo v ciljno matriko
            # Prostorska zahtevonst:  8*O(n/2*m/2) (pri vsaki operaciji se ustvari nova matrika)
            # Časovna zahtevnost: 12*O(n/2*m/2) (8 za operacije in 4 za prepisovanje)
            self[0 : n1, 0 : m1] = P4 + P5 + P6 - P2
            self[n1 : n2, 0 : m1] = P3 + P4
            self[0 : n1, m1 : m2] = P1 + P2
            self[n1 : n2, m1 : m2] = P1 + P5 - P3 - P7

            # Rekurzivno množimo dodatno vrstico v levi matriki z desno matriko
            # Porabimo O(m) prostora
            # Porabimo O(k*m) časa za množenje in O(m) za prepisovanje v dodatno vrstico
            if n0 == 1:
                self[n2, 0: m2 + m0] = left[n2, 0: k2] * right

            # Rekurzivno množimo levo matriko z dodatnim stolpcem v desni matriki
            # Porabimo O(n) prostora
            # Porabimo O(n*k) časa za množenje in O(n) za prepisovanje
            if m0 == 1:
                self[0: n2 + n0, m2] = left * right[0: k2, m2]

            return self

        else:

            # Množimo matriki dimenzij n x (k-1) in (k-1) x m, da pridemo na prejšnji primer
            # Temu dodamo še O(n*m) prostora ko pri množenju nastane nova matrika in O(n*m) časa za prepisovanje
            self[ : , : ] = left[0 : n2 + n0, 0 : k2] * right[0 : k2, 0 : m2 + m0]
            # Na koncu pomnožimo še preostala stolpec in vrstico in produkt prištejemo ciljni matriki
            # Za to porabimo 2*O(n*m) časa (množenje in prištevanje) ter O(n*m) prostora, ko pri množenju nastane nova matrika
            self[ : , : ] += left[0 : n2 + n0, k2] * right[k2, 0 : m2 + m0]

            return self






