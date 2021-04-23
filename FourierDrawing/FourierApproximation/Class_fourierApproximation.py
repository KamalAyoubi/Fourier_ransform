import numpy as np
from copy import deepcopy

### Class FourierApprox 
class FourierApprox:
    """
    This Class will calculate the complex Fourier coefficients for a given function
    """
    def __init__(self,
            fxn,  # Function to be transformed (as Python function object)
             # Note: y is parameterized by its own index
             # 13th value in array = value of function at t=12
            rnge, # (.,.) tuple of range at which to evaluate fxn
            N=500,  # Number of coefficients to calculate
            period=None,  # If different than full length of function
            num_points=1000, # Number of points at which to evalute function
            num_circles=50 # This is needed to calculate proper offsets
        ):
        """
        Create the variables associated with the class

        :type fxn:  scipy.interpolate.fitpack2.UnivariateSpline
        :param fxn: Function to be transformed

        :type rnge: tuple
        :param rnge : the range at which to evaluate fxn

        :type N: int, default = 500 
        :param N : Number of coefficients to calculate

        :type period: int, default = None 
        :param N : the period, if the period == None then it is equal to the entire length of the function 

        :type num_points: int, default = 1000
        :param num_points : Number of points at which to evalute function

        :type num_circles : int, default = 50
        :param num_circles : Number of cercles that will be used 
        """
        
        #assert isinstance(fxn , scipy.interpolate.fitpack2.UnivariateSpline) ' Attribute fxn: should be scipy.interpolate.fitpack2.UnivariateSpline '
        #assert isinstance(rnge, tuple) ' Attribute rnge: should be a tuple  '
        #assert isinstance(N, int) ' Attribute N : should be an integer  '
        #assert isinstance(period, int) ' Attribute period: should be an integer  '
        #assert isinstance(num_points, int)  ' Attribute num_points: should be an integer '
        #assert isinstance(num_circles, int)  ' Attribute num_circles: should be an integer'
        


        self.num_circles = num_circles


        t_vals = list()
        y = list()
        for i in np.linspace(rnge[0], rnge[1]-1, num_points):
            t_vals.append(i)
            y.append(fxn(i))

        #t_vals, y = zip(*[(v, fxn(v)) for v in np.linspace(rnge[0], rnge[1]-1, num_points)])
        t_vals = np.array(t_vals)        
        self.t_vals = t_vals
        
       

        # Save the original coords when plotting
        y = np.array(y)
        y = y - y[0]
        self.fxn_vals = np.array(deepcopy(y))
        
        # Spline function doesn't make endpoints exactly equal
        # This sets the first and last points to their average
        endpoint = np.mean([y[0], y[-1]])
        y[0] = endpoint
        y[-1] = endpoint
        
        # Transform works best around edges when function starts at zero
        # (Can't figure out how to avoid Gibbs-type phenomenon when 
        #  intercept !=0 )
        y = y - y[0]
        
        self.N = N

        if period==None:
            period = rnge[1]
        self.period = period
            
        def cn(n):
            c = y*np.exp(-1j*2*n*np.pi*t_vals/period)
            return(c.sum()/c.size)

        #coefs = [cn(i) for i in range(1,N+1)]
        coefs = list()
        for i in range(1,N+1):
            coefs.append(cn(i))


        self.coefs = coefs
        self.real_coefs = [c.real for c in self.coefs]
        self.imag_coefs = [c.imag for c in self.coefs]
        
        self.amplitudes = np.absolute(self.coefs)
        self.phases = np.angle(self.coefs)
        
        
        def f(x, order=N):
            # Evaluate the function y at time t using Fourier approximiation of order N
            f = list()
            for i in range(1,order+1):
                f.append(2*coefs[i-1]*np.exp(1j*2*i*np.pi*x/period))
                return(np.array(f).sum())
        
         # Evaluate function at all specified points in t domain
        fourier_approximation = np.array([f(t, order=N).real for t in t_vals])
        circles_approximation = np.array([f(t, order=self.num_circles).real for t in t_vals])
        
        # Set intercept to same as original function
        #fourier_approximation = fourier_approximation - fourier_approximation[0] + self.original_offset 
        
        # Adjust intercept to minimize distance between entire function, 
        # rather than just the intercepts. Gibbs-type phenomenon causes
        # perturbations near endpoints of interval
        fourier_approximation = fourier_approximation - (fourier_approximation - self.fxn_vals).mean()
        
        circles_approximation = circles_approximation - (circles_approximation - self.fxn_vals).mean()
        self.circles_approximation = circles_approximation
        
        # Origin offset
        self.origin_offset = fourier_approximation[0] - self.fxn_vals[0]
        
        # Circles offset
        self.circles_approximation_offset = circles_approximation[0] - self.fxn_vals[0]
        
        # Set intercept to same as original function
        self.fourier_approximation = fourier_approximation