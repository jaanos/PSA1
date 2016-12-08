# -*- coding: utf-8 -*-
#from ..matrix import AbstractMatrix

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

        #raise NotImplementedError("Naredi sam!")

        for i in range(left.nrow()):                # Gremo po vrsticah matrike left.
            for k in range(right.ncol()):           # Gremo po stolpcih matrike right
                l = 0                               # Pripravimo število, ki bo po seštevku zmnožkov vrstic matrike left in stolpcev matrike right, enako [i, k] elementu nove matrike.              
                for j in range(right.nrow()):       # Gremo po vseh elementih prve vrstice matrike left in vseh stolpcih matrike right.
                    l += left[i,j]*right[j, k]      # Vsak zmnožek prištejemo številu l, da dobimo [i, k]-ti element.
                self[i, k] = (l)                    # Novi matriki dodamo na novo izračunan element.

        

        


        
