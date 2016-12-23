# -*- coding: utf-8 -*-
from matrix import AbstractMatrix


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

        # Množimo matriki velikosti n x k in k x m
        # T(n, k, m) ... časovna zahtevnost algoritma
        # S(n, k, m) ... prostorska zahtevnost algoritma

        for i in range(self.nrow()):
            for j in range(self.ncol()):
                self[i, j] = left[i, 0] * right[0, j]  # n*m-krat opravimo eno množenje
                for k in range(1, left.ncol()):
                    self[i, j] += left[i, k] * right[k, j]  # še n*m*(k-1)-krat množimo in seštejemo; vse te operacije imajo časovno zahtevnost O(1)

        # T(n, k, m) = O(n*k*m)
        # S(n, k, m) = 0, saj ne porabimo nobenega dodatnega prostora