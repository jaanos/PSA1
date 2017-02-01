# -*- coding: utf-8 -*-
from ..matrix import AbstractMatrix

class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """

        # za študiranje časovne in prostorske zahtevnosti
        # si označimo:
        #
        # n...število vrstic leve matrike
        # k...število stolpcev leve matrike, ki je enako številu vrstic desne matrike
        # m...število stolpcev desne matrike
        #
        # T(n,k,m) ... časovna zahtevnost
        # P(n,k,m) ... prostorska zahtevnost

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
        stVrsticLevaMatrika = left.nrow() #izračunamo število vrstic leve matrike, ki je enako številu vrstic v novi matiki, ki je produkt leve in desne matrike
        stStolpcevDesnaMatrika = right.ncol() #izračunamo število stolpcev desne matrike, ki je enako število stolpcev v novi matriki, ki je produktleve in desne matrike

        #na začetku si shranimo 3 vrednosti: P(n,k,m) = O(3) = O(1)
        #na začetku naredimo tri štetja: T(n,k,m) = O(3) = O(1)

        for i in range(stVrsticLevaMatrika):
            #pomnozi i-to vrstico prve (leve) matrike) z i-tim stolpcem druge (desne) matrike
            for j in range (stStolpcevDesnaMatrika):
                #zdaj smo izbrali vrstico in stolpec, napisati moramo skalarni produkt teh dveh
                #izracunamo skalarni produkt
                vrednost = 0
                # ta vrednost je vedno enaka, zato ne zavzame O(n*m) prostora,
                # temveč samo O(1), torej je zdaj P(n,k,m) = O(1) + O(1) = O(1)
                for k in range(stStolpcevLevaMatrika):
                    vrednost += (left[i,k]*right[k,j])
                    # tu imamo dve operaciji, torej O(2) = O(1), ampak ker smo do tega prišli n*k*m-krat,
                    # imamo O(n*k*m), torej imamo zdaj T(n,k,m) = O(1) + O(n*k*m) = O(n*k*m)
                self[i,j] = vrednost
        return self, self.ncol()


        # sklep:
        # - časovna zahtevnost: T(n,k,m) = O(n*k*m)
        # - prostorska zahtevnost: P(n,k,m) = O(1)