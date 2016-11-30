# -*- coding: utf-8 -*-

__author__ = "Filip Koprivec"

from .slowmatrix import SlowMatrix


class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """

    def multiply(self, left: "FastMatrix", right: "FastMatrix") -> "FastMatrix":
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
            "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
            "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"

        if left.nrow() == 1 or right.ncol() == 1:  # Corner case
            super(FastMatrix, self).multiply(left, right)  # Keep it explicit for sure
            return self

        n = left.nrow() // 2                                    # cost: const
        m = left.ncol() // 2                                    # cost: const
        k = right.ncol() // 2                                   # cost: const

        # For ease of complexity calculations assume: n = max(n,m,k)

        A11 = left[0:n, 0:m]                                    # cost: const
        A12 = left[0:n, m:2 * m]                                # cost: const
        A21 = left[n:2 * n, 0:m]                                # cost: const
        A22 = left[n:2 * n, m:2 * m]                            # cost: const

        B11 = right[0:m, 0:k]                                   # cost: const
        B12 = right[0:m, k:2 * k]                               # cost: const
        B21 = right[m:2 * m, 0:k]                               # cost: const
        B22 = right[m:2 * m, k:2 * k]                           # cost: const

        #                                                       # SUM = 11*const = const

        # From CLRS

        S1 = B12 - B22                                          # cost: m*k
        S2 = A11 + A12                                          # cost: n*m
        S3 = A21 + A22  # = S1'                                 # cost: n*m
        S4 = B21 - B11                                          # cost: m*k
        S5 = A11 + A22                                          # cost: n*m
        S6 = B11 + B22                                          # cost: m*k
        S7 = A12 - A22                                          # cost: n*m
        S8 = B21 + B22                                          # cost: m*k
        S9 = A11 - A21                                          # cost: n*m
        S10 = B11 + B12                                         # cost: m*k

        #                                                       # SUM = 5*m*(n+k) = 10*n**2 = n**2

        P1 = A11 * S1                                           # cost: recurse
        P2 = S2 * B22                                           # cost: recurse
        P3 = S3 * B11                                           # cost: recurse
        P4 = A22 * S4                                           # cost: recurse
        P5 = S5 * S6                                            # cost: recurse
        P6 = S7 * S8                                            # cost: recurse
        P7 = S9 * S10                                           # cost: recurse

        #                                                       # SUM = 7*recurse = 7*MasterTheorem(n/2)

        C11 = P5 + P4 - P2 + P6                                 # cost: 4*n*k
        C12 = P1 + P2                                           # cost: 2*n*k
        C21 = P3 + P4                                           # cost: 2*n*k
        C22 = P5 + P1 - P3 - P7                                 # cost: 4*n*k

        #                                                       # SUM = 12*n*k = n*k = n**2

        # Additional rows/columns

        add_right_left = False
        if left.ncol() % 2:  # right column in left matrix => bottom row in right matrix
            add_right_left = True
            A13 = left[0:n, 2 * m]
            A23 = left[n:2 * n, 2 * m]
            B31 = right[2 * m, 0:k]
            B32 = right[2 * m, k:2 * k]                         # SUM = 4*constant = constant
            C11 += A13 * B31
            C12 += A13 * B32
            C21 += A23 * B31
            C22 += A23 * B32
            #                                                   # SUM = 4*2*n*k = n*k = n**2

        add_right_right = False
        if right.ncol() % 2:  # right column in right matrix
            add_right_right = True
            B13 = right[0:m, 2*k]
            B23 = right[m:2*m, 2*k]                             # SUM = 2*constant = constant

            C13 = A11 * B13 + A12 * B23
            C23 = A21 * B13 + A22 * B23
            #                                                   # SUM = 2*(n*k + n*k + n*k) = 6*n*k = n**2

            if add_right_left:  # 2*m+1, full additional
                B33 = right[2*m, 2*k]
                C13 += A13 * B33
                C23 += A23 * B33                                # SUM = 2*(2*n*k) = n*k = n**2
            self[0:n, 2*k] = C13
            self[n:2*n, 2*k] = C23

        if left.nrow() % 2:  # bottom row in left matrix, will need to add row to self
            A31 = left[2 * n, 0:m]
            A32 = left[2 * n, m:2 * m]                          # SUM = 2*constant = constant

            C31 = A31 * B11 + A32 * B21
            C32 = A31 * B12 + A32 * B22
            #                                                   # SUM = 2*(n*k + n*k + n*k) = 6*n*k = n**2
            if add_right_left:
                A33 = left[2 * n, 2 * m]  # Should be 1*1 matrix
                C31 += A33 * B31
                C32 += A33 * B32                                # SUM = 2*2*m = n

            if add_right_right:
                C33 = A31 * B13 + A32 * B23                     # SUM = 2*m*k = m+n
                if add_right_left:
                    C33 += A33 * B33
                self[2*n, 2*k] = C33

            self[2 * n, 0:k] = C31
            self[2 * n, k:2 * k] = C32

        self[0:n, 0:k] = C11
        self[0:n, k:2 * k] = C12
        self[n:2 * n, 0:k] = C21
        self[n:2 * n, k:2 * k] = C22
        #                                                       # SUM = 4*const = const

        #                                                       # SUM =

        #                             # SUM = 7*MasterTheorem(n/2) + 22*n**2 + 15*const = 7*MasterTheorem(n/2) + O(n**2)

        # N = max(n/2,n/2,n/2)
        # T(N) = 7 * T(N/2) + O(N^2)
        # MasterTheorem -> T(N) = O(N^(log_2(7))) => T(N) =~ O(N^2.8074)

        return self
