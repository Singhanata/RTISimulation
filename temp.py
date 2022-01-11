import numpy as np
import matplotlib.pyplot as plt
import os
from enum import Enum
class RecordIndex(Enum):
    IMAGE = 0
    OBJ_MEAN = 1
    NON_MEAN = 2
    RMSE_ALL = 3
    RMSE_OBJ = 4
    RMSE_NON = 5
    DERIVATIVE_X = 6
    DERIVATIVE_Y = 7
    DERIVATIVE_ABS = 8
    DERIVATIVE_MEAN = 9
    DERIVATIVE_OBJ = 10
    DERIVATIVE_NON = 11
    DERIVATIVE_BORDER = 12
    DERIVATIVE_NONBORDER = 13
    DERIVATIVE_BORDERRATIO = 14
    DERIVATIVE_NONBORDERRATIO = 15
    
    def cal(self, reF, reS, **kw):
        if self == RecordIndex(0): 
            return 'hey'
        if self == RecordIndex(1): 
            return 'hey'
        if self == RecordIndex(2): 
            return 'hey'
        if self == RecordIndex(3): 
            return 'hey'
        if self == RecordIndex(4): 
            return 'hey'
        if self == RecordIndex(5): 
            return 'hey'
        if self == RecordIndex(6): 
            return 'hey'
        if self == RecordIndex(7): 
            return 'hey'
        if self == RecordIndex(8): 
            return 'hey'
        if self == RecordIndex(9): 
            return 'hey'
        if self == RecordIndex(10): 
            return 'hey'
        if self == RecordIndex(11): 
            return 'hey'
        if self == RecordIndex(12): 
            return 'hey'
        if self == RecordIndex(13): 
            return 'hey'
        if self == RecordIndex(14): 
            return 'hey'
        if self == RecordIndex(15): 
            return 'hey'
    
def process_boxplot(data, **kw):
    fig, ax = plt.subplots(1,1)

    bp = plt.boxplot(data, 
                     patch_artist = True,
                     notch = True,
                     zorder=1)
    
    ax.set_xticklabels(kw['ticklabel'])
    ax.set_xlabel(kw['xlabel'])
    ax.set_ylabel(kw['ylabel'])
    
    ax.legend()
    plt.grid()
    
    colors = ['b', 'g',
              'r', 'violet', 
              'white', 'yellow']
 
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set(linewidth = 1.5)
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='black',
                    linewidth = 2,
                    linestyle ="--")
     
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='black',
                linewidth = 5)
     
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='black',
                   linewidth = 3)
     
    # changing style of fliers
    for flier in bp['fliers']:
        flier.set(marker ='D',
                  markersize = 5,
                  color ='black',
                  alpha = 0.5)
    if 'filename' in kw:
        if 'path' in kw:
            fn = os.sep.join([kw['path'], 
                             (kw['filename'] + '.svg')])
        else:
            fn = (kw['filename'] + '.svg')
        plt.savefig(fn)     
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


