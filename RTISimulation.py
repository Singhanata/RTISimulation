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
            
    def simulateReferenceInput(self):
        scheme = self.estimator.weightCalculator.scheme
        
        coordX = scheme.selection.coordX
        coordY = scheme.selection.coordY
        
        dx = coordX[-1] - coordX[0]
        dy = coordY[-1] - coordY[0]
        w_x_range = dx/5
        w_y_range = dy/5
        
        x_range_l = (coordX[0], coordX[0] + dx/5)
        x_range_c = (coordX[0] + 2*dx/5, coordX[0] + 3*dx/5)
        x_range_r = (coordX[0] + 4*dx/5, coordX[0] + 5*dx/5)
        
        y_range_b = (coordY[0], coordY[0] + dx/5)
        y_range_c = (coordY[0] + 2*dy/5, coordY[0] + 3*dy/5)
        y_range_t = (coordY[0] + 4*dy/5, coordY[0] + 5*dy/5)
        
        vxS_lb = scheme.getVoxelScenario(x_range_l, y_range_b)
        vxS_cb = scheme.getVoxelScenario(x_range_c, y_range_b)
        vxS_rb = scheme.getVoxelScenario(x_range_r, y_range_b)
        vxS_lc = scheme.getVoxelScenario(x_range_l, y_range_c)
        vxS_cc = scheme.getVoxelScenario(x_range_c, y_range_c)
        vxS_rc = scheme.getVoxelScenario(x_range_r, y_range_c)
        vxS_lt = scheme.getVoxelScenario(x_range_l, y_range_t)
        vxS_ct = scheme.getVoxelScenario(x_range_c, y_range_t)
        vxS_rt = scheme.getVoxelScenario(x_range_r, y_range_t)

        l_lb = self.calIdealLinkAtten(vxS_lb)
        l_cb = self.calIdealLinkAtten(vxS_cb)
        l_rb = self.calIdealLinkAtten(vxS_rb)
        l_lc = self.calIdealLinkAtten(vxS_lc)
        l_cc = self.calIdealLinkAtten(vxS_cc)
        l_rc = self.calIdealLinkAtten(vxS_rc)
        l_lt = self.calIdealLinkAtten(vxS_lt)
        l_ct = self.calIdealLinkAtten(vxS_ct)
        l_rt = self.calIdealLinkAtten(vxS_rt)
                    
        return (l_lb, l_cb, l_rb, l_lc, l_cc, l_rc, l_lt, l_ct, l_rt)
    
if __name__ == "__main__":
     rti = RTISimulation()
     # rti.simulateReferenceInput()

