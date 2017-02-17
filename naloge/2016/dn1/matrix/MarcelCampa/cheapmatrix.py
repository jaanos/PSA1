# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """
    def multiply(self, left, right, work = None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if work is None:
            work = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"
        
        #časovna zahtevnost O(1)
        #prostorska zahtevnost O(1)
        m = left.nrow()
        k = left.ncol()
        n = right.ncol()
        
        #če je katera izmed dimenzij matrike enaka 1, uporabimo kar naivno množenje
        #časovna zahtevnost O(mn), če k==1 / O(kn), če m==1 / O(mk), če n==1
        #prostorska zahtevnost O(1)
        if m==1 or k==1 or n==1:
            super().multiply(left,right)
        
        else:
            #pripravimo si različne dimenzije matrik
            #časovna zahtevnost O(1)
            #prostorska zahtevnost (1)
            new_m = m//2
            new_M = 2*new_m
            new_k = k//2
            new_K = 2*new_k
            new_n = n//2
            new_N = 2*new_n
            
            #shranimo si pointerje do matrik (vsaj tako naj bi bilo implementirano)
            #časovna zahtevnost O(1)
            #prostorska zahtevnost O(1), namreč shranimo se le pointerje in ne prepisujemo matrik
            A = left[0:new_m, 0:new_k]
            B = left[0:new_m, new_k:new_K]
            C = left[new_m:new_M, 0:new_k]
            D = left[new_m:new_M, new_k:new_K]
            E = right[0:new_k, 0:new_n]
            F = right[0:new_k, new_n:new_N]
            G = right[new_k:new_K, 0:new_n]
            H = right[new_k:new_K, new_n:new_N]
            
            #Ker želimo prostorsko nepotraten algoritem, ne ustvarjamo novih matrik (operatorja += in -= namreč tako delujeta). Seveda moramo takoj vse spremembe invertirati.
            #Da ne porabljamo dodatnega prostora, računamo kar direktno v matriki self, z work matriko si pomagamo za vmesno shranjevanje, saj nam work matrika daje dragocen prostor.
            #časovna zahtevnost 7*T(m//2, k//2, n//2) (množenje) + 10*O(m//2 * k//2) (seštevanje matrik iz left) + 10*O(k//2 * n//2) (seštevanje matrik iz right) + O(m//2 * n//2) (množenje z -1)
            #   T(m,k,n) označuje čas za rekurzivno množenje matrik dimenzij (m,k) in (k,n)
            #prostorska zahtevnost 7*X(m//2, k//2, n//2)
            #   X(m,k,n) označuje prostor, ki ga porabimo pri rekurzivnem množenju matrik dimenzij (m,k) in (k,n)
            
            # računamo P6
            B -= D
            G += H
            self[0:new_m, 0:new_n].multiply(B, G, work[new_m:new_M, new_n:new_N])
            B += D
            G -= H
            
            #računamo P1
            F -= H
            self[0:new_m, new_n:new_N].multiply(A, F, work[new_m:new_M, new_n:new_N])
            F += H
            
            #računamo P3
            C += D
            self[new_m:new_M, 0:new_n].multiply(C, E, work[new_m:new_M, new_n:new_N])
            C -= D
            
            #računamo -P7
            A -= C
            E += F
            self[new_m:new_M, new_n:new_N].multiply(A, E, work[new_m:new_M, new_n:new_N])
            self[new_m:new_M, new_n:new_N] *= -1
            A += C
            E -= F
            
            #računamo P2
            A += B
            work[0:new_m, 0:new_n].multiply(A, H, work[new_m:new_M, new_n:new_N])
            A -= B
            
            #računamo P4
            G -= E
            work[0:new_m, new_n:new_N].multiply(D, G, work[new_m:new_M, new_n:new_N])
            G += E
            
            #računamo P5
            A += D
            E += H
            work[new_m:new_M, 0:new_n].multiply(A, E, work[new_m:new_M, new_n:new_N])
            A -= D
            E -= H
            
            #časovna zahtevnost 8*O(m//2 * n//2)
            #prostorska zahtevnost O(1) (spet vse na mestu)
            
            #računamo self[0:new_m, 0:new_n] = P6 + P5 + P4 - P2
            self[0:new_m, 0:new_n] += work[new_m:new_M, 0:new_n]
            self[0:new_m, 0:new_n] += work[0:new_m, new_n:new_N]
            self[0:new_m, 0:new_n] -= work[0:new_m, 0:new_n]
            
            #računamo self[new_m:new_M, new_n:new_N] = -P7 - P3 + P1 + P5
            self[new_m:new_M, new_n:new_N] -= self[new_m:new_M, 0:new_n]
            self[new_m:new_M, new_n:new_N] += self[0:new_m, new_n:new_N]
            self[new_m:new_M, new_n:new_N] += work[new_m:new_M, 0:new_n]
            
            #računamo self[0:new_m, new_n:new_N] = P1 + P2
            self[0:new_m, new_n:new_N] += work[0:new_m, 0:new_n]
            
            #računamo self[new_m:new_M, 0:new_n] = P3 + P4
            self[new_m:new_M, 0:new_n] += work[0:new_m, new_n:new_N]
            
            ##
            ##
            
            #razdelimo različne primere glede na to, ali so m, k in n sodi ali lihi
            
            if k % 2 == 0:
                #časovna zahtevnost 4*O(k//2 * n//2) + 2*O(n//2) (množenje + seštevanje)
                #prostorska zahtevnost O(1)
                if m % 2 == 1:
                    #računamo zadnjo vrstico
                    self[m-1, 0:new_n].multiply(left[m-1, 0:new_k], E, work[m-1, 0:new_n])
                    work[m-1, 0:new_n].multiply(left[m-1, new_k:new_K], G, work[m-1, new_n:new_N])
                    self[m-1, 0:new_n] += work[m-1, 0:new_n]
                    
                    self[m-1, new_n:new_N].multiply(left[m-1, 0:new_k], F, work[m-1, 0:new_n])
                    work[m-1, 0:new_n].multiply(left[m-1, new_k:new_K], H, work[m-1, new_n:new_N])
                    self[m-1, new_n:new_N] +=  work[m-1, 0:new_n]
                    
                if n % 2 == 1:
                    #računamo zadnji stolpec
                    self[0:new_m, n-1].multiply(A, right[0:new_k, n-1], work[0:new_m, n-1])
                    work[0:new_m, n-1].multiply(B, right[new_k:new_K, n-1], work[new_m:new_M, n-1])
                    self[0:new_m, n-1] += work[0:new_m, n-1]
                    
                    self[new_m:new_M, n-1].multiply(C, right[0:new_k, n-1], work[0:new_m, n-1])
                    work[0:new_m, n-1].multiply(D, right[new_k:new_K, n-1], work[new_m:new_M, n-1])
                    self[new_m:new_M, n-1] += work[0:new_m, n-1]
                
                #časovna zahtevnost 2*O(k//2) + O(1) (množenje + prištevanje enoelementne matrike)
                #prostorska zahtevnost O(1) (naredimo novo matriko, ki pa je dimenzije 1)
                if m % 2 == 1 and n % 2 == 1:
                    #računamo self[m-1,n-1]
                    self[m-1, n-1] = left[m-1, 0:new_k] * right[0:new_k, n-1]
                    self[m-1, n-1] += left[m-1, new_k:new_K] * right[new_k:new_K, n-1]
                    
            else:
                #ker je k lih, moramo blokom matrike self prišteti produkte zadnjega stolpca matrike left z zadnjo vrstico matrike right
                #časovna zahtevnost 8*O(m//2 * n//2) (množenje + seštevanje)
                #prostorska zahtevnost O(1)
                work[0:new_m, 0:new_n].multiply(left[0:new_m, k-1], right[k-1, 0:new_n], work[0:new_m, new_n:new_N])
                self[0:new_m, 0:new_n] += work[0:new_m, 0:new_n]
                
                work[0:new_m, 0:new_n].multiply(left[0:new_m, k-1], right[k-1, new_n:new_N], work[0:new_m, new_n:new_N])
                self[0:new_m, new_n:new_N] += work[0:new_m, 0:new_n]
                
                work[0:new_m, 0:new_n].multiply(left[new_m:new_M, k-1], right[k-1, 0:new_n], work[0:new_m, new_n:new_N])
                self[new_m:new_M, 0:new_n] += work[0:new_m, 0:new_n]
                
                work[0:new_m, 0:new_n].multiply(left[new_m:new_M, k-1], right[k-1, new_n:new_N], work[0:new_m, new_n:new_N])
                self[new_m:new_M, new_n:new_N] += work[0:new_m, 0:new_n]
                
                #časovna zahtevnost 8*O(k//2 * n//2) + 4*O(n//2) + 4*O(n//2) (množenje + seštevanje + for zanke)
                #prostorska zahtevnost O(1)
                if m % 2 == 1:
                    #računamo zadnjo vrstico
                    self[m-1, 0:new_n].multiply(left[m-1, 0:new_k], E, work[m-1, 0:new_n])
                    work[m-1, 0:new_n].multiply(left[m-1, new_k:new_K], G, work[m-1, new_n:new_N])
                    self[m-1, 0:new_n] += work[m-1, 0:new_n]
                    #ker je left[m-1, k-1] število, nam pa se ne da delati nove matrike, uporabimo kar preprosto for zanko
                    for i in range(new_n):
                        self[m-1, i] += left[m-1, k-1] * right[k-1, 0:new_n][0, i]
                    
                    self[m-1, new_n:new_N].multiply(left[m-1, 0:new_k], F, work[m-1, 0:new_n])
                    work[m-1, 0:new_n].multiply(left[m-1, new_k:new_K], H, work[m-1, new_n:new_N])
                    self[m-1, new_n:new_N] += work[m-1, 0:new_n]
                    for i in range(new_n):
                        self[m-1, i+new_n] += left[m-1, k-1] * right[k-1, new_n:new_N][0, i]
                
                if n % 2 == 1:
                    #računamo zadnji stolpec
                    self[0:new_m, n-1].multiply(A, right[0:new_k, n-1], work[0:new_m, n-1])
                    work[0:new_m, n-1].multiply(B, right[new_k:new_K, n-1], work[new_m:new_M, n-1])
                    self[0:new_m, n-1] += work[0:new_m, n-1]
                    for i in range(new_m):
                        self[i, n-1] += right[k-1, n-1] * left[0:new_m, k-1][i, 0]
                        
                    self[new_m:new_M, n-1].multiply(C, right[0:new_k, n-1], work[0:new_m, n-1])
                    work[0:new_m, n-1].multiply(D, right[new_k:new_K, n-1], work[new_m:new_M, n-1])
                    self[new_m:new_M, n-1] += work[0:new_m, n-1]
                    for i in range(new_m):
                        self[i+new_m, n-1] += right[k-1, n-1] * left[new_m:new_M, k-1][i, 0]
                
                #časovna zahtevnost 2*O(k//2) + O(1) (množenje + seštevanje)
                #prostorska zahtevnost O(1) (spet, naredimo matriko dimenzij 1)
                if m % 2 == 1 and n % 2 == 1:
                    #računamo self[m-1, n-1]
                    self[m-1, n-1] = left[m-1, 0:new_k] * right[0:new_k, n-1]
                    self[m-1, n-1] += left[m-1, new_k:new_K] * right[new_k:new_K, n-1]
                    self[m-1, n-1] += left[m-1, k-1] * right[k-1, n-1]
                    
                    
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
