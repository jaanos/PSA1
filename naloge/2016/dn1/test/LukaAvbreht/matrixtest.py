import unittest
from matrix.LukaAvbreht import SlowMatrix

class TestMatrix(unittest.TestCase):
    def test_multiply(self):
        a = SlowMatrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20]])
        b = SlowMatrix([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24]])
        c = a * b
        self.assertEqual(c, SlowMatrix([[130, 140, 150, 160, 170, 180], [290, 316, 342, 368, 394, 420], [450, 492, 534, 576, 618, 660], [610, 668, 726, 784, 842, 900], [770, 844, 918, 992, 1066, 1140]]))
        d = SlowMatrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        e = SlowMatrix([[1, 1], [1, 1], [1, 1], [1, 1]])
        f = d * e
        self.assertEqual(f, SlowMatrix([[4, 4], [4, 4], [4, 4], [4, 4], [4, 4], [4, 4]]))
        g =SlowMatrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        h =SlowMatrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        i = g*h
        self.assertEqual(i, SlowMatrix([[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4]]))

