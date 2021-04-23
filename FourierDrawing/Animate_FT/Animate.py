
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np


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
xFT = FourierApprox(x_spl, (0, num_pixels), num_points=num_points, N=num_circles)
yFT = FourierApprox(y_spl, (0, num_pixels), num_points=num_points, N=num_circles)

# Distance between circles and image
X_circles_spacing = 200
Y_circles_spacing = 300

# Origin calculation: Offset the circles so they line up with 
# the plotted image
x_main_offset = xFT.origin_offset
y_main_offset = yFT.origin_offset
x_origin = (0, X_circles_spacing)
#y_origin = (circles_spacing, y_main_offset)
y_origin = (0, Y_circles_spacing)
#y_origin = (0,0)
# %%
# These calculations set transparency based on how close the 
# approximation is to the original function (prevents the big 
# swoops across the drawing to dominate the image)
approx_coords = np.array(list(zip(xFT.fourier_approximation, yFT.fourier_approximation)))
og_coords = np.array(list(zip(Img.x_tour,Img.y_tour)))
approx_dist = distance.cdist(approx_coords, og_coords, 'euclidean')
closest_points = approx_dist.min(1)
def alpha_fxn(d):
    return(np.exp(-(1/10)*d))
    heights = hist[0]
    scaled_h = heights/heights[0]
    breaks = hist[1]
    for i, b in enumerate(breaks[1:]):
        if d < b:
            return(scaled_h[i])
    
cutoff = int(len(closest_points)*.95)
alpha_vals = [ alpha_fxn(p) if i < cutoff else 0.33 for i, p in enumerate(closest_points) ]

xCircles = Circles(xFT, num_circles=num_circles, origin=x_origin)
yCircles = Circles(yFT, num_circles=num_circles, origin=y_origin)

# set up figure and styling
fig = plt.figure()
plt.axis([-550,500,-250,350])

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
drawing_segments = []
for idx in range(len(xFT.t_vals)):
    segment, = ax.plot([-1000, -1001], [-1000,-1001], '-', lw=1, color=drawing_color, alpha=alpha_vals[idx])
    drawing_segments.append(segment)
# Add one more for line segment
segment, = ax.plot([-1000,-1001], [-1000,-1001], '-', lw=1, color=drawing_color, alpha=alpha_vals[0])
drawing_segments.append(segment)


# Plot axes of cirlces
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


def init():
    """initialize animation"""
    for idx in range(len(xFT.t_vals)):
        drawing_segments[idx].set_data([],[])
    
    X_connector_line.set_data([], [])
    Y_connector_line.set_data([], [])
    trace_point.set_data([], [])
    
    for c in range(num_circles):
        ax.add_patch(X_circle_objs[c])
        ax.add_patch(X_center_objs[c])
        ax.add_patch(Y_circle_objs[c])
        ax.add_patch(Y_center_objs[c])
    return([])

def animate(i):
    """perform animation step"""
        
    X_radii, X_x_centers, X_y_centers, X_x_final, X_y_final = xCircles.get_circles()
    Y_radii, Y_x_centers, Y_y_centers, Y_x_final, Y_y_final = yCircles.get_circles(transpose=True)
    

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

ani.save('./animation.gif', writer='imagemagick')
DisplayImage(url='./animation.gif') 