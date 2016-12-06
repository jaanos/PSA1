# -*- coding: utf-8 -*-

__author__ = "Filip Koprivec"

from .slowmatrix import SlowMatrix


class CheapMatrix(SlowMatrix):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """
    Matrika s prostorsko nepotratnim množenjem.
    """
    def multiply(self, left: "CheapMatrix", right: "CheapMatrix", work: "CheapMatrix"=None) -> "CheapMatrix":
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

        if left.nrow() == 1 or right.ncol() == 1:  # Corner case
            super().multiply(left, right)  # no memory overhead (except for recursion)
            return self

        return self._multiply(left, right, work)

    def _multiply(self, left: "CheapMatrix", right: "CheapMatrix", work: "CheapMatrix") -> "CheapMatrix":
        """

        Idea: firstly make all seven multiplications (take care of additions for those), then assemble self back with
        help of work matrix (7 + 1 = 8 <= 2*(2*2)

        :param left: matrix A
        :param right: matrix B
        :param work: working matrix D, with same dimensions as self
        :return: self, filled with values of A*B
        """

        n = left.nrow() // 2                                    # cost: const
        m = left.ncol() // 2                                    # cost: const
        k = right.ncol() // 2                                   # cost: const

        A11 = left[0:n, 0:m]                                    # cost: const
        A12 = left[0:n, m:2 * m]                                # cost: const
        A21 = left[n:2 * n, 0:m]                                # cost: const
        A22 = left[n:2 * n, m:2 * m]                            # cost: const

        B11 = right[0:m, 0:k]                                   # cost: const
        B12 = right[0:m, k:2 * k]                               # cost: const
        B21 = right[m:2 * m, 0:k]                               # cost: const
        B22 = right[m:2 * m, k:2 * k]                           # cost: const

        C11 = self[0:n, 0:k]                                    # cost: const
        C12 = self[0:n, k:2 * k]                                # cost: const
        C21 = self[n:2 * n, 0:k]                                # cost: const
        C22 = self[n:2 * n, k:2 * k]                            # cost: const

        D11 = work[0:n, 0:k]                                    # cost: const
        D12 = work[0:n, k:2 * k]                                # cost: const
        D21 = work[n:2 * n, 0:k]                                # cost: const
        D22 = work[n:2 * n, k:2 * k]                            # cost: const

        # Calculate products
        # Idea: multiply matrix on Cij/Dij, with D22 as work matrix

        B12 -= B22  # change                                    # cost: n**2
        C12.multiply(A11, B12, D22)  # P1 = A(F-H)              # cost: recurse
        B12.unsafe_iadd(B22)  # clean                                     # cost: n**2

        A11.unsafe_iadd(A12)  # change                                    # cost: n**2
        D12 *= 0  # Init D12                                    # cost: n**2
        D12.multiply(A11, B22, D22)  # P2 = (A+B)H              # cost: recurse
        A11.unsafe_isub(A12)  # clean                                     # cost: n**2

        A21.unsafe_iadd(A22)  # change                                    # cost: n**2
        C21.multiply(A21, B11, D22)  # P3 = (C+D)E              # cost: recurse
        A21.unsafe_isub(A22)  # clean                                     # cost: n**2

        B21.unsafe_isub(B11)  # change                                    # cost: n**2
        D21 *= 0  # Init D12                                    # cost: n**2
        D21.multiply(A22, B21, D22)  # P4 = D(G-E)              # cost: recurse
        B21.unsafe_iadd(B11)  # clean                                     # cost: n**2

        A11.unsafe_iadd(A22)  # change                                    # cost: n**2
        B11.unsafe_iadd(B22)  # change                                    # cost: n**2
        D11 *= 0  # Init D12                                    # cost: n**2
        D11.multiply(A11, B11, D22)  # P5 = (A+D)(E+H)          # cost: recurse
        A11.unsafe_isub(A22)  # clean                                     # cost: n**2
        B11.unsafe_isub(B22)  # clean                                     # cost: n**2

        A12.unsafe_isub(A22)  # change                                    # cost: n**2
        B21.unsafe_iadd(B22)  # change                                    # cost: n**2
        C11.multiply(A12, B21, D22)  # P6 = (B-D)(G+H)          # cost: recurse
        A12.unsafe_iadd(A22)  # clean                                     # cost: n**2
        B21.unsafe_isub(B22)  # clean                                     # cost: n**2

        A11.unsafe_isub(A21)  # change                                    # cost: n**2
        B11.unsafe_iadd(B12)  # change                                    # cost: n**2
        C22.multiply(A11, B11, D22)  # P7 = (A-C)(E+F)          # cost: recurse
        A11.unsafe_iadd(A21)  # clean                                     # cost: n**2
        B11.unsafe_isub(B12)  # clean                                     # cost: n**2

        C22 *= -1  # -P7                                        # cost: n**2

        #                                                   # SUM = 7*recurse + O(n**2) = 7*MasterTheorem(n/2) + O(n**2)

        # Recalculate self

        C22.unsafe_isub(C21)  # P3                                        # cost: n**2
        C22.unsafe_iadd(D11)  # P5                                        # cost: n**2
        C22.unsafe_iadd(C12)  # P1                                        # cost: n**2

        C12.unsafe_iadd(D12)  # P2                                        # cost: n**2

        C21.unsafe_iadd(D21)  # P4                                        # cost: n**2

        C11.unsafe_iadd(D11)  # P5                                        # cost: n**2
        C11.unsafe_iadd(D21)  # P4                                        # cost: n**2
        C11.unsafe_isub(D12)  # P2                                        # cost: n**2

        # Fix non even matrix

        add_right_left = False
        if left.ncol() % 2:  # right column in left matrix => bottom row in right matrix
            add_right_left = True
            A13 = left[0:n, 2 * m]
            A23 = left[n:2 * n, 2 * m]
            B31 = right[2 * m, 0:k]
            B32 = right[2 * m, k:2 * k]                         # SUM = 4*constant = constant

            D12 *= 0  # Init D12
            D12.multiply(A13, B31, D22)
            C11.unsafe_iadd(D12)

            D12 *= 0
            D12.multiply(A13, B32, D22)
            C12.unsafe_iadd(D12)

            D12 *= 0
            D12.multiply(A23, B31, D22)
            C21.unsafe_iadd(D12)

            D12 *= 0
            D12.multiply(A23, B32, D22)
            C22.unsafe_iadd(D12)
            #                                                   # SUM = 4*3*n*k = n*k = n**2

        add_right_right = False
        if right.ncol() % 2:  # right column in right matrix
            add_right_right = True
            B13 = right[0:m, 2*k]
            B23 = right[m:2*m, 2*k]                             # SUM = 2*constant = constant

            C13 = self[0:n, 2*k]
            C23 = self[n:2*n, 2*k]

            D13 = work[0:n, 2*k]
            D23 = work[n:2 * n, 2 * k]

            D13 *= 0
            D13.multiply(A11, B13, D23)
            C13.unsafe_iadd(D13)

            D13 *= 0
            D13.multiply(A12, B23, D23)
            C13.unsafe_iadd(D13)

            D13 *= 0
            D13.multiply(A21, B13, D23)
            C23.unsafe_iadd(D13)
            D13 *= 0
            D13.multiply(A22, B23, D23)
            C23.unsafe_iadd(D13)

            #                                                   # SUM = 2*(n*k + n*k + n*k) = 6*n*k = n**2

            if add_right_left:  # 2*m+1, full additional
                B33 = CheapMatrix([[right[2*m, 2*k]]])

                D13 *= 0
                D13.multiply(A13, B33, D23)
                C13.unsafe_iadd(D13)

                D13 *= 0
                D13.multiply(A23, B33, D23)
                C23.unsafe_iadd(D13)                                      # SUM = 2*(3*n*k) = n*k = n**2

        if left.nrow() % 2:  # bottom row in left matrix, will need to add row to self
            A31 = left[2 * n, 0:m]
            A32 = left[2 * n, m:2 * m]                          # SUM = 2*constant = constant

            C31 = self[2 * n, 0:k]
            C32 = self[2 * n, k:2 * k]

            D31 = work[2 * n, 0:k]
            D32 = work[2 * n, k:2 * k]

            D31 *= 0
            D31.multiply(A31, B11, D32)
            C31.unsafe_iadd(D31)

            D31 *= 0
            D31.multiply(A32, B21, D32)
            C31.unsafe_iadd(D31)

            D32 *= 0
            D32.multiply(A31, B12, D31)
            C32.unsafe_iadd(D32)

            D32 *= 0
            D32.multiply(A32, B22, D31)
            C32.unsafe_iadd(D32)

            #                                                   # SUM  = n**2
            if add_right_left:
                A33 = CheapMatrix([[left[2 * n, 2 * m]]])  # Should be 1*1 matrix, no memory overhead
                C31.unsafe_iadd(A33 * B31)
                C32.unsafe_iadd(A33 * B32)                                # SUM = 2*2*m = n

            if add_right_right:
                C33 = A31 * B13 + A32 * B23                     # SUM = 2*m*k = n**2, memory: O(1)
                if add_right_left:
                    C33.unsafe_iadd(A33 * B33)                            # memory: O(1)
                self[2*n, 2*k] = C33

        # END

        #                                                            Without non even matrix fixing
        #                             # SUM = 7*MasterTheorem(n/2) + 32*n**2  = 7*MasterTheorem(n/2) + O(n**2)

        # N = max(n,m,k)
        # T(N) = 7 * T(N/2) + O(N^2)
        # MasterTheorem -> T(N) = O(N^(log_2(7))) => T(N) =~ O(N^2.8074)
        return self

    def unsafe_iadd(self, other: "CheapMatrix") -> "CheapMatrix":
        """
        Ker:

        `M += N` in `M -= N` matriki `M` prišteje oziroma odšteje matriko `N` (ne ustvari se nova matrika). Mogoče je tudi kombinirati s podmatrikami.

        ampak:

        __iadd__:

        Prištevanje k matriki.

        K trenutni matriki prišteje istoležne vrednosti podane matrike.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.



        :param other: other matrix
        :return: self + other
        """


        oi = other._rslice.start
        for r in self._data[self._rslice]:
            sj = self._cslice.start
            oj = other._cslice.start
            for j in range(self._ncol):
                r[sj] += other._data[oi][oj]
                sj += self._cslice.step
                oj += other._cslice.step
            oi += other._rslice.step
        return self

    def unsafe_isub(self, other: "CheapMatrix") -> "CheapMatrix":
        """
        Enak argument kot zgoraj...

        :param other:
        :return:
        """

        oi = other._rslice.start
        for r in self._data[self._rslice]:
            sj = self._cslice.start
            oj = other._cslice.start
            for j in range(self._ncol):
                r[sj] -= other._data[oi][oj]
                sj += self._cslice.step
                oj += other._cslice.step
            oi += other._rslice.step
        return self
