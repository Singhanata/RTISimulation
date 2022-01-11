# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:12:11 2022

@author: krong
"""

from rti_eval import RTIEvaluation, RecordIndex
from rti_sim_input import simulateInput, sim_trajectory

def process_animate(sim):
    """
    This process animates an RTI scenario.

    Parameters
    ----------
    sim : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    setting = {
        #scenario setting
        'title':'animation',
        'area_dimension':(10.,10.),
        'voxel_dimension':(0.20,0.20),
        'sensing_area_position':(9.,9.),
        # 'n_sensor':20,
        'alpha': 1, 
        'schemeType':'RE',
        'weightalgorithm':'EX',
        # 'object_dimension': (0.5, 0.5),
        'object_type': 'human',
        #sample setting        
        'SNR': 4,
        'SNR_mode' : 2,
        # 'sample_size' : 100,
        #input setting
        'paramset': ['obj_pos'],
        'paramlabel': ['Object Position'],
        # 'param1' : np.linspace(8, 64, 15),
        # 'param2' : ['LS1','LS2','EL','EX','IN'],
        #output setting
        'gfx_enabled' : True,
        'record_enabled' : False,
        'der_plot_enabled': False,
        'frame_rate' : 30,
        'resultset':[
            RecordIndex.RMSE_ALL,
            RecordIndex.OBJ_RATIO,
            RecordIndex.DERIVATIVE_RATIO_BN]
        }

    savepath = sim.process_routine(**setting)

    startpoint = (5.0, 5.0)
    traject_info = [[1, setting['frame_rate'], 'lin', [(7.5, 8.0),
                                   (0.63, 0.20),
                                   (0.19, 0.28),
                                   (0.43, 0.39),
                                   (0.23, 0.88),
                                   (0.32, 0.70),
                                   (0.45, 0.61)]]]
    setting['param1'] = sim_trajectory(startpoint, traject_info)
    ev = RTIEvaluation(**setting)
    for idx, v in enumerate(setting['param1']):
        refInput = simulateInput(sim.scheme,
                          sim.calculator,
                          v,
                          **setting)
        for key, value in refInput.items():
            # calculate image
            iM = (sim.estimator.calVoxelAtten(value[0], True))
            ev.evaluate(sim,                        # RTI Simulation
                        value[0],                   # Link Attenuation
                        value[1],                   # Reference
                        iM,                         # Image
                        savepath,                   # Result Folder
                        key,                        # Information of sample
                        # data index
                        data_idx1 = idx,            # data index 1
                        # data_idx2 = idx_snr,        # data index 2
                        # data_idx3 = value[2],       # data index 3
                        # adding title
                        # add_title = r'$\alpha$' + '@' + str(al)
                        )
    ev.conclude(savepath['conc'], setting, 
                # add_title = f's@{setting["sample_size"]}',
                gfx = '')            
    # fig, ax, hm = plotRTIIm(sim.scheme,
    #         iM, 
    #         path = savepath['gfx'],
    #         filename = sim.getTitle('', True),
    #         title = sim.getTitle(), 
    #         label = 'Rel. Attenuation',
    #         anime = True)

    # # stD = np.zeros(iM.shape)
    # time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    # ax.set_autoscale_on(False)
    # dt = 1/setting['frame_rate']
    
    # def init():
    #     hm.set_data(stD)
    #     time_text.set_text('')
    #     return hm, time_text
    
    # def animate(i):
    # for i in range(len(setting['param1'])):
    #     refInput = simulateInput(sim.scheme,
    #                      sim.calculator,
    #                      setting['param1'][i],
    #                      **setting)
    #     v = list(refInput.values())
    #     iM = (sim.estimator.calVoxelAtten(v[0][0], True))
    #     hm.set_data(iM)
    #     time_text.set_text('time = %.1f' % dt*i)
        
    #     plt.show()
        # plt.draw()
        
        # return hm, time_text
        
    # interval = dt * len(setting['param1'])
    
    # ani = animation.FuncAnimation(fig, animate, frames=30,
    #                           interval=interval, blit=True, init_func=init)
    # ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    # plt.show()