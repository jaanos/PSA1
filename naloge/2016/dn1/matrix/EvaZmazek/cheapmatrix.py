
# -*- coding: utf-8 -*-
from .slowmatrix import SlowMatrix

class CheapMatrix(SlowMatrix):
    """
    Matrika s prostorsko nepotratnim množenjem.
    """

    # za študiranje časovne in prostorske zahtevnosti
    # si označimo:
    #
    # n...število vrstic leve matrike
    # k...število stolpcev leve matrike, ki je enako številu vrstic desne matrike
    # m...število stolpcev desne matrike
    #
    # T(n,k,m) ... časovna zahtevnost
    # P(n,k,m) ... prostorska zahtevnos

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
            work = self.__class__(nrow=self.nrow(), ncol=self.ncol())
        else:
            assert self.nrow() == work.nrow() and self.ncol() == work.ncol(), \
                "Dimenzije delovne matrike ne ustrezajo dimenzijam produkta!"

        stStolpcevLeveMatrike = left.ncol()  # izračunamo šrevilo stolpcev leve matrike, ki mora biti enako številu vrstic desne matike, da je množenje sploh definirano
        stVrsticLeveMatrike = left.nrow()  # izračunamo število vrstic leve matrike, ki je enako številu vrstic v novi matiki, ki je produkt leve in desne matrike
        stStolpcevDesneMatrike = right.ncol()  # izračunamo število stolpcev desne matrike, ki je enako število stolpcev v novi matriki, ki je produktleve in desne matrike

        # na začetku si shranimo 3 vrednosti: P(n,k,m) = O(3) = O(1)
        # na začetku naredimo tri štetja: T(n,k,m) = O(3) = O(1)

        # tako kot v SlowMatrix, tudi v primerih, ko je ena od dimenzij stStolpcevLeveMatike, stVrsticLeveMatrike in stStolpcevDesne matrike enaka 1, izracunamo matriko na roke
        if stStolpcevLeveMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                for j in range(stStolpcevDesneMatrike):
                    self[i, j] = (left[i, 0] * right[0, j])
            return self
        if stVrsticLeveMatrike == 1:
            for j in range(stStolpcevDesneMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[0, k] * right[k, j]
                self[0, j] = vrednost
            return self
        if stStolpcevDesneMatrike == 1:
            for i in range(stVrsticLeveMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[i, k] * right[k, 0]
                self[i, 0] = vrednost
            return self

        # v teh treh primerih sta tako časovna, kot tudi prostorska zahtevnost enaki, kot v metodi SlowMatrix

        # lotimo se sedaj matrik vecjih dimenzij

        # za časovno in prostorsko zahtevnost pogledamo najslabši možen primer, ki je pri nas ta, da so vse dimenzije matrik lihe

        # najprej poglejmo mnozenje matrik, katerih dimenzije so sode:

        if stStolpcevLeveMatrike % 2 == 0 and stVrsticLeveMatrike % 2 == 0 and stStolpcevDesneMatrike % 2 == 0:

            #najprej si naredimo pointerje, ki vzamejo O(1) dodatnega prostora

            #cetrine leve matrike
            A = left[0:stVrsticLeveMatrike // 2, 0:stStolpcevLeveMatrike // 2]
            B = left[0:stVrsticLeveMatrike // 2, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]
            C = left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, 0:stStolpcevLeveMatrike // 2]
            D = left[stVrsticLeveMatrike // 2:stVrsticLeveMatrike, stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike]

            #cetrine desne matrike
            E = right[0:stStolpcevLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2]
            F = right[0:stStolpcevLeveMatrike // 2, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike]
            G = right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, 0:stStolpcevDesneMatrike // 2]
            H = right[stStolpcevLeveMatrike // 2:stStolpcevLeveMatrike, stStolpcevDesneMatrike // 2:stStolpcevDesneMatrike]

            #cetrtine delovne matrike
            D1 = work[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2]
            D2 = work[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]
            D3 = work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2]
            D4 = work[stVrsticLeveMatrike // 2: stVrsticLeveMatrike,stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]

            #tudi self matriko si razdelimo na cetrtine. Pri tem je
            S1 = self[0:stVrsticLeveMatrike // 2, 0:stStolpcevDesneMatrike // 2]
            S2 = self[0:stVrsticLeveMatrike // 2, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]
            S3 = self[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, 0:stStolpcevDesneMatrike // 2]
            S4 = self[stVrsticLeveMatrike // 2: stVrsticLeveMatrike, stStolpcevDesneMatrike // 2: stStolpcevDesneMatrike]

            F -= H
            S2.multiply(A,F,D1)
            #v zgornjo desno cetrtino koncne matrike S2 vpisemo P1 = A  * (F - H)
            F += H

            #v tem koraku naredimo eno rekurzivno množenje ter eno odštevanje (prištevanje nasprotnih vrednosti) in eno prištevanje, za kar porabimo
            #T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(k//2 * m//2)=O(k//2 * m//2) dodatnega časa za odštevanje ter seštevanje
            #P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za odštevanje in seštevanje

            A += D
            E += H
            S1.multiply(A,E,D2)
            #v zgorno levo cetrtino koncne matrike S1 vpisemo P5 = (A + D) * (E + H)
            A -= D
            E -= H

            # v tem koraku naredimo eno rekurzivno množenje ter dve seštevanji in dve odstevanji, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(n//2 * k//2) + 2*O(k//2 * m//2) = 2*O((n+m)//2 * k//2) = O((n+m)//2 * k//2) dodatnega časa za seštevanje in odstevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za seštevanje in odstevanje

            C += D
            S3.multiply(C,E,D3)
            #v spodnjo levo cetrtino koncne matrike S3 vpisemo P3 = (C + D) * E
            C -= D

            # v tem koraku naredimo eno rekurzivno množenje ter eno seštevanje in eno odstevanje, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(n//2 * k//2)=O(n//2 * k//2) dodatnega časa za seštevanje in odstevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za seštevanje in odstevanje

            A -= C
            E += F
            S4.multiply(A,E,D4)
            #v spodnjo desno cetrtino koncne matrike S4 vpisemo P7 = (A - C ) * (E + F)
            A += C
            E -= F

            # v tem koraku naredimo eno rekurzivno množenje ter dve seštevanji in dve odštevanji, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(n//2 * k//2) + 2*O(k//2 * m//2) = 2*O((n+m)//2 * k//2)= O((n+m)//2 * k//2) dodatnega časa za seštevanje in odštevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za seštevanje in odštevanje

            S4 *= (-1)
            S4 += S2
            S4 += S1
            S4 -= S3
            #s temi koraki spodnjo desno cetrtino koncne matrike nastavimo na -P7 + P1 + P5 - P3.

            #v tem koraku naredimo 3 seštevanja in dve mnozenji z (-1), za kar porabimo
            #5*O(n//2 * m//2) = O(n//2 * m//2) dodatnega časa
            #nič dodatnega prostora

            A += B
            D1.multiply(A,H,D2)
            #v spodnjo desno cetrtino delovne matrike si torej zapisemo P2 = (A + B ) * H
            A -= B

            # v tem koraku naredimo eno rekurzivno množenje ter eno seštevanje in eno odstevanje, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2* O(n//2 * k//2) = O(n//2 * k//2) dodatnega časa za seštevanje in odstevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za seštevanje

            S2 += D1
            #s tem korakom zgornjo desno cetrtino koncne matrike nastavimo na P1 + P2.

            # v tem koraku naredimo 1 seštevanje, za katero porabimo
            # O(n//2 * m//2) dodatnega časa
            # nič dodatnega prostora

            G -= E
            D2.multiply(D,G,D3)
            #zgornjo levo cetrtino delovne matrike nastavimo na P4 = D * (G - E)
            G +=E

            # v tem koraku naredimo eno rekurzivno množenje ter eno odštevanje in eno odstevanje, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(k//2 * m//2) = O(k//2 * m//2) dodatnega časa za odštevanje in pristevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za odstevanje in sestevanje

            S3 += D2
            #s tem korakom smo spodnjo levo cetrtino koncne matrike nastavili na P3 + P4.

            # v tem koraku naredimo eno seštevanje, za katero porabimo
            # O(n//2 * m//2) dodatnega časa
            # nič dodatnega prostora

            B -= D
            G += H
            D3.multiply(B,G,D4)
            #spodnjo levo cetrtino delovne matrike nastavimo na P6 = (B - D) * (G + H)
            B += D
            G -= H

            # v tem koraku naredimo eno rekurzivno množenje ter dve seštevanji in dve odstevanji, za kar porabimo
            # T(n//2,k//2,m//2) dodatnega časa za rekurzivno množenje in 2*O(n//2 * k//2) + 2*O(k//2 * m//2) = 2*O((n+m)//2 * k//2) = O((n+m)//2 * k//2) dodatnega časa za seštevanje in odstevanje
            # P(n//2,k//2,m//2) dodanega prostora za rekurzivno množenje in nič dodatnega prostora za seštevanje in odstevanje

            S1 -= D1
            S1 += D2
            S1 += D3
            #s tem korakom smo zgornjo desno cetrtino koncne matrike nastavili na P4 + P5 + P6 - P2

            # v tem koraku naredimo 3 seštevanja, za kar porabimo
            # 3*O(n//2 * m//2) = O(n//2 * m//2) dodatnega časa
            # nič dodatnega prostora

            return self

        if stVrsticLeveMatrike % 2 == 1:
            self[0:stVrsticLeveMatrike - 1, :].multiply(left[0:stVrsticLeveMatrike - 1, :], right, work[0:stVrsticLeveMatrike - 1, :])
            for j in range(stStolpcevDesneMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[stVrsticLeveMatrike - 1:stVrsticLeveMatrike, k] * right[k, j]
                self[stVrsticLeveMatrike - 1:stVrsticLeveMatrike, j] = vrednost
            #self[stVrsticLeveMatrike - 1:stVrsticLeveMatrike, :] = left[stVrsticLeveMatrike - 1:stVrsticLeveMatrike,:] * right #ujame se v drugi if v algoritmu, zato to ok
            return self

        # v tem koraku porabimo O(k*m) dodatnega časa
        # v tem koraku porabimo O(1) dodatnega prostora

        if stStolpcevDesneMatrike % 2 == 1:
            self[:, 0:stStolpcevDesneMatrike - 1].multiply(left,right[:, 0:stStolpcevDesneMatrike - 1], work[:, 0:stStolpcevDesneMatrike - 1])
            for i in range(stVrsticLeveMatrike):
                vrednost = 0
                for k in range(stStolpcevLeveMatrike):
                    vrednost += left[i, k] * right[k, stStolpcevDesneMatrike - 1]
                self[i, stStolpcevDesneMatrike - 1] = vrednost
            #self[:, stStolpcevDesneMatrike - 1] = left * right[:, stStolpcevDesneMatrike - 1] #ujame se v tretji if v algoritmu, zato to ok
            return self

        # v tem koraku porabimo O(n*k) dodatnega časa
        # v tem koraku porabimo O(1) dodatnega prostora

        else:
            self[:, :].multiply(left[:, 0:stStolpcevLeveMatrike - 1],right[0:stStolpcevLeveMatrike - 1, :], work)
            for i in range(stVrsticLeveMatrike):
                for j in range(stStolpcevDesneMatrike):
                    self[i, j] += (left[i, stStolpcevLeveMatrike - 1] * right[stStolpcevLeveMatrike - 1, j])
            #self[:, :] += left[:,stStolpcevLeveMatrike - 1] *right[stStolpcevLeveMatrike - 1,:] #ujame se v prvi if, v algoritmu, zato self ni problem in je to ok
            return self

        # v tem koraku porabimo O(m*n) dodatnega časa
        # v tem koraku ne porabimo nobenega dodatnega prostora

            # Sklep:
            # Časovna zahtevnost: T(n,k,m) = O(1) + 7*T(n//2,k//2,m//2) + O(k//2 * m//2) + O((n+m)//2 * k//2) +
            # O(n//2 * k//2) + O((n+m)//2 * k//2) + O(n//2 * m//2) + O(n*k) + O(k*m) + O(m*n) + O(n//2 * k//2) +
            # O(n//2 * m//2) + O(k//2 * m//2) + O(n//2 * m//2) + O((n+m)//2 * k//2) + O(n//2 * m//2) =
            # = O(1) + 7*T(n//2,k//2,m//2) + 5*O((n+m)//2 * k//2)+ 4*O(n//2 * m//2)+ O(n*k) + O(k*m) + O(m*n)
            # =O(1) + 7*T(n//2,k//2,m//2) + O((n+m)//2 * k//2) + O(n//2 * m//2)+ O(n*k) + O(k*m) + O(m*n)
            # Prostorska zahtevnost: P(n,k,m) = 7*P(n//2,k//2,m//2) + O(1)