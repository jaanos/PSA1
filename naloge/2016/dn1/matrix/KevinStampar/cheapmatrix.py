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
        strassen(left,right,self,work)



def zmnozi(left,right,rezultat):
    """Naivno zmnozi dve matriki,rezultat zapise v matriko rezultat """
    i = 0
    while (i < left.nrow()):
        j = 0
        while (j < right.ncol()):
            v = 0
            rezultat[i, j] = 0 #nastavi element rezultat[i, j] na 0 (ne bi bilo potrebno, ce bi vedeli da je matrika work nicelna)
            while (v < right.nrow()): #elementu rezultat[i, j] pristevamo ustrezne produkte elementov matrik left in right, tako da nastane skalarni produkt
                rezultat[i,j] = rezultat[i,j] + left[i, v] * right[v, j]
                v = v + 1
            j = j + 1
        i = i + 1

def strassen(left,right,rezultat,work=None):
    """s strassenovim algoritmom izracuna mnozenje dveh matrik, rezultat shrani v rezultat,"""
    lv = left.nrow() #stevilo vrstic leve
    ls = left.ncol() #stevilo stolpcev leve  = stevilo vrstic desne
    ds = right.ncol()   #stevilo stolpcev desne
    if(work is None): #ce ne dobimo delavne matrike, si jo ustvarimo
        work = AbstractMatrix(None,lv,ds)
    if (any([lv == 1, ls == 1, ds == 1])):
        zmnozi(left, right,rezultat)  #ce je leva ali desna matrika ranga 1 naivno zmnozi levo in desno

    elif (lv % 2 == 0 and ls % 2 == 0 and ds % 2 == 0): #ce so vse stranice matrik deljive z 2 naredimo:
        #matriko left razdelimo na   [A11 A12]
        #                            [A21,A22]
        #pri tem ne porabimo nic, saj so to le rezine, ki ne zapravijo rama saj le kazejo na originalno matriko

        A11 = left[0:(lv / 2), 0:(ls / 2)]
        A12 = left[0:(lv / 2), (ls / 2):ls]
        A21 = left[(lv/2):lv, 0:(ls / 2)]
        A22 = left[(lv / 2):lv, (ls / 2):ls]
        #enako za matriko right
        B11 = right[0:(ls / 2), 0:(ds / 2)]
        B12 = right[0:(ls / 2), (ds / 2):ds]
        B21 = right[(ls / 2):ls, 0:(ds / 2)]
        B22 = right[(ls / 2):ls, (ds / 2):ds]


        #enako za matriko work

        W11 = work[0:(lv / 2), 0:(ds / 2)]
        W12 = work[0:(lv / 2), (ds / 2):ds]
        W21 = work[(lv / 2):lv, 0:(ds / 2)]
        W22 = work[(lv / 2):lv, (ds / 2):ds]

        work[0:work.nrow(), 0:work.ncol()] = 0
        #izracunamo M6 in M7, rezultata shranimo v W22 in W11
        strassen((A12 - A22) , (B21 + B22),W11,W12) #M7
        strassen((A21 - A11), (B11+B12),W22,  W21) #M6
        W12[0:W12.nrow(),0:W12.ncol()] = 0 #pobrisemo delovni del matrike
        W21[0:W12.nrow(),0:W12.ncol()] = 0
        rezultat +=work  #rezultatu pristejemo delovno matriko work = [[M7,0],[0,M6]]
        work[0:work.nrow(), 0:work.ncol()] = 0 #pobrisemo delovno matriko



        #izracunamo M3 in M4, rezultata shranimo v W12 in W11, racunamo pa v W22 in W21
        strassen((A22) , (B21 - B11),W11,W21) #M4
        strassen((A11), (B12 - B22),W12,  W22) #M3
        W21[0:W21.nrow(),0:W21.ncol()] = W11[0:W11.nrow(),0:W11.ncol()] #W21 nastavimo na W11
        W22[0:W22.nrow(),0:W22.ncol()] = W12[0:W12.nrow(),0:W12.ncol()] #W22 nastavimo na W12
        rezultat+=work  #rezultatu pristejemo delovno matriko work = [[M4,M3],[M4,M3]]
        work[0:work.nrow(), 0:work.ncol()] = 0 #pobrisemo delovno matriko

        #izracunamo M5 in M2, rezultata shranimo v W12 in W21, racunamo pa v W11 in W22
        strassen((A11 + A12),(B22),W12,W11) #M5
        strassen((A21 + A22), (B11),W21,  W22) #M2
        W11[0:W11.nrow(), 0:W11.ncol()] = (-1)*W12[0:W12.nrow(),0:W12.ncol()] #W11 nastimamo na -W12
        W22[0:W22.nrow(), 0:W22.ncol()] = (-1)*W21[0:W21.nrow(),0:W21.ncol()] #W22 nastimamo na -W11
        rezultat+=work #rezultatu pristejemo delovno matriko work = [[-M5,M5],[M2,-M2]]
        work[0:work.nrow(), 0:work.ncol()] = 0 #pobrisemo delovno matriko

        #izracunamo se M1 , rezultat shranimo v W11, racunamo pa v W12
        strassen((A11 + A22), (B11+B22), W11, W12) #M1
        W22[0:W11.nrow(), 0:W11.ncol()] = W11[0:W12.nrow(), 0:W12.ncol()] #W22 nastimamo na W11
        W21[0:W21.nrow(), 0:W21.ncol()] = 0 #W21 in W12 nastimamo na 0
        W12[0:W21.nrow(), 0:W21.ncol()] = 0
        rezultat+=work #rezultatu pristejemo delovno matriko work =  [[M1,0],[0,M1]]
        work[0:work.nrow(), 0:work.ncol()] = 0  # pobrisemo delovno matriko

        #tukaj koncamo, rezultat je sedaj enak vsoti [[M1,0],[0,M1]]+[[-M5,M5],[M2,-M2]]+[[M4,M3],[M4,M3]]+[[M7,0],[0,M6]]
        #Rezultat = [R11 R12]
        #           [R21 R22]
        #velja sledece:
        #R11 = M1+M4-M5+M7
        #R12 = M3+M5
        #R21 = M2+M4
        #R22 = M1-M2+M3+M6

    elif (lv % 2 == 1): #ce stevilo vrstic leve matrike ni deljivo z 2 naredimo:
        # matriko left razdelimo na   [A11]
        #                             [A21]
        #kjer je A21 enovrsticna matrika
        A1 = left[0:(lv - 1), 0:ls]
        A2 = left[(lv - 1):lv, 0:ls]
        #enako naredimo z matriko rezultat
        R1 = rezultat[0:lv-1, 0:ds]
        R2 = rezultat[lv-1:lv, 0:ds]
        #iz matrike work vzamemo zgornjo matriko(razdeljeno tako kot matriki A in , da bomo lahko v njej racunali
        #spodnjega dela ne rabimo, saj bomo mnozenje zadnje vrstice opravili kar v matriki rezultat, ker bomo mnozili naivno
        W1 = work[0:lv - 1, 0:ds]
        #zmnozimo matriki A1 in right, rezultat zapisemo v R1, delamo pa v W1
        strassen(A1 , right,R1,W1)
        #naivno zmnozimo matriki a1 in right, rezultat zapisemo v R2
        zmnozi(A2 , right,R2)

        work[0:work.nrow(), 0:work.ncol()] = 0  # pobrisemo delovno matriko

    elif (ls % 2 == 1):#ce stevilo levih stolpcev ni deljivo z 2 naredimo:
        # matriko right razdelimo na   [B1]
        #                              [B2]
        # kjer je B21 enovrsticna matrika
        # matriko left razdelimo na   [[A11],[A21]]
        # kjer je A21 enostolpcna matrika
        A1 = left[0:lv, 0:(ls - 1)]
        A2 = left[0:lv, (ls - 1):ls]
        B1 = right[0:(ls - 1), 0:ds]
        B2 = right[(ls - 1):ls, 0:ds]

        #zmnozimo matriki A1 in B1, za racunanje uporabljamo matriko work, rezultat pa zapisemo v rezultat
        strassen(A1,B1,rezultat,work)
        #naivno zmnozimo matriki A2 in B2, rezultat shranimo v work
        zmnozi(A2,B2,work)
        rezultat+=work #rezultatu pristejemo delovno matriko
        work[0:work.nrow(), 0:work.ncol()] = 0  #pocistimo delovno matriko


    elif (ds % 2 == 1):#ce stevilo desnih stolpcev ni deljivo z 2 naredimo:
        # matriko right razdelimo na   [B1]
        #                              [B2]
        #enako storimo za matriko rezultat
        B1 = right[0:ls, 0:(ds - 1)]
        B2 = right[0:ls, (ds - 1):ds]
        R1=rezultat[0:lv, 0:ds-1]
        R2 =rezultat[0:lv,ds-1:ds]
        # iz matrike work vzamemo zgornjo matriko(razdeljeno tako kot matriki A in , da bomo lahko v njej racunali
        # spodnjega dela ne rabimo, saj bomo mnozenje zadnje vrstice opravili kar v matriki rezultat, ker bomo mnozili naivno
        W1 = work[0:lv, 0:ds - 1]
        #zmnozimo matriki left in B1, rezultat zapisemo v R1 , za racunanje pa uporabljamo W1
        strassen(left,B1,R1,W1)
        #naivno zmnozimo matriki left in B2, rezultat zapisemo v R2
        zmnozi(left,B2,R2)
        work[0:work.nrow(), 0:work.ncol()] = 0  #pobrisemo delovno matriko