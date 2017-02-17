# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """

    # v primeru če je kakšna vrstica ali stolpec dolg 1 vrne naivno množenje
    # v primeru če je kdo lih odreže en stolpec oziroma vrstico in posebaj ravna z njo in posebaj z ostankom
    # če je vse sodo se da razdeliti na 4 enake dele sepravi izvedemo strassenov algoritem
    
    def dobro_mnozenje(self,druga):
        n=self.nrow()
        m=self.ncol()
        k=druga.nrow()
        l=druga.ncol()
        nova=self.nicelna_matrika(n,l)
        if m!=k:
            return "ni mogoce"
        elif m==1 or n==1 or k==1 or l==1:
            return self.slabo_mnozenje(druga)
        elif n%2==1:
            c1=self[:n-1,:m].dobro_mnozenje(druga)
            c2=self[n-1,:m].dobro_mnozenje(druga)
            nova[:m-1,:l]=c1
            nova[m-1,:l]=c2
            return nova
        elif m%2==1:
            c1=self[:n,:m-1].dobro_mnozenje(druga[:k-1,:l])
            c2=self[:n,m-1].dobro_mnozenje(druga[k-1,:l])
            return c1+c2
        elif l%2==1:
            c1=self.dobro_mnozenje(druga[:k,:l-1])
            c2=self.dobro_mnozenje(druga[:k,l-1])
            nova[:m,:l-1]=c1
            nova[:m,l-1]=c2
            return nova
        else:
            a=self[:n//2,:m//2]
            b=self[:n//2,m//2:]
            c=self[n//2:,:m//2]
            d=self[n//2:,m//2:]
                
            e=druga[:k//2,:l//2]
            f=druga[:k//2,l//2:]
            g=druga[k//2:,:l//2]
            h=druga[k//2:,l//2:]

            p1=a.dobro_mnozenje(f-h)
            p2=(a+b).dobro_mnozenje(h)
            p3=(c+d).dobro_mnozenje(e)
            p4=d.dobro_mnozenje(g-e)
            p5=(a+d).dobro_mnozenje(e+h)
            p6=(b-d).dobro_mnozenje(g+h)
            p7=(a-c).dobro_mnozenje(e+f)

                
            nova[:n//2,:l//2]=p4+p5+p6-p2
            nova[:n//2,l//2:]=p1+p2
            nova[n//2:,:l//2]=p3+p4
            nova[n//2:,l//2:]=p1+p5-p3-p7
            return nova


    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        #raise NotImplementedError("Naredi sam!")
        self[:left.nrow(),:right.ncol()]=left.dobro_mnozenje(right)
