
import numpy as np
import matplotlib.pyplot as plt

def process_boxplot(data, **kw):
    fig, ax = plt.subplots(1,1)    
    bp = plt.boxplot(data, patch_artist = True,
                notch ='True', vert = 0)
    ax.set_xticklabels(kw['ticklabel'])
    ax.set_xlabel(kw['xlabel'])
    ax.set_ylabel(kw['ylabel'])
    plt.grid()
    
    colors = ['bla', 'b',
          'b', 'b']
 
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='#8B008B',
                    linewidth = 1.5,
                    linestyle =":")
     
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='#8B008B',
                linewidth = 2)
     
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='b',
                   linewidth = 3)
     
    # changing style of fliers
    for flier in bp['fliers']:
        flier.set(marker ='D',
                  color ='#e7298a',
                  alpha = 0.5)
         
    plt.show()

data_1 = np.random.normal(100, 10, 200)
data_2 = np.random.normal(90, 20, 200)
data_3 = np.random.normal(80, 30, 200)
data_4 = np.random.normal(70, 40, 200)
data = [data_1, data_2, data_3, data_4]
tickLabel = ['1e0','1e1','1e2','1e3'] 

process_boxplot(data, 
                ticklabel = tickLabel,
                xlabel = 'Alpha',
                ylabel = 'RMSE')
