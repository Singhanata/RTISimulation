import math
import numpy as np
from voxel import *
from geoutil import *
from link import *

class IntersectPosition(Position):
    def __init__(self, x, y, linkLambda):
        super().__init__(x, y)
        self.linkLambda = linkLambda

class RTISimulation():
    def __init__(self, scheme):
        self.area_w = area_w
        self.area_l = area_l
        self.voxel_w = voxel_w
        self.voxel_l = voxel_l
        self.n_sensor = n_sensor
        self.dist_ss = dist_ss





# def initSensorArr(arr_x, arr_y):
#     """
#     Parameters
#     ----------
#     arr_x : TYPE
#         DESCRIPTION.
#     arr_y : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     sensor_arr : TYPE
#         DESCRIPTION.
#     """

#     sensor_arr = []
#     # Check arr_x and arr_y must be at equal size
#     if not (len(arr_x) == len(arr_y)):
#         return sensor_arr
#     for i in range(len(arr_x)):
#         pos = Position(arr_x[i],arr_y[i])
#         sensor_arr.append(Sensor(pos))
#     return sensor_arr

# def initXGrid(area_w, voxel_w):

#     arr_x = []

#     n_x = int(area_w/voxel_w)
#     for i in range(n_x + 1):
#         arr_x.append(i * voxel_w)
#     return arr_x

# def initYGrid(area_l, voxel_l):

#     arr_y = []

#     n_y = int(area_l/voxel_l)
#     for i in range(n_y + 1):
#         arr_y.append(i * voxel_l)
#     return arr_y

# def initVoxelField(arr_x, arr_y, voxel_w, voxel_l, ref_pos):
#     """


#     Parameters
#     ----------
#     arr_x : TYPE
#         DESCRIPTION.
#     arr_y : TYPE
#         DESCRIPTION.
#     voxel_w : TYPE
#         DESCRIPTION.
#     voxel_l : TYPE
#         DESCRIPTION.
#     ref_pos : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     voxel_arr : TYPE
#         DESCRIPTION.

#     """

#     voxel_arr = []
#     n_x = len(arr_x)-1
#     n_y = len(arr_y)-1
#     for i in arr_x[0:n_x]:
#         for j in arr_y[0:n_y]:
#             idx = i * len(arr_y) + j
#             pos = Position(arr_x[i],arr_y[j])
#             voxel_arr.append(Voxel(idx, voxel_w, voxel_l, pos, 0, False, 0))

#     voxel_field = VoxelField(voxel_w, voxel_l, n_x, n_y, voxel_arr, ref_pos)
#     return voxel_field

# def initLinkArr(sensor_arr_a, sensor_arr_b):
#     """


#     Parameters
#     ----------
#     sensor_arr_a : TYPE
#         DESCRIPTION.
#     sensor_arr_b : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     link_arr : TYPE
#         DESCRIPTION.

#     """

#     link_arr = []
#     #
#     for sa in sensor_arr_a:
#         for sb in sensor_arr_b:
#             link_arr.append(RTILink(sa,sb, 0))
#     return link_arr

# def buildWeightingMatrix(link_arr, voxel_field, arr_x, arr_y, voxel_w, voxel_l):
#     """


#     Parameters
#     ----------
#     link_arr : TYPE
#         DESCRIPTION.
#     voxel_arr : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     None.

#     """
#     weightingMatrix = np.zeros(len(link_arr), len(voxel_field.voxel_arr))
#     binaryMatrix = np.zeros(len(link_arr), len(voxel_field.voxel_arr))
#     omegaMtrix = np.zeros(len(link_arr), len(voxel_field.voxel_arr))
#     # Looping each link
#     for l in link_arr:
#         # Loop Gird X find the ratio lambda by determining the intersection point.
#         intersection_arr = []
#         for i in arr_x:
#             # Find lambda of each value in Grid X
#             linkLambda = (i - l.sensor1.pos.x)/(l.sensor2.pos.x - l.sensor1.pos.x)
#             if linkLambda <= 1: # Check if the intercsection point is in the boudary
#                 # calculate y at any x on the defined grid
#                 y = l.sensor1.pos.y - linkLambda * (l.sensor2.pos.y - l.sensor1.pos.y)
#                 voxel_idx = voxel_field.findVoxelIdx(i, y) # find index in the array
#                 voxel_field.voxel_arr[voxel_idx] =



#         for j in arr_y:
#             # Find lambda of each value in Grid y
#             linkLambda = (j - l.sensor1.pos.y)/(l.sensor2.pos.y - l.sensor1.pos.y)
#             if linkLambda <= 1:
#                 intersection_arr.append(linkLambda)
#         # Alreary got all lambda at every intersection

#     # Calculate Selection Binary Matrix

#     # Calculate Omega Matrix (Corresponding coefficiecnts)



# # declare variables
# area_w = 4
# area_l = 10
# voxel_w = 1
# voxel_l = 1
# n_sensor = 18
# sensor_a_x = [0,0,0,0,0,0,0,0,0]
# sensor_a_y = [8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5]
# sensor_b_x = [6,6,6,6,6,6,6,6,6]
# sensor_b_y = [8.5,7.5,6.5,5.5,4.5,3.5,2.5,1.5,0.5]
# # Build Sensor Arrays
# sensor_arr_a = initSensorArr(sensor_a_x, sensor_a_y)
# sensor_arr_b = initSensorArr(sensor_b_x, sensor_b_y)
# # Calculate total link count
# n_link = len(sensor_arr_a) * len(sensor_arr_b)
# # Build Voxel Array
# arr_x = initXGrid(area_w, voxel_w)
# arr_y = initYGrid(area_l, voxel_l)
# voxel_field = initVoxelField(arr_x, arr_y, voxel_w, voxel_l, Position(1,0))
# # Build Link Array
# link_arr  = initLinkArr(sensor_arr_a, sensor_arr_b)
# # Model Weighting Matrix
# # WeightingMatrix = buildWeightingMatrix(link_arr, voxel_field)




