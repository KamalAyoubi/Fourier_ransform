from PIL import Image
import requests
from io import BytesIO
import pylab
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.spatial import distance
from scipy.interpolate import UnivariateSpline


class Imagemanip:
    def __init__(self, url ):
    """ Create image object  """

        # Import raw image
        self.url = url
        response = requests.get(url)
        self.img_raw = Image.open(BytesIO(response.content))

    
    def show(self):
    """ Show raw image and his informations """

        # Show raw image 
        pylab.imshow(np.asarray(self.img_raw))

        # Show image informations
        print("The image format is : {}".format(self.img_raw.format))
        print("The image size is : {}".format(self.img_raw.size))
        print("The image mode is : {}".format(self.img_raw.mode))
        
    def single_color(self):
    """ Convert image to single color """  

        #Convert image to single color
        self.img_single_color = self.img_raw.convert('L')

    def convert_binary(self, scale=3, thresh_val=200):   
    """ Convert to binary image with 0 or 255 array values """

        # convert image to nympy array
        self.thresh_val = thresh_val
        image_array = np.array(self.img_single_color)

        # convert to binary image_array using thresh_val to cut
        for i in range(len(image_array)):
            for j in range(len(image_array[0])):
                if image_array[i][j] > thresh_val:
                    image_array[i][j] = 255 #white
                else:
                    image_array[i][j] = 0   #black
        self.image_array = image_array
        image = Image.fromarray(image_array)
        
        # reduce number of non-zero pixels by scaling down the image
        self.img_scale = image.resize(tuple([int(v/scale) for v in image.size]),Image.ANTIALIAS)
    
    def black_and_white(self):
    """  Convert image to black and white """

        # convert image to black and white
        self.img_blackwhite = self.img_scale.convert(mode='1', dither=2)
        self.pixels = (1 - np.asarray(self.img_blackwhite).astype(int))
        self.pixels_vector = np.reshape(self.pixels, self.pixels.size)

    def show_black_and_white(self):
    """  Show black and white image  """

        # Show black and white image 
        pylab.imshow(np.asarray(self.img_blackwhite))

        # Show black and white image informations
        print("The image format is : {}".format(self.img_blackwhite.format))
        print("The image size is : {}".format(self.img_blackwhite.size))
        print("The image mode is : {}".format(self.img_blackwhite.mode))
        print("Numbre of pixels is: {}".format(self.pixels.sum()))

    def distance_matrix(self):
    """ Get non-zero pixel coordiantes than calcualte distance between each pair of them """

        # Find positions of non-zero pixels
        non_zero_P_index = np.where(self.pixels_vector > 0)[0]

        # Make a range array index form 1 to len(non_zero_P_index)
        N = len(non_zero_P_index)+1
        arrange_index = np.array(range(1, N ))
        
        # Replace each non-zero pixel with its number
        self.flat_img_mod = deepcopy(self.pixels_vector)
        for r, pix in enumerate(non_zero_P_index):
            self.flat_img_mod[pix] = r+1

        # Get coordiantes for each non-zero pixel
        img_idx = np.reshape(self.flat_img_mod, self.pixels.shape)
        self.coord_list = []
        for v in arrange_index:
            v_coords = tuple([int(i) for i in np.where(img_idx==v)])
            self.coord_list.append(list(v_coords))
        
        # Calcualte distance between each pair of coords
        self.distance_matrix = distance.cdist(self.coord_list, self.coord_list, 'euclidean')
   
    def contours_search(self, plot=True):
    """ Get the image tour using the nearest neighbor heuristic  """ 

        edges = self.coord_list
        length_edges = len(edges)

        # Set a random starting edge form length edges
        start = int(np.random.choice(range(length_edges),size=1))

        # Set the starting edge for heuristic nearest neighbor research
        tour = [start]
        current_edge = start

        # Look for the point closest to the current edge
        for step in range(0, length_edges):
            dist_row = deepcopy(self.distance_matrix[current_edge,:])
            for i in tour:
                dist_row[i] = np.inf
            nearest_neighbor = np.argmin(dist_row)
            if nearest_neighbor not in tour:
                tour.append(nearest_neighbor)
            current_edge = nearest_neighbor
        
        # Extract the coordinates of the tour points 
        x_y_tour = list()
        for i in range(length_edges+1):
            v = edges[tour[i % length_edges]]  
            x_y_tour.append(v)
        xy_tour = np.array(x_y_tour)

        x_tour = xy_tour[:,1]
        y_tour = -xy_tour[:,0]

        x_tour = x_tour - x_tour[0]
        y_tour = y_tour - y_tour[0]

        # Close the circuit by returning to the beginning point
        np.append(x_tour, x_tour[0])
        np.append(y_tour, y_tour[0])
        length_edges = length_edges + 1
    
        self.x_tour = x_tour
        self.y_tour = y_tour
        self.length_pixels = length_edges

        # Show the image countour
        if plot:
            plt.plot(self.x_tour, self.y_tour)

    def get_splines(self, degree=1, plot=True):
    """ Smooth the curves tour angles  """

        # Smooth the curves tour angles
        length_pixels_list = list(range(0,self.length_pixels))
        x_spl = UnivariateSpline(length_pixels_list, self.x_tour, k=degree)
        y_spl = UnivariateSpline(length_pixels_list, self.y_tour, k=degree)
        
        self.x_spl = x_spl
        self.y_spl = y_spl
        
        if plot:
            vect = np.linspace(0, self.length_pixels-1, 1000)
            x_cord = list()
            y_cord = list()
            for v in vect:
                x_cord.append(x_spl(v))
                y_cord.append(y_spl(v))  
            p = plt.plot(x_cord,y_cord)

