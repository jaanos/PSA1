# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """

    # za študiranje časovne in prostorske zahtevnosti
    # si označimo:
    #
    # n...število vrstic leve matrike
    # k...število stolpcev leve matrike, ki je enako številu vrstic desne matrike
    # m...število stolpcev desne matrike
    #
    # T(n,k,m) ... časovna zahtevnost
    # P(n,k,m) ... prostorska zahtevnos

    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"

        stStolpcevLeveMatrike = left.ncol() #izračunamo šrevilo stolpcev leve matrike, ki mora biti enako številu vrstic desne matike, da je množenje sploh definirano
        stVrsticLeveMatrike = left.nrow() #izračunamo število vrstic leve matrike, ki je enako številu vrstic v novi matiki, ki je produkt leve in desne matrike
        stStolpcevDesneMatrike = right.ncol() #izračunamo število stolpcev desne matrike, ki je enako število stolpcev v novi matriki, ki je produktleve in desne matrike

        # na začetku si shranimo 3 vrednosti: P(n,k,m) = O(3) = O(1)
        # na začetku naredimo tri štetja: T(n,k,m) = O(3) = O(1)

        #tako kot v SlowMatrix, tudi v primerih, ko je ena od dimenzij stStolpcevLeveMatike, stVrsticLeveMatrike in stStolpcevDesne matrike enaka 1, izracunamo matriko na roke
        if stStolpcevLeveMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                for j in range(stStolpcevDesneMatrike):
                    self[i, j] = (left[i, 0] * right[0, j])
            return self
        if stVrsticLeveMatrike == 1:
            for j in range(stStolpcevDesneMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[0,k]*right[k,j]
                self[0,j] = vrednost
            return self
        if stStolpcevDesneMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[i,k]*right[k,0]
                self[i,0] = vrednost
            return self

        #v teh treh primerih sta tako časovna, kot tudi prostorska zahtevnost enaki, kot v metodi SlowMatrix

        #lotimo se sedaj matrik vecjih dimenzij

        #za časovno in prostorsko zahtevnost pogledamo najslabši možen primer, ki je pri nas ta, da so vse dimenzije matrik lihe

        #najprej poglejmo mnozenje matrik, katerih dimenzije so sode:

        if stStolpcevLeveMatrike % 2 == 0 and stVrsticLeveMatrike % 2 == 0 and stStolpcevDesneMatrike % 2 == 0:
            A = left[0:stVrsticLeveMatrike//2, 0:stStolpcevLeveMatrike//2]
            B = left[0:stVrsticLeveMatrike//2, stStolpcevLeveMatrike//2:stStolpcevLeveMatrike]
            C = left[stVrsticLeveMatrike//2:stVrsticLeveMatrike, 0:stStolpcevLeveMatrike//2]
            D = left[stVrsticLeveMatrike//2:stVrsticLeveMatrike, stStolpcevLeveMatrike//2:stStolpcevLeveMatrike]
            E = right[0:stStolpcevLeveMatrike//2, 0:stStolpcevDesneMatrike//2]
            F = right[0:stStolpcevLeveMatrike//2, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike]
            G = right[stStolpcevLeveMatrike//2:stStolpcevLeveMatrike, 0:stStolpcevDesneMatrike//2]
            H = right[stStolpcevLeveMatrike//2:stStolpcevLeveMatrike, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike]

            #za izpis teh matrik porabimo konstantno časa, oz. O(8) = O(1),
            #torej je časovna zahtevnost na tem koraku T(n,k,m) = O(1) + O(1) = O(1)
            #prve štiri matrike so velikosti n/2 * k/2, zadnje štiri pa k/2*m/2, torej prostorsko zahtevnost v tem koraku povečamo za
            #O(n/2*k/2+k/2*m/2)=O(n*k+m*k)=O(k*(m+n)), torej je naš nov P(n,k,m) = O(1) + O(k*(m+n)) = O(k*(m+n))

            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)

            #na vsakem od teh korakov naredimo eno ali dve seštevanji v času O(n/2 * k/2) ali O(k/2 * m/2), torej za seštevanje porabimo O(max(m,n)*k) časa,
            #za vsako množenje pa T(n/2, k/2, m/2), torej je v tem koraku časovna zahtevnost enaka T(n,k,m) = O(1) + 7*T(n/2, k/2, m/2) + O(max(m,n)*k)
            #P1,P2,P3,P4,P5,P6,P7 so velikosti n/2*m/2, za zapis vsake od njih porabimo O(n/2*m/2)=O(n*m), zaradi rekurzivnega klica pa v tem koraku porabimo še 7*P(n/2,k/2,m/2),
            #torej je naša prostorska zahtevnost v tem koraku enaka P(n,k,m) = O(1) * O(k*(m+n)) + O(n*m) + 7*P(n/2,k/2,m/2)

            self[0:stVrsticLeveMatrike//2,0:stStolpcevDesneMatrike//2] = (P4 + P5 + P6 -P2)
            self[0:stVrsticLeveMatrike//2, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike] = (P1 + P2)
            self[stVrsticLeveMatrike//2:stVrsticLeveMatrike, 0:stStolpcevDesneMatrike//2] = (P3 + P4)
            self[stVrsticLeveMatrike//2:stVrsticLeveMatrike, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike] = (P1 + P5 - P3 -P7)

            #na tem delu za seštevanje spet porabimo O(max(m,n)*k) časa, torej se časovna zahtevnost na tem koraku ne spremeni
            #tudi prostorska zahtevnost se v tem koraku ne spremeni

            return self

        if stVrsticLeveMatrike % 2 == 1:
            self[0:stVrsticLeveMatrike-1, : ] = left[0:stVrsticLeveMatrike-1, :] * right
            self[stVrsticLeveMatrike-1:stVrsticLeveMatrike, : ] = left[stVrsticLeveMatrike-1:stVrsticLeveMatrike, :] * right
            return self

        #v tem koraku porabimo O(k*m) dodatnega časa
        #v tem koraku porabimo O(1) dodatnega prostora

        if stStolpcevDesneMatrike % 2 == 1:
            self[:, 0:stStolpcevDesneMatrike-1]=left * right[:, 0:stStolpcevDesneMatrike-1]
            self[:, stStolpcevDesneMatrike-1] = left * right[:, stStolpcevDesneMatrike-1]
            return self

        #v tem koraku porabimo O(n*k) dodatnega časa
        #v tem koraku porabimo O(1) dodatnega prostora

        else:
            self[:,:] = left[:, 0:stStolpcevLeveMatrike-1] * right[0:stStolpcevLeveMatrike-1, :] + left[:, stStolpcevLeveMatrike-1] * right[stStolpcevLeveMatrike-1, :]
            return self

        #v tem koraku porabimo O(m*n) dodatnega časa
        #v tem koraku ne porabimo nobenega dodatnega prostora

        # Sklep:
        # Časovna zahtevnost: T(n,k,m) = O(1) + 7*T(n/2, k/2, m/2) + O(max(m,n)*k) + O(n*k) + O(k*m) + O(m*n)
        # Prostorska zahtevnost: P(n,k,m) = O(1) * O(k*(m+n)) + O(n*m) + 7*P(n/2,k/2,m/2) + O(1)


