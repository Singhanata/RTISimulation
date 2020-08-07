import copy
from geoutil import RTIGrid
import matplotlib.pyplot as plt
def transformWeightingM(wM_in):
    wM_temp = copy.deepcopy(wM_in)
    wM_out = []
    for i in range(len(wM_temp)):
        wM_out.append(RTIGrid.reshapeVoxelM2Arr(wM_temp[i]))
    
    return wM_out

def plotRTIIm(iM):
    fig,ax = plt.subplots()
    hm = ax.imshow(iM, cmap = 'coolwarm', interpolation = 'nearest')
    plt.colorbar(hm)
    plt.show()