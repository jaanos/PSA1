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
        #Ce je leva ali desna matrika oblike 1 x n oz m x 1 je ne moremo vec deliti zato matriki preprosto zmnozimo
        if left.nrow()==1:
            for j in range(right.ncol()):
                for i in range(left.ncol()):
                    self[0,j]+=left[0,i]*right[i,j]
        elif right.ncol()==1:
            for i in range(left.nrow()):
                for k in range(left.ncol()):
                    self[i,0]+=left[i,k]*right[k,0]
        else:
            #tu nastavimo podmatrike A,B,C,...
            A=(left[0:(left.nrow()//2),0:(left.ncol()//2)])
            B=(left[0:(left.nrow()//2),(left.ncol()//2):(2*(left.ncol()//2))])
            C=(left[(left.nrow()//2):(2*(left.nrow()//2)),0:(left.ncol()//2)])
            D=(left[(left.nrow()//2):(2*(left.nrow()//2)),(left.ncol()//2):(2*(left.ncol()//2))])
            E=(right[0:(right.nrow()//2),0:(right.ncol()//2)])
            F=(right[0:(right.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))])
            G=(right[(right.nrow()//2):(2*(right.nrow()//2)),0:(right.ncol()//2)])
            H=(right[(right.nrow()//2):(2*(right.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))])
            #naredimo P1,P2,...
            P1 = A * (F-H)
            P2 = (A + B)*H
            P3 = (C + D)*E
            P4 = D*(G - E)
            P5 = (A + D)*(E + H)
            P6 = (B - D)*(G + H)
            P7 = (A - C)*(E + F)
            #v naso matriko zapisemo rezultat Strassenovega algoritma za kvadratno matriko. Ce je katera od zacetnih matrik lihih dimenzij ima nasa matrika se prazen stolpec in/ali vrstico
            self[0:(left.nrow()//2),0:(right.ncol()//2)]=P4 + P5 + P6 - P2
            self[(left.nrow()//2):(2*(left.nrow()//2)),0:(right.ncol()//2)]=P3 + P4
            self[0:(left.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))]=P1+P2
            self[(left.nrow()//2):(2*(left.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))]=P1 + P5 - P3 - P7
            #obravnavamo primer, ce ima leva matrika liho stevilo stolpcev(in seveda desna isto stevilo vrstic)
            if (left.ncol())%2==1:
                for i in range(2*(left.nrow()//2)): #2*(left.nrow()//2) da ne stejemo tistega zadnjega elementa na mestu(n,n) leve matrike 2-krat ce velja tudi (left.nrow()%2)==1:
                    for j in range(2*(right.ncol()//2)): # 2*(right.ncol()//2) da ne stejemo zadnjega stolpca desne matrike 2-krat ce velja tudi (right.ncol()%2)==1
                        self[i,j]+=left[i,left.ncol()-1]*right[right.nrow()-1,j]
            #obravnavamo primer, ce ima leva matrika liho stevilo vrstic
            if (left.nrow()%2)==1:
                for j in range(2*(right.ncol()//2)): # 2*(right.ncol()//2) da ne stejemo zadnjega stolpca desne matrike 2-krat ce velja tudi (right.ncol()%2)==1
                    for i in range(left.ncol()):
                        self[left.nrow()-1,j]+=left[left.nrow()-1,i]*right[i,j]
            #obravnavamo primer, ce ima desna matrika liho stevilo stolpcev
            if (right.ncol()%2)==1:
                for i in range(left.nrow()):
                    for j in range(left.ncol()):
                        self[i,right.ncol()-1]+=left[i,j]*right[j,right.ncol()-1]
                
        return self
