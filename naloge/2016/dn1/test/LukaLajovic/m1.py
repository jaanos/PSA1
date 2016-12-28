import matrix

import math


class matrika(matrix.AbstractMatrix):
    #pomnožiu te bom tako da bom jaz na desni drug pa na levi
    def slabo_mnozenje(self,druga):
        if self.ncol()!=druga.nrow():
            return "ni mogoce"
        else:
            vrstice1=self.nrow()
            stolpci1=self.ncol()
            vrstice2=druga.nrow()
            stolpci2=druga.ncol()
            nula=self.nicelna_matrika(vrstice1,stolpci2)
            for i in range(vrstice1):
                for j in range(stolpci2):
                    k=0
                    for x in range(stolpci1):                    
                        k+=self[i,x]*druga[x,j]
                    nula[i,j]=k
            return nula
    


    # delovalo bo samo za 2^nx2^n
    def dobro_mnozenje1(self,druga):                
            if self.ncol()==1:
                return self.slabo_mnozenje(druga)
            
            else:
                c=self.nicelna_matrika(self.ncol(),self.ncol())
                a11=self[:self.ncol()//2,:self.ncol()//2]
                a12=self[:self.ncol()//2,self.ncol()//2:]
                a21=self[self.ncol()//2:,:self.ncol()//2]
                a22=self[self.ncol()//2:,self.ncol()//2:]
                
                b11=druga[:self.ncol()//2,:self.ncol()//2]
                b12=druga[:self.ncol()//2,self.ncol()//2:]
                b21=druga[self.ncol()//2:,:self.ncol()//2]
                b22=druga[self.ncol()//2:,self.ncol()//2:]
                
                c[:self.ncol()//2,:self.ncol()//2]=a11.dobro_mnozenje1(b11)+a12.dobro_mnozenje1(b21)
                c[:self.ncol()//2,self.ncol()//2:]=a11.dobro_mnozenje1(b12)+a12.dobro_mnozenje1(b22)
                c[self.ncol()//2:,:self.ncol()//2]=a21.dobro_mnozenje1(b11)+a22.dobro_mnozenje1(b21)
                c[self.ncol()//2:,self.ncol()//2:]=a21.dobro_mnozenje1(b12)+a22.dobro_mnozenje1(b22)
                return c
                


    def dobro_mnozenje2(self,druga):
        n=self.nrow()
        m=self.ncol()
        k=druga.nrow()
        l=druga.ncol()
        nova=self.nicelna_matrika(m,l)
        if m!=k:
            print("slaba")
            return "ni mogoce"
        elif m==1 or n==1 or k==1 or l==1:
            return self.slabo_mnozenje(druga)
        elif n%2==1:
            print("slo je")
            c1=self[:n-1,:m].dobro_mnozenje2(druga)
            c2=self[n-1,:m].dobro_mnozenje2(druga)
            nova[:m-1,:l]=c1
            nova[m-1,:l]=c2
            return nova
        elif m%2==1:
            print("slo je2")
            c1=self[:n,:m-1].dobro_mnozenje2(druga[:k-1,:l])
            c2=self[:n,m-1].dobro_mnozenje2(druga[k-1,:l])
            return c1+c2
        elif l%2==1:
            print("slo je3")
            c1=self.dobro_mnozenje2(druga[:k,:l-1])
            print("slo je 4")
            c2=self.dobro_mnozenje2(druga[:k,l-1])
            nova[:m,:l-1]=c1
            nova[:m,l-1]=c2
            return nova
        else:
            print("riba raca rak")
            a=self[:n//2,:m//2]
            b=self[:n//2,m//2:]
            c=self[n//2:,:m//2]
            d=self[n//2:,m//2:]
                
            e=druga[:k//2,:l//2]
            f=druga[:k//2,l//2:]
            g=druga[k//2:,:l//2]
            h=druga[k//2:,l//2:]

            p1=a.dobro_mnozenje2(f-h)
            p2=(a+b).dobro_mnozenje2(h)
            p3=(c+d).dobro_mnozenje2(e)
            p4=d.dobro_mnozenje2(g-e)
            p5=(a+d).dobro_mnozenje2(e+h)
            p6=(b-d).dobro_mnozenje2(g+h)
            p7=(a-c).dobro_mnozenje2(e+f)

                
            nova[:n//2,:l//2]=p4+p5+p6-p2
            nova[:n//2,l//2:]=p1+p2
            nova[n//2:,:l//2]=p3+p4
            nova[n//2:,l//2:]=p1+p5-p3-p7
            return nova
            
            
            

                    
    def k(self):
        return self.dobro_mnozenje2(self)-self.slabo_mnozenje(self)
                    
    def kvadrat(self):
        return self.dobro_mnozenje2(self)
            
            
    def multiply(self,druga):
        if self.nrow()!=druga.ncol():
            return "napačne matrike"

                
    def nicelna_matrika(self,a,b):
        c=b*[0]
        d=[c for i in range(a)]
        return matrika(d,a,b)
        
    
r1=[[1,0,1],[2,1,3],[1,1,1]]
r2=[[2,1,0],[0,0,2],[1,0,1]]
r3=[[1,0],[3,3]]
m1=matrika(r1,3,3)
m2=matrika(r2,3,3)
m3=matrika(r3,2,2)
r4=[[1,1,1],[1,1,1]]
r5=[[1,1],[1,1],[1,1]]
m4=matrika(r4,2,3)
m5=matrika(r5,3,2)
r6=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
m6=matrika(r6,4,4)
r7=[[4,1,0,0],[0,4,1,0],[0,0,4,1],[0,0,0,4]]
m7=matrika(r7,4,4)

r8=[[1,1],[1,1],[1,1]]
m8=matrika(r8,3,2)
r9=[[1],[1],[1]]
m9=matrika(r9,3,1)


r10=[[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
m10=matrika(r10,4,3)
r11=[[4,1,0,0,0],[0,4,1,0,0],[0,0,4,1,0],[0,0,0,4,1],[0,0,0,0,4]]
m11=matrika(r11,5,5)
r12=[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
m12=matrika(r12,5,3)

r13=[[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
m13=matrika(r13,4,3)

r14=[[1,1],[1,1],[1,1],[1,1]]
m14=matrika(r14,4,2)
r15=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
m15=matrika(r15,5,5)

r16=[[1],[-1],[0],[0],[0]]
m16=matrika(r16,5,1)

r17=[[1,1,-1,-1,0],[1,1,-1,-1,0],[1,1,-1,-1,0],[1,1,-1,-1,0],[1,1,-1,-1,0]]
m17=matrika(r17,5,5)

