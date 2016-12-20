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
        A.copy(left[0:(left.nrow()//2),0:(left.ncol()//2))
        B.copy(left[0:(left.nrow()//2),(left.ncol()//2)):(2*(left.ncol()//2))])
        C.copy(left[(left.nrow()//2):(2*(left.nrow()//2)),0:(left.ncol()//2)])
        D.copy(left[(left.nrow()//2):(2*(left.nrow()//2)),(left.ncol()//2):(2*(left.ncol()//2))])
        E.copy(right[0:(right.nrow()//2),0:(right.ncol()//2))
        F.copy(right[0:(right.nrow()//2),(right.ncol()//2)):(2*(right.ncol()//2))])
        G.copy(right[(right.nrow()//2):(2*(right.nrow()//2)),0:(right.ncol()//2)])
        H.copy(right[(right.nrow()//2):(2*(right.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))])
