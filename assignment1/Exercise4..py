
import random
import matplotlib.pyplot as pl
import numpy as np

#Create an array X to store generated numbers
X=[]
#COSIN is an array in where we will store cosine values
COSIN=[]
#SIN is an array in where we will store sine values
SIN=[]
#Generate 10 random numbers between 0 and 90
for x in range(0,10):
     X.append(random.randrange(0,90))

X=np.sort(X)
for x in range(len(X)):
     COSIN.append(np.cos(X[x]))
for x in range(len(X)):
     SIN.append(np.sin(X[x]))
#Create a new subplot from a grid
fig, aX = pl.subplots(1)
#Plot sine using red color with a continuous line of width 1 (pixels)
aX.plot(X, SIN,'-r',label='sin')
# Plot cosine using blue color with a continuous line of width 1 (pixels)
aX.plot(X, COSIN,'-b',label='cos')
#Customize plot
pl.ylim(-1.5,1.5)
pl.xticks([0,10,20,30,40,50,60,70,80,90],[0,10,20,30,40,50,60,70,80,90])
pl.title('Plots of the sine and cosine function for 10 random numbers!')
pl.xlabel('x-axis')
pl.ylabel('y-axis')
#Add a legend
pl.legend(loc='best')
#Print random numbers 
print(X)
#Show the plot
pl.show()
