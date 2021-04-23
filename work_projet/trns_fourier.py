#La transformée de Fourier discrète bi-dimensionnelle. Application
#à la compression d’image.
#On utilisera ici le sous-module ndimage du module scipy (from scipy import
#ndimage). On étudie l’image représentée en figure

#%%
import numpy as np
import pylab as pl
import scipy
from scipy import ndimage
pi=np.pi
image = ndimage.imread('image.jpg')
pl.imshow(image)
pl.colorbar()
imageR=image[:,:,0]
imageG=image[:,:,1]
imageB=image[:,:,2]
 
pl.figure()
pl.imshow(imageR)
pl.colorbar()
pl.show()

# Transformées de Fourier Discrète et Rapide
#%%
data=np.loadtxt('data.out')
print (data.shape)
time=data[:,0]
signal=data[:,1]
#pl.plot(time,signal)
#pl.show()

#%%
ctfd=np.fft.fft(signal)
ctfd=np.fft.fftshift(ctfd)
#%%
actfd=np.abs(ctfd)
ctfd[actfd<0.9*np.max(actfd)]=0
pl.figure();
pl.plot(actfd)
pl.plot(ctfd)
 
#%%
signali=np.fft.ifft(ctfd)
 
 
pl.figure(figsize=(12,6))
pl.plot(time,signal, color="bleu",label="signalnal brut")
pl.plot(time, signali, color="red",label="composante spectral principale")

# Intégration numérique
#%%
def rectG(x,y):
    npts = x.shape[0]
    h1 = (x[npts-1]-x[0])/(npts-1)
    print (x[npts-1],x[0],npts)
    h2 =x[1]-x[0]
    s=0
    for i in range(0,npts-1):
            s=s+y[i]
    return h1*s
     
a=np.linspace(0,1,5)
b=np.linspace(1,1,5)
print(a)
print(b)
print(rectG(a,b))