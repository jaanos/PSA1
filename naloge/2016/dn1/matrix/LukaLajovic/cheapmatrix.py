# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """

    #izvede mnozenje te matrike z drugo
    #parameter nova je matrika ki se jo spremijna
    def dm(self,druga,nova=None):
        n=self.nrow()
        m=self.ncol()
        k=druga.nrow()
        l=druga.ncol()
        if nova==None:
            nova=self.nicelna_matrika(n,l)
        if m!=k:
            return "ni mogoce"
        elif m==1 or n==1 or k==1 or l==1:
            return self.slabo_mnozenje2(druga,nova)
        elif n%2==1:
            print("hucklberry finn")
            c1=self[:n-1,:m].dm(druga,nova[:m-1,:l])
            c2=self[n-1,:m].dm(druga,nova[m-1,:l])
            nova[:m-1,:l]=c1
            nova[m-1,:l]=c2
            return nova
        elif m%2==1:
            print("tom sawyer")
            c1=self[:n,:m-1].dm(druga[:k-1,:l],nova)
            c2=self[:n,m-1].dm(druga[k-1,:l],nova)
            return c1+c2
        elif l%2==1:
            print("indijanec joe")
            c1=self.dm(druga[:k,:l-1],nova[:m,:l-1])
            c2=self.dm(druga[:k,l-1],nova[:m,l-1])
            nova[:m,:l-1]=c1
            nova[:m,l-1]=c2
            return nova
        else:
            print("jim")
            mors=nova[:m//2,:l//2]
            a=self[:n//2,:m//2]
            b=self[:n//2,m//2:]
            c=self[n//2:,:m//2]
            d=self[n//2:,m//2:]
                
            e=druga[:k//2,:l//2]
            f=druga[:k//2,l//2:]
            g=druga[k//2:,:l//2]
            h=druga[k//2:,l//2:]


            #nova[:n//2,:l//2]=p4+p5+p6-p2
            #nova[:n//2,l//2:]=p1+p2
            #nova[n//2:,:l//2]=p3+p4
            #nova[n//2:,l//2:]=p1+p5-p3-p7
            
            p1=a.dm(f-h,mors)
            p2=(a+b).dm(h,mors)
            p3=(c+d).dm(e,mors)
            p4=d.dm(g-e,mors)
            p5=(a+d).dm(e+h,mors)
            p6=(b-d).dm(g+h,mors)
            p7=(a-c).dm(e+f,mors)

                
            #nova[:n//2,:l//2]=p4
            #nova[:n//2,:l//2]+=p5
            #nova[:n//2,:l//2]+=p6
            #nova[:n//2,:l//2]-=p4
            
            #nova[:n//2,l//2:]=p1
            #nova[:n//2,l//2:]+=p2
            
            #nova[n//2:,:l//2]=p3
            #nova[n//2:,:l//2]+=p4
            
            #nova[n//2:,l//2:]=p1
            #nova[n//2:,l//2:]+=p5
            #nova[n//2:,l//2:]-=p3
            #nova[n//2:,l//2:]-=p7

            nova[:n//2,:l//2]=p4+p5+p6-p2
            nova[:n//2,l//2:]=p1+p2
            nova[n//2:,:l//2]=p3+p4
            nova[n//2:,l//2:]=p1+p5-p3-p7
            
            return nova




    # izvede naivno mnozenje dveh matrik
    def slabo_mnozenje2(self,druga,nula):
        if self.ncol()!=druga.nrow():
            return "ni mogoce"
        else:
            vrstice1=self.nrow()
            stolpci1=self.ncol()
            vrstice2=druga.nrow()
            stolpci2=druga.ncol()
            for i in range(vrstice1):
                for j in range(stolpci2):
                    k=0
                    for x in range(stolpci1):                    
                        k+=self[i,x]*druga[x,j]
                    nula[i,j]=k
            return nula


    #slabo množenje 3 izvede slabo naivno množenje dveh matrik uporabil ga bom ko bom množil matrike ki imajo kakšno dimenzijo ena
    def slabo_mnozenje3(self,prva,druga,nula):
            vrstice1=prva.nrow()
            stolpci1=prva.ncol()
            vrstice2=druga.nrow()
            stolpci2=druga.ncol()
            for i in range(vrstice1):
                for j in range(stolpci2):
                    k=0
                    for x in range(stolpci1):                    
                        k+=prva[i,x]*druga[x,j]
                    nula[i,j]=k
            return nula     
            #c1=self[:n,:m-1].poceni_mnozenje(druga[:k-1,:l])
            #c2=self[:n,m-1].poceni_mnozenje(druga[k-1,:l])
    
    def multiply(self, left, right,delovna=None):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Kot neobvezen argument lahko podamo še delovno matriko.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        if delovna is None:
            delovna = self.__class__(nrow = self.nrow(), ncol = self.ncol())
        else:
            assert self.nrow() == delovna.nrow() and self.ncol() == delovna.ncol(), \
               "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"
        #raise NotImplementedError("Naredi sam!")
        #označimo stolpce in vrstice za lažjo pisavo
        n=left.nrow()
        m=left.ncol()
        k=right.nrow()
        l=right.ncol()        
        

        
        
        self[:n,:l]=left.dm(right,delovna)

            

            
v1=CheapMatrix([[1],[1]])

m1=CheapMatrix([[1,2,3],[1,2,3]])
m2=CheapMatrix([[1,1],[1,1],[1,1]])
m3=CheapMatrix([[1,1],[1,1]])
nula=CheapMatrix([[0]])
#print(m2*m3)
m4=CheapMatrix([[1,1]])
m5=CheapMatrix([[1,1],[1,1]])
#print(m4*m5)

m6=CheapMatrix([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
m7=CheapMatrix([[1,1],[1,1],[1,1],[1,1]])


iv1=CheapMatrix([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])

m5=CheapMatrix([[1,1,1],[1,1,1],[1,1,1]])
print(m5*m5)
