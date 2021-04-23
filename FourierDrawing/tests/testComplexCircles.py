
import sys
sys.path.append("..")
from Cirles_radii_center.ComplexCircles import ComplexCircles as C
import unittest

class TestComplexCircles:
    def setUp(self):
        self.C = Circles(FT,20,0,(0,0))

    def tearDown(self):
        self.C.num_circles(300)

    def test_Circles_is_instance_of_Circles(self):
        self.assertIsInstance(self.C, ComplexCircles)

if __name__=='__main__':
    unittest.main()

