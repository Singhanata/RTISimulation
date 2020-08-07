from geoutil import RTIGrid
from rti_scheme import RTIScheme, SidePositionScheme
from rti_cal import RTIWeightCalculator, LineWeightingRTICalculator
from rti_estimator import RTIEstimator

class RTISimulation():
    def __init__(self):
        rs = SidePositionScheme()
        rc = LineWeightingRTICalculator(rs)
        re = RTIEstimator(rc, 1.)
        self.estimator = re
    
    def calIdealLinkAtten(self, voxelAttenM):
        try:
            vxArr = RTIGrid.reshapeVoxelM2Arr(voxelAttenM)
            linkAttenArr = (self.
                            estimator.
                            weightCalculator.
                            calIdealLinkAtten(vxArr))
            return linkAttenArr
        except ValueError:
            raise ValueError('Dimension mismatch.')
            
    def simulateReferenceInput(self, x_range, y_range):
        pass
            
        
if __name__ == "__main__":
     rti = RTISimulation()
     # voxelAttenM = np.zeros()
     # rti.calIdealLinkAtten(voxelAttenM)

