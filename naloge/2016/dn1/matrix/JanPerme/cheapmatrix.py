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
            #Tu delamo samo pointerje tako da je nasa prostorska zahtevnost vredu
            A=(left[0:(left.nrow()//2),0:(left.ncol()//2)])
            B=(left[0:(left.nrow()//2),(left.ncol()//2):(2*(left.ncol()//2))])
            C=(left[(left.nrow()//2):(2*(left.nrow()//2)),0:(left.ncol()//2)])
            D=(left[(left.nrow()//2):(2*(left.nrow()//2)),(left.ncol()//2):(2*(left.ncol()//2))])
            E=(right[0:(right.nrow()//2),0:(right.ncol()//2)])
            F=(right[0:(right.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))])
            G=(right[(right.nrow()//2):(2*(right.nrow()//2)),0:(right.ncol()//2)])
            H=(right[(right.nrow()//2):(2*(right.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))])
            #Naredimo se pointerje na dele zacetne matrike da ne prepisujemo daljse kode
            
            D_1=(self[0:(left.nrow()//2),0:(right.ncol()//2)])
            D_2=self[(left.nrow()//2):(2*(left.nrow()//2)),0:(right.ncol()//2)]
            D_3=self[0:(left.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))]
            D_4=self[(left.nrow()//2):(2*(left.nrow()//2)),(right.ncol()//2):(2*(right.ncol()//2))]
            #rabimo se del delovne matrike ustretne velikosti kjer bomo shranjevali stvari
            W_1=work[0:(left.nrow()//2),0:(right.ncol()//2)]
            #naredimo se del delovne matrike ki ga bomo dali naprej v rekurziji
            W_2=work[0:(left.nrow()//2),(right.ncol()//2):(2*(right.ncol()//2))]
            #P1 = A * (F-H)
            #P2 = (A + B)*H
            #P3 = (C + D)*E
            #P4 = D*(G - E)
            #P5 = (A + D)*(E + H)
            #P6 = (B - D)*(G + H)
            #P7 = (A - C)*(E + F)
            #P1
            F-=H
            W_1.multiply(A,F,W_2)
            F+=H
            D_3+=W_1
            D_4+=W_1
            W_1[:,:]=0
            #P2
            A+=B
            W_1.multiply(A,H,W_2)
            A-=B
            D_1-=W_1
            D_3+=W_1
            W_1[:,:]=0
            #P3
            C+=D
            W_1.multiply(C,E,W_2)
            C-=D
            D_2+=W_1
            D_4-=W_1
            W_1[:,:]=0
            #P4
            G-=E
            W_1.multiply(D,G,W_2)
            G+=E
            D_1+=W_1
            D_2+=W_1
            W_1[:,:]=0
            #P5
            A+=D
            E+=H
            W_1.multiply(A,E,W_2)
            A-=D
            E-=H
            D_1+=W_1
            D_4+=W_1
            W_1[:,:]=0
            #P6
            B-=D
            G+=H
            W_1.multiply(B,G,W_2)
            B+=D
            G-=H
            D_1+=W_1
            W_1[:,:]=0
            #P7
            A-=C
            E+=F
            W_1.multiply(A,E,W_2)
            A+=C
            E-=F
            D_4-=W_1
            W_1[:,:]=0
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

