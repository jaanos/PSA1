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

        stStolpcevLeveMatrike = left.ncol()
        stVrsticLeveMatrike = left.nrow()
        stStolpcevDesneMatrike = right.ncol()

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

        #lotimo se sedaj matrik vecjih dimenzij

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

            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)

            self[0:stVrsticLeveMatrike//2,0:stStolpcevDesneMatrike//2] = (P4 + P5 + P6 -P2)
            self[0:stVrsticLeveMatrike//2, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike] = (P1 + P2)
            self[stVrsticLeveMatrike//2:stVrsticLeveMatrike, 0:stStolpcevDesneMatrike//2] = (P3 + P4)
            self[stVrsticLeveMatrike//2:stVrsticLeveMatrike, stStolpcevDesneMatrike//2:stStolpcevDesneMatrike] = (P1 + P5 - P3 -P7)

            return self

        if stVrsticLeveMatrike % 2 == 1:
            prilagojenaLevaMatrika = left[0:stVrsticLeveMatrike-1, :]
            zadnjaLevaVrstica = left[stVrsticLeveMatrike-1:stVrsticLeveMatrike, :]
            self[0:stVrsticLeveMatrike-1, : ] = prilagojenaLevaMatrika * right
            self[stVrsticLeveMatrike-1:stVrsticLeveMatrike, : ] = zadnjaLevaVrstica * right
            return self

        if stStolpcevDesneMatrike % 2 == 1:
            prilagojenaDesnaMatrika = right[:, 0:stStolpcevDesneMatrike-1]
            zadnjiDesniStolpec = right[:, stStolpcevDesneMatrike-1]
            self[:, 0:stStolpcevDesneMatrike-1]=left * prilagojenaDesnaMatrika
            self[:, stStolpcevDesneMatrike-1] = left * zadnjiDesniStolpec
            return self

        else:
            prilagojenaLevaMatrika = left[:, 0:stStolpcevLeveMatrike-1]
            zadnjiStolpecLeveMatrike = left[:, stStolpcevLeveMatrike-1]
            prilagojenaDesnaMatrika = right[0:stStolpcevLeveMatrike-1, :]
            zadnjaVrsticaDesneMatrike = right[stStolpcevLeveMatrike-1, :]
            self[:,:] = prilagojenaLevaMatrika * prilagojenaDesnaMatrika + zadnjiStolpecLeveMatrike * zadnjaVrsticaDesneMatrike
            return self


