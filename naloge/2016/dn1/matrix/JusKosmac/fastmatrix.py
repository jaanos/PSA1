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
        
        #velikosti matrik sta m x k in k x n
        #T(m,k,n) naj oznacuje casovno zahtevnost mnozenja teh matrik
        #S(m,k,n) naj oznacuje prostorsko zahtevnost mnozenja teh matrik
        
        #casovna zahtevnost: O(1)
        #prostorska zahtevnost: O(1)
        m = left.nrow()
        k = left.ncol()
        n = right.ncol()

        #ce matrik ne moremo vec razdeliti (vsaj ena dimenzija je enaka 1),
        #uporabimo navadno mnozenje matrik
        #casovna zahtevnost: O(mn) ali O(mk) ali O(nk) (odvisno katera dimanzija je enaka 1)
        #prostorska zahtevnost: O(1)
        if m == 1 or n == 1 or k == 1:
            #klicemo metodo za mnozenje nadrazreda SlowMatrix
            super().multiply(left, right)
        else:
            #dimenzije matrik celostevilsko razpolovimo
            #casovna zahtevnost: O(1)
            #prostorska zahtevnost: O(1)
            m1 = m // 2
            m2 = 2 * m1
            n1 = n // 2
            n2 = 2 * n1
            k1 = k // 2
            k2 = 2 * k1

            #v spremenljivke shranimo reference na posamezne dele vhodnih matrik za nadaljnje delo
            #casovna zahtevnost: O(1)
            #prostorska zahtevnost: O(1) (ne ustvarijo se nove matrike, temveč le reference)
            A = left[0:m1, 0:k1]
            B = left[0:m1, k1:k2]
            C = left[m1:m2, 0:k1]
            D = left[m1:m2, k1:k2]
            
            E = right[0:k1, 0:n1]
            F = right[0:k1, n1:n2]
            G = right[k1:k2, 0:n1]
            H = right[k1:k2, n1:n2]

            #manjse podmatrike rekurzivno zmnozimo, vsako mnozenje in sestevanje/odstevanje
            #ustvarita novo matriko ustreznih dimenzij
            #casovna zahtevnost: 7*T(m/2,k/2,n/2) + 5*O(m/2*k/2) + 5*O(k/2*n/2) (rekurzivno mnozenje, sestevanje v levi matriki in sestevanje v desni matriki)
            #prostorska zahtevnost: 7*S(m/2,k/2,n/2) + 7*O(m/2*n/2) + 5*O(m/2*k/2) + 5*O(k/2*n/2)
            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)
            
            if k2 == k: #k je sod
                #casovna zahtevnost: 8*O(m/2*n/2) (sestevanje) + 4*O(m/2*n/2) (prepisovanje vrednosti v ciljno matriko)
                #prostorska zahtevnost: 8*O(m/2*n/2)
                #ker je k sod, nam ni treba pristevati dodatnih produktov zaradi zadnjega stolpca/vrstice
                self[0:m1, 0:n1] = P4 + P5 + P6 - P2
                self[0:m1, n1:n2] = P1 + P2
                self[m1:m2, 0:n1] = P3 + P4
                self[m1:m2, n1:n2] = P1 + P5 - P3 - P7
                
                if m2 != m: #m je lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    #izracunamo zadnjo vrstico z blocnim mnozenjem
                    #casovna zahtevnost: 4*O(k/2*n/2) (mnozenje) + 4*O(n/2) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: 6*O(n/2)
                    self[m-1, 0:n1] = a * E + b * G
                    self[m-1, n1:n2] = a * F + b * H
                    
                if n2 != n: #n je lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    #izracunamo zadnji stolpec z blocnim mnozenjem
                    #casovna zahtevnost: 4*O(k/2*m/2) (mnozenje) + 4*O(m/2) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: 6*O(m/2)
                    self[0:m1, n-1] = A * c + B * d
                    self[m1:m2, n-1] = C * c + D * d
                    
                if n2 != n and m2 != m: #oba sta liha
                    #izracunamo element (m, n)
                    #casovna zahtevnost: 2*O(k/2) (mnozenje) + O(1) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: O(1)
                    self[m-1, n-1] = a * c + b * d
                    
            else: #k je lih
                #casovna zahtevnost: O(1)
                #prostorska zahtevnost: O(1)
                x = left[0:m1, k-1]
                y = left[m1:m2, k-1]
                u = right[k-1, 0:n1]
                w = right[k-1, n1:n2]

                #casovna zahtevnost: 4*O(m/2*n/2) (mnozenje) + 12*O(m/2*n/2) (sestevanje) + 4*O(m/2*n/2) (prepisovanje vrednosti v ciljno matriko)
                #prostorska zahtevnost: 16*O(m/2*n/2)
                #ker je k lih, moramo poleg P_i - jev upostevati se produkte, ki nastopijo zaradi zadnje vrstice in stolpca
                self[0:m1, 0:n1] = P4 + P5 + P6 - P2 + x * u
                self[0:m1, n1:n2] = P1 + P2 + x * w
                self[m1:m2, 0:n1] = P3 + P4 + y * u
                self[m1:m2, n1:n2] = P1 + P5 - P3 - P7 + y * w
                
                if m2 != m: #m je lih
                    a = left[m-1, 0:k1]
                    b = left[m-1, k1:k2]
                    alfa = left[m-1, k-1]
                    #izracunamo zadnjo vrstico z blocnim mnozenjem
                    #casovna zahtevnost: 2*O(n/2) + 4*O(k/2*n/2) (mnozenje) + 6*O(n/2) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: 10*O(n/2)
                    self[m-1, 0:n1] = a * E + b * G + alfa * u
                    self[m-1, n1:n2] = a * F + b * H + alfa * w
                    
                if n2 != n: #n je lih
                    c = right[0:k1, n-1]
                    d = right[k1:k2, n-1]
                    beta = right[k-1, n-1]
                    #izracunamo zadnji stolpec z blocnim mnozenjem
                    #casovna zahtevnost: 2*O(m/2) + 4*O(k/2*m/2) (mnozenje) + 6*O(m/2) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: 10*O(m/2)
                    self[0:m1, n-1] = A * c + B * d + x * beta
                    self[m1:m2, n-1] = C * c + D * d + y * beta
                    
                if n2 != n and m2 != m: #oba sta liha
                    #izracunamo element (m, n)
                    #casovna zahtevnost: 2*O(k/2) (mnozenje) + O(1) (sestevanje in prepisovanje)
                    #prostorska zahtevnost: O(1)
                    self[m-1, n-1] = a * c + b * d + alfa * beta
                
                
            
