# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:48:27 2021

@author: krong
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def plotRTIIm(scheme, iM, **kw):
    path = ''
    if 'path' in kw:
        path = kw['path']
    title = ''
    if 'title' in kw:
        title = kw['title']
    label = ''
    if 'label' in kw:
        label = kw['label']
    sensorPosition = scheme.getSensorPosition()
    if 'sensorPosition' in kw:
        sensorPosition = kw['sensorPosition']
    rmse=-1
    if 'rmse' in kw:
        rmse = kw['rmse']
    color='coolwarm'
    if 'color' in kw:
        color = kw['color']
    s_sensor = True
    if 'show_sensor' in kw:
        s_sensor = kw['show_sensor']
    s_marker = 's'
    if 'sensor_marker' in kw:
        s_marker = kw['sensor_marker']
    s_color = 'black'
    if 'sensor_color' in kw:
        s_color = kw['sensor_color']
        
    sel = scheme.selection

    coordX = np.asarray(sel.coordX)
    coordY = np.asarray(sel.coordY)

    fig, ax = plt.subplots(1, 1)
    hm = ax.imshow(iM.T,
                   extent=[coordX[0], coordX[-1], coordY[0], coordY[-1]],
                   cmap=color,
                   origin='lower',
                   interpolation='nearest',
                   vmin=0)
    ax.set_title(title, pad=10)
    ax.set_ylabel('[m]')
    xlabel = '[m]'
    if rmse >= 0: xlabel += '\nRMSE =' + str(rmse)
    ax.set_xlabel(xlabel)
    cb = plt.colorbar(hm)
    if label: cb.set_label(label)
    if s_sensor and len(sensorPosition) > 0:
        plt.scatter(sensorPosition[0],
                    sensorPosition[1],
                    s=150,
                    c=s_color,
                    marker=s_marker)
    plt.grid()
    if path:        
        fn = path + '.svg'
        plt.savefig(fn)
    plt.show()

def plotSurface(scheme, Z, **kw):
    path = ''
    if 'path' in kw:
        path = kw['path']
    title = ''
    if 'title' in kw:
        title = kw['title']
    label = ''
    if 'label' in kw:
        label = kw['label']
    color = cm.coolwarm
    if 'color' in kw:
        color = kw['color']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = np.asarray(scheme.selection.coordX)
    y = np.asarray(scheme.selection.coordY)

    X, Y = np.meshgrid(x, y)

    # Plot the surface.
    surf = ax.plot_surface(X, 
                           Y, 
                           Z, 
                           cmap=color,
                           linewidth=0, 
                           antialiased=False)

    # Customize the z axis.
    mn = min(Z)
    mx = max(Z)
    ax.set_zlim(mn-0.05*abs(mn), mx + 0.05*abs(mx))

    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')
    ax.set_xlabel('x[m]')
    ax.set_ylabel('y[m]')
    if title: ax.set_title(title)
    # Add a color bar which maps values to colors.
    cb = fig.colorbar(surf,
                     shrink=0.5,
                     aspect=5)
    if label: cb.set_label(label)
    if path:        
        fn = path + '.svg'
        plt.savefig(fn)

    plt.show()