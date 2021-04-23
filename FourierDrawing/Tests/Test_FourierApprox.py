import sys
sys.path.append("..")
from ImageManipulation.Imgmanip import Imagemanip
from FourierApproximation.Class_fourierApproximation import FourierApprox
import unittest


url = 'https://www.seekpng.com/png/detail/116-1164659_line-drawing-bunny-rabbit-at-getdrawings-bunny-drawing.png'
Img = Imagemanip(url)
Img.single_color()
Img.convert_binary(scale=3, thresh_val=200)
Img.black_and_white()
Img.distance_matrix()
Img.contours_search()
Img.get_splines()


class TestFourierApprox(unittest.TestCase):
    def test_FourierApprox_is_instance_of_FourierApprox(self):
        """ Assert that the Fourier object is created """
        xFT =  FourierApprox(Img.x_spl, (0, Img.length_pixels), num_circles= 50)
        self.assertIsInstance(xFT, FourierApprox)


    def test_origin_offset_is_float(self):
        """ Assert that the attribute origin_offset of the FourierApprox object is a float """
        xFT =  FourierApprox(Img.x_spl, (0, Img.length_pixels), num_circles= 50)
        self.assertIsInstance(xFT.origin_offset, float)
    

    def test_circles_approximation_offset_is_float(self):
        """ Assert that the attribute circles_approximation_offset of the FourierApprox object is a float """
        xFT =  FourierApprox(Img.x_spl, (0, Img.length_pixels), num_circles= 50)
        self.assertIsInstance(xFT.circles_approximation_offset, float)

    def test_Fourier_Coefs_are_complex(self):
        """ Assert that the attribute coefs of the FourierApprox object are complex """
        xFT =  FourierApprox(Img.x_spl, (0, Img.length_pixels), num_circles= 50)
        for i in range(1, 500):
            self.assertIsInstance(xFT.coefs[i], complex)


if __name__=='__main__' : 
    unittest.main() 



    
    

    

        
        
        
        
        
        
        
        
         




