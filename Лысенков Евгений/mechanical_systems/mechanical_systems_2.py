import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

t0 = 0
dt = 0.05

v0 = 0;
y0 = 10
a = 9.8

def generator(v0, y0, a, t0, dt):
    v = [v0]
    y = [y0]
    P = [y[-1]*a]
    K = [(v[-1]**2)/2]
    t = [t0]
    yield (t,y,v,P,K)
        
    while y[-1] >= 0:
        v.append(v[-1] - a*dt) 
        y.append(y[-1] + v[-1]*dt)
        P.append(y[-1]*a)
        K.append((v[-1]**2)/2)
        t.append(t[-1] + dt)
        yield (t,y,v,P,K)
	
    while(True):  
        v.append(0)
        y.append(0)
        P.append(0)
        K.append(0)
        t.append(t[-1] + dt)
        yield (t,y,v,P,K)

fig, axes = plt.subplots(2)
ax1 = axes[0]
ax2 = axes[1]
gen = generator(v0, y0, a, t0, dt)

def animate(i):
    ax1, ax2, gen
    ax1.clear()
    ax1.set_xlim(0, 4)
    ax1.set_ylim(0, y0+1)
    tyvPK = next(gen)
    ax1.scatter([2], [tyvPK[1][-1]], lw = 3)
    
    ax2.clear()
    ax2.set_xlim(tyvPK[0][0], tyvPK[0][-1])
    miny = min(min(tyvPK[1]), min(tyvPK[2]), min(tyvPK[3]), min(tyvPK[4]))
    maxy = max(max(tyvPK[1]), max(tyvPK[2]), max(tyvPK[3]), max(tyvPK[4]))
    ax2.set_ylim(miny-1, maxy+1)
    ax2.plot(tyvPK[0], tyvPK[1], label='y')
    ax2.plot(tyvPK[0], tyvPK[2], label='v')
    ax2.plot(tyvPK[0], tyvPK[3], label='K')
    ax2.plot(tyvPK[0], tyvPK[4], label='P')
    

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()