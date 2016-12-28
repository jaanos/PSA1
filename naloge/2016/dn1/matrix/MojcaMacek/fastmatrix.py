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
        n=len(right[0])
        m=len(right)
        p=len(left)
        
        assert len(left[0]) == m, \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert len(self) == p and n == len(self[0]), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if n==1 or m==1 or p==1:
            return SlowMatrix.multiply(self,left,right)
        

        else:
            m1=m-m%2
            n1=n-n%2
            p1=p-p%2
        
            A=left[0:p1/2, 0:n1/2]
            B=left[0:p1/2, n1/2:n1]
            C=left[p1/2:p1, 0:n1/2]
            D=left[p1/2:p1, n1/2:n1]
            E=right[0:n1/2, 0:m1/2]
            F=right[0:n1/2, m1/2:m1]
            G=right[n1/2:n1, 0:m1/2]
            H=right[n1/2:n1, m1/2:m1]

            X=[([0, ] * (m1/2)), ]*(p1/2)

            P1=FastMatrix.multiply(AbstractMatrix(X, A, F-G))
            P2=FastMatrix.multiply(AbstractMatrix(X, A+B, H))
            P3=FastMatrix.multiply(AbstractMatrix(X, C+D, E))
            P4=FastMatrix.multiply(AbstractMatrix(X, D, G-E))
            P5=FastMatrix.multiply(AbstractMatrix(X, A+D, E+H))
            P6=FastMatrix.multiply(AbstractMatrix(X, B-D, G+H))
            P7=FastMatrix.multiply(AbstractMatrix(X, A-C, E+F))
            
            DM =[[P4+P5+P6-P2, P1+P2],[P3+P4, P1+P5-P3-P7]]#delovna matrika
            CM =[([0, ] * m), ]*p#ciljna matrika
            for i in range(0,p1):
                for j in range(0,m1):
                    #uredili bomo del, kjer smo uporabili Strassena
                    #vzeli bomo element (i,j) matrike DM in prišteli, kar manjka    
                    CM[i][j]=DM[i][j]+ right[n][j]*left[i][n]
            for j in range(m1,m):#zadnji stolpec, na roke
                for i in range(0,p):
                    x=0
                    for k in range(0,n):
                        x += right[k][m]*left[i][k]
                    CM[i][j]=x
            for i in range(p1,p):#zadnja vrstica, na roke
                for j in range(0,m):
                    x=0
                    for k in range(0,n):
                        x += left[p][k]*right[k][j]
                    CM[i][j]=x
            return CM
