#%%
from FourierDrawing.ImageManipulation.Imgmanip import Imagemanip
from FourierDrawing.FourierApproximation.Class_fourierApproximation import FourierApprox
from FourierDrawing.Circles_radii_center.ComplexCircles import Circles
#from Animate_FT import Animate 
#%%

url = 'https://www.seekpng.com/png/detail/116-1164659_line-drawing-bunny-rabbit-at-getdrawings-bunny-drawing.png'


img = Imagemanip(url)
img.show()


#%%
img.single_color()
img.convert_binary(scale=3, thresh_val=200)
img.black_and_white()

img.show_black_and_white()
# %%
img.distance_matrix()

#%%
img.contours_search(plot=True)
# %%

img.get_splines(plot=True)
#%%
ani = animation.FuncAnimation(fig, animate, frames=num_frames,
                              interval=interval, blit=True, init_func=init)
#%%

ani.save('./Images/animation5.gif', writer='imagemagick')
DisplayImage(url='./Images/animation5.gif')
