
import numpy as np
import matplotlib.pyplot as plt

x = [1 ,10 ,100,1000]

y = [1,2,3,4]

fig, ax = plt.subplots(1,1)
 
ax.set_xscale('log')

ax.set_xlabel('LOG')

plt.plot(x,y)

plt.show()