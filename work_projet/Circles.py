
class Circles:
    """ Circles Class:
        Tracks radii and centers of circles implied by 
        Fourier decomposition of given FourierTransform object
    """
    def __init__(self,
                 FT, # FourierTransform object
                 num_circles=20, # Number of circles to keep track of
                 t_init=0, # Initial time state of object
                 origin=(0, 0) # Center of the first circle
        ):
        self.FT = FT
        self.t_init = t_init
        if num_circles > FT.N:
            raise Exception("num_circles exceeds the degree of the given Fourier series.")
        self.num_circles = num_circles
        self.origin = origin
        self.origin_x = origin[0]
        self.origin_y = origin[1]
        self.t_elapsed = 0
        self.steps_elapsed = 0
        self.t_current = self.t_init
        self.t_index_current = 0
        self.true_fxn_val_current = self.FT.fxn_vals[t_init]
        self.fourier_approx_val_current = self.FT.fourier_approximation[t_init]
        
        self.Xs = [] # Track the coords of the center of the last circle
        self.Ys = [] # for each value of t 
        
        self.As = FT.amplitudes[0:num_circles] # Amplitude of each frequency/circle
        self.Zs = FT.phases[0:num_circles] # Phase of each frequency/cirlce
    
    def circle_positions(self, transpose=False):
        """compute the current radii and centers of each circle at the current value of t"""
        
        num_circles = self.num_circles
        t = self.t_current
        
        running_x_offset = deepcopy(self.origin_x)
        running_y_offset = deepcopy(self.origin_y)

        # There will be 1 more center than radius;
        # Use this to plot the last point on the last circle
        # Stored in final_x, final_y below
        radii = []
        x_centers = [deepcopy(self.origin_x)]
        y_centers = [deepcopy(self.origin_y)]
        
        for i in range(0,num_circles):
            freq = i+1 # Corresponding frequency for given circle/coefficient
            a = self.As[i] # Magnitude (i.e., amplitude) of complex coefficient
            z = self.Zs[i] # Argument (i.e., phase) of complex coefficient

            radius = 2*a
            radii.append(radius)
            
            running_x_offset += 2*a*np.cos(t*2*np.pi*freq/self.FT.period + z)
            running_y_offset += 2*a*np.sin(t*2*np.pi*freq/self.FT.period + z)
            
            if i < num_circles-1:
                x_centers.append(running_x_offset)
                y_centers.append(running_y_offset)
            
        if t==0:
                        self.circles_offset = running_x_offset
        radii = np.array(radii)
        x_centers = np.array(x_centers) - self.circles_offset + self.FT.origin_offset
        y_centers = np.array(y_centers)
        
        x_final = running_x_offset - self.circles_offset + self.FT.origin_offset
        y_final = running_y_offset
        
        self.Xs.append(x_final)
        self.Ys.append(y_final)
        
        if transpose:
            return(radii, -y_centers, x_centers, -y_final, x_final)
        return(radii, x_centers, y_centers, x_final, y_final)
    
    
    def get_circles(self, transpose=False):
        return(self.circle_positions(transpose=transpose))
    
    def step(self, dt=1):
        # dt = how many times to increment t_vals array for each step
        self.steps_elapsed += 1
        next_index = dt*self.steps_elapsed 
        if next_index > len(self.FT.t_vals)-1:
            print("Max t-value reached")
            self.steps_elapsed -= 1
        else:
            self.t_current = self.FT.t_vals[next_index]
            self.t_elapsed = self.t_current - self.t_init
            self.t_index_current = next_index
            self.true_fxn_val_current = self.FT.fxn_vals[next_index]
            self.fourier_approx_val_current = self.FT.fourier_approximation[next_index]

#%%
# Animate the Circles!
#%%
x_spl = horse.x_spl
y_spl = horse.y_spl
num_pixels = horse.num_pixels

# Number of circles to draw in animation
num_circles = 100

anim_length = 20 # in seconds
fps = 24 # frames per second
num_frames = anim_length*fps
interval = (1./fps)*1000
#%%
# Ensure that the approximation has at least 2000
# points to ensure smoothness
dt = (int(2000. / num_frames) + 1)
num_points =  dt* num_frames
xFT = FourierTransform(x_spl, (0, num_pixels), num_points=num_points, N=num_circles)
yFT = FourierTransform(y_spl, (0, num_pixels), num_points=num_points, N=num_circles)
#%%
# Distance between circles and image
X_circles_spacing = 200
Y_circles_spacing = 300
#%%
# Origin calculation: Offset the circles so they line up with 
# the plotted image
x_main_offset = xFT.origin_offset
y_main_offset = yFT.origin_offset
x_origin = (0, X_circles_spacing)
#y_origin = (circles_spacing, y_main_offset)
y_origin = (0, Y_circles_spacing)
#y_origin = (0,0)

#%%
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

#%%
#Note: The rendering will take several (5-10) minutes!
#Adjust the num_cirlces, fps, and anim_length parameters above to reduce render time. 
#Particularly when just getting started, making all of these numbers smaller will significantly speed up the animation process.
xCircles = ComplexCircles(xFT, num_circles=num_circles, origin=x_origin)
yCircles = ComplexCircles(yFT, num_circles=num_circles, origin=y_origin)

#------------------------------------------------------------
#%%
# set up figure and styling
fig = plt.figure()
plt.axis([-400,75,-150,350])

ax = plt.gca()
ax.set_aspect(1)
ax.set_facecolor('#f9f9f9')

# Suppress axes
ax.set_yticklabels([])
#ax.set_xticklabels([])
plt.tight_layout(pad=0)
plt.axis('off')

circle_color = 'black'
drawing_color = '#9c0200'


#------------------------------------------------------------
#%%
# Set up animation elements


# INITIALIZE CIRLCE PLOTS
alphas = np.linspace(1, 0.25, num_circles) #np.repeat(1, num_circles)
X_circle_objs = []
X_center_objs = []
Y_circle_objs = []
Y_center_objs = []

X_radii, X_x_centers, X_y_centers, X_x_final, X_y_final = xCircles.get_circles()
Y_radii, Y_x_centers, Y_y_centers, Y_x_final, Y_y_final = yCircles.get_circles(transpose=True)


for c in range(0,num_circles):
    # X Outer Circles
    Xcirc = plt.Circle((X_x_centers[c], X_y_centers[c]), radius=X_radii[c],
                      edgecolor=circle_color, facecolor='None', alpha=alphas[c])
    X_circle_objs.append(Xcirc)
    # X Center Point Circles
    Xcenter = plt.Circle((X_x_centers[c], X_y_centers[c]), radius=2,
                      edgecolor=circle_color, facecolor=circle_color, alpha=alphas[c])
    X_center_objs.append(Xcenter)
    
    
    # Y Outer Circles
    Ycirc = plt.Circle((Y_x_centers[c], Y_y_centers[c]), radius=Y_radii[c],
                      edgecolor=circle_color, facecolor='None', alpha=alphas[c])
    Y_circle_objs.append(Ycirc)
    # Y Center Point Circles
    Ycenter = plt.Circle((Y_x_centers[c], Y_y_centers[c]), radius=2,
                      edgecolor=circle_color, facecolor=circle_color, alpha=alphas[c])
    Y_center_objs.append(Ycenter)

    
# Connectors between end of circles and actual drawing
X_connector_line, = ax.plot([], [], '-', lw=1, color='black')
Y_connector_line, = ax.plot([], [], '-', lw=1, color='black') 

# Point on plot at current time t
trace_point, = ax.plot([], [], 'o', markersize=8, color=drawing_color)

# Trace of full drawing
#%%
drawing_segments = []
for idx in range(len(xFT.t_vals)):
    segment, = ax.plot([-1000, -1001], [-1000,-1001], '-', lw=1, color=drawing_color, alpha=alpha_vals[idx])
    drawing_segments.append(segment)
# Add one more for line segment
segment, = ax.plot([-1000,-1001], [-1000,-1001], '-', lw=1, color=drawing_color, alpha=alpha_vals[0])
drawing_segments.append(segment)


# Plot axes of cirlces
#%%
x_main_offset = X_x_centers[0]
y_main_offset = Y_y_centers[0]

axis_length = 50
axis_style = {
    "linestyle": "solid",
    "linewidth": 1,
    "color": "black"
}
x_x_axis = ax.plot(
    [x_main_offset-axis_length, x_main_offset+axis_length], 
    [X_circles_spacing,X_circles_spacing],
    **axis_style
)
x_y_axis = ax.plot(
    [x_main_offset, x_main_offset], 
    [X_circles_spacing-axis_length,X_circles_spacing+axis_length],
    **axis_style
)
y_x_axis = ax.plot(
    [-Y_circles_spacing-axis_length, -Y_circles_spacing+axis_length],
    [y_main_offset, y_main_offset], 
    **axis_style
)
y_y_axis = ax.plot(
    [-Y_circles_spacing, -Y_circles_spacing],
    [y_main_offset-axis_length, y_main_offset+axis_length], 
    **axis_style
)

#%%
def init():
    """initialize animation"""
    for idx in range(len(xFT.t_vals)):
        drawing_segments[idx].set_data([],[])
    
    X_connector_line.set_data([], [])
    Y_connector_line.set_data([], [])
    trace_point.set_data([], [])
    #centers.set_data([], [])
    for c in range(num_circles):
        ax.add_patch(X_circle_objs[c])
        ax.add_patch(X_center_objs[c])
        ax.add_patch(Y_circle_objs[c])
        ax.add_patch(Y_center_objs[c])
    return([])

#%%
def animate(i):
    """perform animation step"""
        
    X_radii, X_x_centers, X_y_centers, X_x_final, X_y_final = xCircles.get_circles()
    Y_radii, Y_x_centers, Y_y_centers, Y_x_final, Y_y_final = yCircles.get_circles(transpose=True)
    #Y_x_centers = [x - circles_spacing for x in Y_x_centers]
    #Y_x_final = Y_x_final - circles_spacing

 for c in range(0,num_circles):
        # X Outer Circles
        X_circle_objs[c].center = (X_x_centers[c], X_y_centers[c])
        # X Center Point Circles
        X_center_objs[c].center = (X_x_centers[c], X_y_centers[c])

        # Y Outer Circles
        Y_circle_objs[c].center = (Y_x_centers[c], Y_y_centers[c])
        # Y Center Point Circles
        Y_center_objs[c].center = (Y_x_centers[c], Y_y_centers[c])
        
    
    #idx_current = max(int(np.round(xCircles.t_current)),len(xFT.fourier_approximation)-1)
    idx_current = xCircles.t_index_current
    x_true_current = deepcopy(xCircles.fourier_approx_val_current)
    y_true_current = deepcopy(yCircles.fourier_approx_val_current)
    X_connector_line.set_data(
        [x_true_current, x_true_current], 
        [y_true_current, X_y_final]
    )
    Y_connector_line.set_data(
        [Y_x_final, x_true_current], [y_true_current, y_true_current]
    )
    trace_point.set_data([x_true_current], [y_true_current])
    
    # Iterate circles to next step
    xCircles.step(dt=dt)
    yCircles.step(dt=dt)

    drawing_segments[idx_current].set_data(
        [x_true_current, xCircles.fourier_approx_val_current], 
        [y_true_current, yCircles.fourier_approx_val_current]
    )
    
    
    return([])


 


ani = animation.FuncAnimation(fig, animate, frames=num_frames,
                              interval=interval, blit=True, init_func=init)

HTML(ani.to_html5_video())

# If you get the "KeyError: 'ffmpeg'" error (as you will if you run this on Binder),
# then your system does not have the ffmpeg video library installed.
# You can get around this by using an alternative image library.
# COMMENT OUT the line "HTML(ani.to_html5_video())" above, and UNCOMMENT the following lines:

#from IPython.display import Image as DisplayImage
#ani.save('./animation.gif', writer='imagemagick')
#DisplayImage(url='./animation.gif')

#---------------------------------------------------------

#%%
# Fun miscellaneous function to draw a single frame of the 
# circles animation; understanding this step and getting the
# phase/amplitude of the circles correct is 90% of the work
# for understanding how the full animation works
def draw_circles(FT, t, num_circles=200):
    
    period = FT.period
    As = FT.amplitudes[0:num_circles]
    Zs = FT.phases[0:num_circles]

    t_vals = np.linspace(0,3000, 500)
    Xs = []
    Ys = []
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    x_offset = 0
    y_offset = 0

    col="#004785"
    for i in range(0,num_circles):
        Hz = i+1
        a = As[i] # Magnitude (i.e., amplitude) of complex coefficient
        z = Zs[i] # Argument (i.e., phase) of complex coefficient

        plt.plot([x_offset], [y_offset], marker='o', markersize=10, color=col)
        circ = plt.Circle((x_offset, y_offset), radius=2*a, edgecolor='black',
                          linewidth=2, facecolor='None')
        ax.add_patch(circ)

        x_offset += 2*a*np.cos(t*2*np.pi*Hz/period + z)
        y_offset += 2*a*np.sin(t*2*np.pi*Hz/period + z)

    Xs.append(x_offset)
    Ys.append(y_offset)
    plt.axis('equal')
    plt.show()
    return(fig)

#%%
f = draw_circles(xFT, 1400, num_circles=20)