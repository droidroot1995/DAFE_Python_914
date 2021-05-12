import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

N1 = 10
m1 = 6.645*10**(-27)
T1 = 10000
N2 = 10
m2 = 3.3*10**(-26)
T2 = 10000

k = 1.38*10**(-23)
dt = 0.0001

xmin = 0.
xmax = 20.
ymin = 0.
ymax = 10.

def f(locT, locN, locm, locxmin, locxmax):
    global k,dt, ymin, ymax, xmin, xmax
    Vav = np.sqrt(3*k*locT/locm/locN)
    vx = np.random.uniform(-Vav,Vav,locN)
    vy = np.sqrt((-1)*(vx**2 - Vav**2))
    x = np.random.uniform(locxmin, locxmax, locN)
    y = np.random.uniform(ymin, ymax, locN)
    yield (x,y)
    while(True):
        for i in range(locN):    
            if (x[i] <= xmin or x[i] >= xmax):
                vx[i] = (-1)*vx[i]
                x[i] += vx[i]*dt    
            else:
            	x[i] += vx[i]*dt
            
            if (y[i] <= ymin or y[i] >= ymax):
                vy[i] = (-1)*vy[i]
            y[i] += vy[i]*dt
        yield (x,y)

fig, ax = plt.subplots()
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
line = ax.scatter([], [], lw = 2)
gen1 = f(T1, N1, m1, xmin, (xmax-xmin)/2)
gen2 = f(T2, N2, m2, (xmax-xmin)/2, xmax)

def init():
    global xmin, xmax, ymin, ymax
    ax.clear()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.scatter([], [], lw = 2, color = 'r')
    ax.scatter([], [], lw = 2, color = 'b')

def animate(i):
    global xmin, xmax, ymin, ymax, gen1, gen2
    xy1 = next(gen1)
    xy2 = next(gen2)
    ax.clear()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.scatter([xy1[0]], [xy1[1]], lw = 2, color = 'r')
    ax.scatter([xy2[0]], [xy2[1]], lw = 2, color = 'b')
    

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=10)

plt.show()