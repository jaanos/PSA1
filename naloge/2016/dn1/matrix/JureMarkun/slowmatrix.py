# -*- coding: utf-8 -*-
from ..matrix import AbstractMatrix
import time

class SlowMatrix(AbstractMatrix):
    """
    Matrika z naivnim množenjem.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede z izračunom skalarnih produktov
        vrstic prve in stolpcev druge matrike."""""
        m = right.nrow()  # št. stolpcev prve = št.vrstic druge
        n = left.nrow() #št.vrstic prve
        l = right.ncol()  #št.stolpcev druge

        #skica
        #      m                l               l
        #   [       ]       [        ]      [       ]
        # n [       ]   * m [        ] =  n [       ]
        #   [       ]       [        ]      [       ]
        assert left.ncol() == right.nrow(), \
            "Dimenzije matrik ne dopuščajo množenja!"

        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
             "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        for n1 in range(n):
            for l1 in range(l):
                for m1 in range(m):
                    self[n1,l1] += left[n1,m1]*right[m1,l1]
        return self

#######################################

#C = AbstractMatrix([[3,2,1],[3,5,1]])
#D = AbstractMatrix([[1],[8],[5]])
#E = AbstractMatrix([[0],[0]])

#print(SlowMatrix.multiply(E,C,D))

#T = AbstractMatrix([[1, 2, 1, 0, 0, 3, 3, 3, 3, 3, 5, 3, 4, 5],
                    # [2, 1, 0, 1, 0, 4, 5, 6, 7, 8, 8, 3, 4, 5],
                    # [1, 2, 5, 3, 3, 5, 5, 6, 2, 7, 7, 3, 3, 7],
                    # [2, 1, 0, 1, 0, 4, 5, 6, 7, 8, 8, 4, 5, 4],
                    # [2, 1, 0, 1, 0, 4, 5, 6, 7, 8, 8, 3, 2, 4]])
#S = AbstractMatrix([[2, 8, 2, 0, 0, 1, 2],
                    # [1, 3, 0, 1, 8, 5, 2],
                    # [0, 2, 0, 1, 0, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [3, 4, 6, 2, 3, 1, 3],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2],
                    # [2, 1, 2, 1, 2, 1, 2]])
#U = AbstractMatrix([([0, ] * 7), ] * 5)

#start = time.time()
#print(SlowMatrix.multiply(U,T,S),"Slow")
#end = time.time()
#print(end - start,"tempus")
########################################
#Ciljna matrika more bit matrika ničel.