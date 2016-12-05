import unittest   #za testiranje delovanja mnozenja matrik

from matrix import AbstractMatrix
from matrix.AndrazPirnovar.slowmatrix import SlowMatrix
from matrix.AndrazPirnovar.fastmatrix import FastMatrix
from matrix.AndrazPirnovar.cheapmatrix import CheapMatrix

class TestMatrixMultiply(unittest.TestCase):

    def setUp(self):

        self.A = AbstractMatrix([[1,0,-2],
                                 [0,3,-1]])

        self.B = AbstractMatrix([[0,3],
                                 [-2,-1],
                                 [0,4]])

        self.AB = AbstractMatrix([[0,-5],
                                  [-6,-7]])

        self.BA = AbstractMatrix([[0,9,-3],
                                  [-2,-3,5],
                                  [0,12,-4]])

        self.C = AbstractMatrix([[1,3,5,7],
                                 [2,4,6,8],
                                 [5,8,5,0],
                                 [2,4,9,2]])

        self.I = AbstractMatrix([[1,0,0,0],
                                 [0,1,0,0],
                                 [0,0,1,0],
                                 [0,0,0,1]])


        self.testi = [(self.A,self.B,self.AB),(self.B,self.A,self.BA),(self.C,self.I,self.C),(self.I,self.C,self.C)]

    def testSlowMatrix(self):

        for matrike in self.testi:
            with self.subTest(matrike = matrike):
                self.assertEqual(SlowMatrix(matrike[0])*SlowMatrix(matrike[1]),SlowMatrix(matrike[2]))


