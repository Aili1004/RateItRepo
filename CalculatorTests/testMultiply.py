# Unit test for calculator multiply function.

import unittest
from calculator import multiply


class TestMultiply(unittest.TestCase):

    def assertAssociativeMultiplyEquals(self, a, b, result):
	self.assertEquals(multiply(a, b), result)
	self.assertEquals(multiply(b, a), result)

    # Testing empty input
    def testEmpty(self):
	self.assertAssociativeMultiplyEquals("", 5, None)
        self.assertEquals(multiply("",""), None)

    # Testing positive integer input
    def testPositiveInteger(self):
        self.assertAssociativeMultiplyEquals(3, 5, 15)

    # Testing zero integer input
    def testZeroInteger(self):
	self.assertAssociativeMultiplyEquals(5, 0, 0)
        self.assertEquals(multiply(0, 0), 0)

    # Testing negative integer input
    def testNegativeInteger(self):
	self.assertAssociativeMultiplyEquals(-5, 2, -10)
        self.assertAssociativeMultiplyEquals(-5, -2, 10)

    # Testing positive float input
    def testPositiveFloat(self):
        self.assertAssociativeMultiplyEquals(3.2, 2.5, 8.0)
        self.assertAssociativeMultiplyEquals(3.2, 2, 6.4)

    # Testing zero float input
    def testZeroFloat(self):
	self.assertAssociativeMultiplyEquals(5.0, 0.0, 0.0)
        self.assertEquals(multiply(0.0, 0.0), 0.0)

    # Testing negative float input
    def testNegativeFloat(self):
	self.assertAssociativeMultiplyEquals(-5.1, 2, -10.2)
        self.assertAssociativeMultiplyEquals(-5.1, -2, 10.2)

    # Testing object input
    def testObject(self):
	self.assertRaises(TypeError, multiply, object(), 2)
	self.assertRaises(TypeError, multiply, 2, object())
	self.assertRaises(TypeError, multiply, object(), object())

if __name__ == "__main__":
    unittest.main()
