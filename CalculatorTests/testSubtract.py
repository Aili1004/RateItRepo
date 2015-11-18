'''
Created on 24 Aug 2014

@author: Yan Zhu

'''

import unittest

class TestSubtract(unittest.TestCase):
        
        def testPositiveInteger(self):
                self.assertEqual(subtract( 0, 0), 0)
                self.assertEqual(subtract( 1, 0), 1)
                self.assertEqual(subtract( 3, 3), 0)
                self.assertEqual(subtract( 3, 2), 1)
                self.assertEqual(subtract( 2, 3), -1)

        def testNegativeInteger(self):
                self.assertEqual(subtract( -2, -3), 1)
                self.assertEqual(subtract( 3, -3), 6)
                self.assertEqual(subtract( -3, 0), -3)

        def testDecimal(self):
                self.assertEqual(round(subtract( 0.5, 0.5), 3), 0.000)
                self.assertEqual(round(subtract( 0.5, -0.3), 3), 0.800)
                self.assertEqual(round(subtract( -0.5, 0.3), 3), -0.800)
                self.assertEqual(round(subtract( 1, -0.5), 3), 1.500)
                self.assertEqual(round(subtract( -0.5, 1), 3), -1.500)

        def testEmptyInput(self):
                self.assertEqual(subtract( "" , 1), None)
                self.assertEqual(subtract( 1, ""), None)
                self.assertEqual(subtract( "", ""), None)

        def testBadInput(self):
                self.assertEqual(subtract( "s", 1), None)
                self.assertEqual(subtract( 1, "s"), None)
                self.assertEqual(subtract( "s", "s"), None)

if __name__ == "__main__":
	unittest.main()

	