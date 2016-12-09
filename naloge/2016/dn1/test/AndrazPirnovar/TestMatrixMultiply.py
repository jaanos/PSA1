import unittest   #za testiranje delovanja mnozenja matrik

from matrix import AbstractMatrix
from matrix.AndrazPirnovar import SlowMatrix
from matrix.AndrazPirnovar import FastMatrix
from matrix.AndrazPirnovar import CheapMatrix

class TestMatrixMultiply(unittest.TestCase):

    def setUp(self):

        self.A1 = AbstractMatrix([[1,0,-2],
                                 [0,3,-1]])

        self.B1 = AbstractMatrix([[0,3],
                                 [-2,-1],
                                 [0,4]])

        self.AB1 = AbstractMatrix([[0,-5],
                                  [-6,-7]])

        self.BA1 = AbstractMatrix([[0,9,-3],
                                  [-2,-3,5],
                                  [0,12,-4]])

        self.C1 = AbstractMatrix([[1,3,5,7],
                                 [2,4,6,8],
                                 [5,8,5,0],
                                 [2,4,9,2]])

        self.I44 = AbstractMatrix([[1,0,0,0],
                                 [0,1,0,0],
                                 [0,0,1,0],
                                 [0,0,0,1]])

        self.A2 = AbstractMatrix([[-1,2,-3,4,-5],
                              [5,-4,3,-2,1],
                              [-6,7,-8,9,0],
                              [0,-9,8,-7,6],
                              [-1,3,-5,7,-9],
                              [9,-7,5,-3,1],
                              [-2,1,-4,3,-5]])

        self.B2 = AbstractMatrix([[1,2,3,4,5],
                                  [-1,1,1,-1,1],
                                  [-5,4,-3,2,-1],
                                  [2,-1,-3,1,2],
                                  [0,3,0,4,-2]])

        self.AB2 = AbstractMatrix([[20,-31,-4,-28,18],
                                   [-10,23,8,32,12],
                                   [45,-46,-14,-38,3],
                                   [-45,48,-12,42,-43],
                                   [35,-53,-6,-46,35],
                                   [-15,37,14,54,25],
                                   [23,-37,-2,-34,11]])

        self.I55 = AbstractMatrix([[1,0,0,0,0],
                                   [0,1,0,0,0],
                                   [0,0,1,0,0],
                                   [0,0,0,1,0],
                                   [0,0,0,0,1]])

        self.A3 = AbstractMatrix([[1,1,1,1],
                                  [1,1,1,1],
                                  [1,1,1,1],
                                  [1,1,1,1]])

        self.B3 = AbstractMatrix([[1,1,1,1],
                                  [1,1,1,1],
                                  [1,1,1,1],
                                  [1,1,1,1]])

        self.AB3 = AbstractMatrix([[4,4,4,4],
                                   [4,4,4,4],
                                   [4,4,4,4],
                                   [4,4,4,4]])




        self.testi = [(self.A1,self.B1,self.AB1),(self.B1,self.A1,self.BA1),(self.C1,self.I44,self.C1),
                      (self.I44,self.C1,self.C1),(self.A2,self.B2,self.AB2),(self.B2,self.I55,self.B2),
                      (self.A3,self.B3,self.AB3)]

    def testSlowMatrix(self):

        for matrike in self.testi:
            with self.subTest(matrike = matrike):
                self.assertEqual(SlowMatrix(matrike[0])*SlowMatrix(matrike[1]),SlowMatrix(matrike[2]))

    def testFastMatrix(self):

        for matrike in self.testi:
            with self.subTest(matrike = matrike):
                self.assertEqual(FastMatrix(matrike[0])*FastMatrix(matrike[1]),FastMatrix(matrike[2]))


