# -*- coding: utf-8 -*-
from ..matrix import AbstractMatrix

class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede z izračunom skalarnih produktov
        vrstic prve in stolpcev druge matrike.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"

        stStolpcevLevaMatrika = left.ncol() #izračunamo šrevilo stolpcev leve matrike, ki mora biti enako številu vrstic desne matike, da je množenje sploh definirano
        stVrsticLevaMatrika = left.nrow() #izračunamo število vrstic leve matrike, ki je enako številu vrstic v novi matiki, ki je produkt prve in druge matrike
        stStolpcevDesnaMatrika = right.ncol()

        for i in range(stVrsticLevaMatrika):
            #pomnozi i-to vrstico prve (leve) matrike) z i-tim stolpcem druge (desne) matrike
            for j in range (stStolpcevDesnaMatrika):
                #zdaj smo izbrali vrstico in stolpec, napisati moramo skalarni produkt teh dveh
                #izracunamo skalarni produkt
                vrednost = 0
                for k in range(stStolpcevLevaMatrika):
                    vrednost += (left[i,k]*right[k,j])
                self[i,j] = vrednost
        return self


