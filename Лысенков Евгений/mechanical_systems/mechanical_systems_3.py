import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

t0 = 0
dt = 0.05

v0 = 10
alpha = np.pi/6
y0 = 0
x0 = 0
a = 9.8

def generator(v0, x0, y0, a, alpha, t0, dt):
    v = []
    vx = []
    vy = []
    x = [x0]
    y = []
    P = []
    K = []
    t = [t0]
    
    while(True):
        v.append(v0)
        vx.append(v0*np.cos(alpha))
        vy.append(v0*np.sin(alpha))
        y.append(y0)
        P.append(y[-1]*a)
        K.append((v[-1]**2)/2)
        yield (t,x,y,v,vx,vy,P,K)
        
        while y[-1] >= 0:
            vy.append(vy[-1] - a*dt)
            vx.append(vx[-1])
            v.append(np.sqrt(vx[-1]**2+vy[-1]**2))
            x.append(x[-1] + vx[-1]*dt)
            y.append(y[-1] + vy[-1]*dt)
            P.append(y[-1]*a)
            K.append((v[-1]**2)/2)
            t.append(t[-1] + dt)
            yield (t,x,y,v,vx,vy,P,K)
            
        vy.append(-vy[-1])
        vx.append(vx[-1])
        v.append(np.sqrt(vx[-1]**2+vy[-1]**2))
        x.append(x[-1] + vx[-1]*dt)
        y.append(y[-1] + vy[-1]*dt)
        P.append(y[-1]*a)
        K.append((v[-1]**2)/2)
        t.append(t[-1] + dt)
        yield (t,x,y,v,vx,vy,P,K)

        while y[-1] > y[-2]:
            vy.append(vy[-1] - a*dt)
            vx.append(vx[-1])
            v.append(np.sqrt(vx[-1]**2+vy[-1]**2))
            x.append(x[-1] + vx[-1]*dt)
            y.append(y[-1] + vy[-1]*dt)
            P.append(y[-1]*a)
            K.append((v[-1]**2)/2)
            t.append(t[-1] + dt)
            yield (t,x,y,v,vx,vy,P,K)
        
        vy.append(-vy[-1])
        vx.append(vx[-1])
        v.append(np.sqrt(vx[-1]**2 + vy[-1]**2))
        x.append(x[-1] + vx[-1]*dt)
        y.append(y[-1] + vy[-1]*dt)
        P.append(y[-1]*a)
        K.append((v[-1]**2)/2)
        t.append(t[-1] + dt)
        yield (t,x,y,v,vx,vy,P,K)
        t.append(t[-1]+1)
        x.append(x[-1] + vx[-1]*dt)

fig, axes = plt.subplots(2)
ax1 = axes[0]
ax2 = axes[1]
gen = generator(v0, x0, y0, a, alpha, t0, dt)

def animate(i):
    ax1, ax2, gen
    ax1.clear()
    all = next(gen)
    ax1.set_xlim(100*(all[1][-1]//100), 100*(all[1][-1]//100 + 1))
    ax1.set_ylim(0, 10)
    ax1.scatter([all[1][-1]], [all[2][-1]], lw = 3)
    
    ax2.clear()
    ax2.set_xlim(all[0][0], all[0][-1])
    #miny = min(all[1])
    #maxy = max(all[1])
    miny = min(min(all[2]), min(all[3]), min(all[5]), min(all[6]), min(all[7]))
    maxy = max(max(all[2]), max(all[3]), max(all[5]), max(all[6]), max(all[7]))
    ax2.set_ylim(miny-1, maxy+1)
    ax2.plot(all[0], all[2], label='y')
    ax2.plot(all[0], all[3], label='v')
    ax2.plot(all[0], all[4], label='vx')
    ax2.plot(all[0], all[5], label='vy')
    ax2.plot(all[0], all[6], label='K')
    ax2.plot(all[0], all[7], label='P')
    ax2.legend(loc = 'right')
    

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()