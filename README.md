
## Fourier transform 

With fourier analysis we can break a signal up into simple periodic signals. The main goal of our project is redraw a picture using Fourier transform. We are inspired from this video : https://youtu.be/r6sGWTCMz2k?t=1000 .

The principle is as follows: we consider the drawing as a path defined by a periodic x and y signal and by using the Fourier transform we can calculate the sine and cosine  coefficients that give us the speed and size of connected circle that would imitate our drawing.

Our work is structured as follows : 

# Step 1: Image Manipulation ( Coding : Kamal Ayoubi )

We will create a class named Image that provides functions for extracting a path of coordinate from various image formats (png, jpg, etc.). This path forms the basis of the parametric functions that we will be approximating using Fourier series.

# Step 2 : Calculate Fourier Approximations ( Coding :  Otmane  Jabbar )

We will create a class named FourierSerie that provides functions for calculate the Fourier approximations of the extracted path and use coefficients from this approximation to determine the phase and amplitude of the circle needed for the final visualization. Then ensuring the degree of approximation, i.e.  make sure that the approximation is close to the original function (prevents the big swoops across the drawing to dominate the image).


# Step 3 : Create and animate the circle ( Coding : Stephane  Sadio)

We will create a class named Circles that provides functions for : 

   - Tracking radii and center of circle implied by  Fourier decomposition of given FourierSerie object.
   - Perform the  animation.
   - Adjusting the speed of the animation. 

##   The members of group 2  : 

   - Ayoubi	Kamal	kamal.ayoubi@etu.umontpellier.fr .
   - Jabbar	Otmane	otmane.jabbar@etu.umontpellier.fr .
   - Sadio	Stephane  stephane.sadio@etu.umontpellier.fr .
