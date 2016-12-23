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

        # Predpostavljajmo: left je dimenzij n*m, right pa m*k

        # Po vrsticah matrike left; n-krat
        for i in range(left.nrow()):
            # Po stolpcih matrike right; k-krat
            for j in range(right.ncol()):
                v = 0  # Porabi O(1) prostora
                # Po elementih i-te vrstice prve in j-tega stolpca druge;    m-krat
                for k in range(left.ncol()):
                    # Sestevek zmnozka teh elementov
                    v += left[i, k] * right[k, j]  # O(1) prostora
                self[i, j] = v

                # Časovna zahtevnost:    O(n*m*k)
                # Prostorska zahtevnost: O(1)
