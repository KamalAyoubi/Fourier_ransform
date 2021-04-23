
# Animate the Circles!
# Obviously, it helps to have a simple image with only 2 colors and 
# close to a single path
#%%
#url = "http://thevirtualinstructor.com/images/continuouslinedrawinghorse.jpg"
url = 'https://www.seekpng.com/png/detail/116-1164659_line-drawing-bunny-rabbit-at-getdrawings-bunny-drawing.png'
response = ImageObject(url)
response.show()

x_spl = response.x_spl
y_spl = response.y_spl
num_pixels = response.num_pixels

# Number of circles to draw in animation
num_circles = 100

anim_length = 20 # in seconds
fps = 24 # frames per second
num_frames = anim_length*fps
interval = (1./fps)*1000

# Ensure that the approximation has at least 2000
# points to ensure smoothness
dt = (int(2000. / num_frames) + 1)
num_points =  dt* num_frames
xFT = FourierTransform(x_spl, (0, num_pixels), num_points=num_points, N=num_circles)
yFT = FourierTransform(y_spl, (0, num_pixels), num_points=num_points, N=num_circles)

# Distance between circles and image
X_circles_spacing = 250
Y_circles_spacing = 350
 
# Origin calculation: Offset the circles so they line up with 
# the plotted image
x_main_offset = xFT.origin_offset
y_main_offset = yFT.origin_offset
x_origin = (0, X_circles_spacing)
#y_origin = (circles_spacing, y_main_offset)
y_origin = (0, Y_circles_spacing)
#y_origin = (0,0)


# approximation is to the original function (prevents the big 
# swoops across the drawing to dominate the image)
approx_coords = np.array(list(zip(xFT.fourier_approximation, yFT.fourier_approximation)))
og_coords = np.array(list(zip(horse.x_tour, horse.y_tour)))
approx_dist = distance.cdist(approx_coords, og_coords, 'euclidean')
closest_points = approx_dist.min(1)

def alpha_fxn(d):
    # Takes distance between approx. and true value
    # and returns transparency level
    return(np.exp(-(1/10)*d))
    #hist = plt.hist(closest_points)
    heights = hist[0]
    scaled_h = heights/heights[0]
    breaks = hist[1]
    for i, b in enumerate(breaks[1:]):
        if d < b:
            return(scaled_h[i])
    
cutoff = int(len(closest_points)*.95)
alpha_vals = [alpha_fxn(p) if i < cutoff else 0.33 for i, p in enumerate(closest_points)]
