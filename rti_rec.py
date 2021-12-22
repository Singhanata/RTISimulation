# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 14:08:27 2021

@author: krong
"""
import numpy as np
import os
import xlsxwriter

def result_record(path, title, record):
    fn_r = os.sep.join([path, title])
    try:
        os.mkdir(fn_r)
    except:
        print('Folder ' + fn_r + ' is already exist')

    fn_rx = os.sep.join([fn_r, 'x.csv'])
    fn_ry = os.sep.join([fn_r, 'y.csv'])
    fn_ref = os.sep.join([fn_r, 'ref.csv'])
    fn_res = os.sep.join([fn_r, 'res.csv'])
    fn_der_x = os.sep.join([fn_r, 'derivative_x.csv'])
    fn_der_y = os.sep.join([fn_r, 'derivative_y.csv'])
    fn_der_abs = os.sep.join([fn_r, 'derivative_abs.csv'])

    np.savetxt(fn_rx, record['x'], delimiter=',')
    np.savetxt(fn_ry, record['y'], delimiter=',')
    np.savetxt(fn_ref, record['ref'], delimiter=',')
    np.savetxt(fn_res, record['image'], delimiter=',')
    np.savetxt(fn_der_x, record['derivative']['x'],delimiter=',')
    np.savetxt(fn_der_y, record['derivative']['y'],delimiter=',')
    np.savetxt(fn_der_abs, record['derivative']['abs'],delimiter=',')
    
    fn_excel = os.sep.join([fn_r, 'results.xlsx'])
    wb = xlsxwriter.Workbook(fn_excel)
    ws1 = wb.add_worksheet('xy')
    ws2 = wb.add_worksheet('ref')
    ws3 = wb.add_worksheet('image')
    ws4 = wb.add_worksheet('derivative_x')
    ws5 = wb.add_worksheet('derivative_y')
    ws6 = wb.add_worksheet('derivative_abs')
    ws7 = wb.add_worksheet('conclusion')
    
    if len(record['x']) > len(record['y']):
        n_min = len(record['y'])
        n_max = len(record['x'])
        for i in range(n_min):
            ws1.write(i, 0, record['x'][i])
            ws1.write(i, 1, record['y'][i])
        for i in range(n_min, n_max):    
            ws1.write(i, 0, record['x'][i])
    else:
        n_min = len(record['x'])
        n_max = len(record['y'])
        for i in range(n_min):
            ws1.write(i, 0, record['x'][i])
            ws1.write(i, 1, record['y'][i])
        for i in range(n_min, n_max):    
            ws1.write(i, 1, record['y'][i])
   
    shape = record['ref'].shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            ws2.write(i, j, record['ref'][i][j])
            ws3.write(i, j, record['image'][i][j])
            ws4.write(i, j, record['derivative']['x'][i][j])
            ws5.write(i, j, record['derivative']['y'][i][j])
            ws6.write(i, j, record['derivative']['abs'][i][j])
    
    rol = 0
    ws7.write(rol, 0, 'RMSE')
    rol += 1 
    for key, value in record['rmse'].items():        
        ws7.write(rol, 0, key)
        ws7.write(rol, 1, value)
        rol += 1
    ws7.write(rol, 0, 'DERIVATIVE')
    rol += 1
    ws7.write(rol, 0, 'border')
    ws7.write(rol, 1, record['derivative']['border'])
    rol += 1
    ws7.write(rol, 0, 'border_ratio')
    ws7.write(rol, 1, record['derivative']['border_ratio'])
    rol += 1
    ws7.write(rol, 0, 'non-border')
    ws7.write(rol, 1, record['derivative']['non-border'])
    rol += 1
    ws7.write(rol, 0, 'non-border_ratio')
    ws7.write(rol, 1, record['derivative']['non-border_ratio'])
    rol += 1
    ws7.write(rol, 0, 'non-derivative')
    ws7.write(rol, 1, record['derivative']['non-derivative'])
    rol += 1
    ws7.write(rol, 0, 'obj-derivative')
    ws7.write(rol, 1, record['derivative']['obj-derivative'])
    rol += 1
    
    wb.close()
    
    # with open(fn_info, 'w') as f:
    #     f.write(pre_fn + '\nRMSE = ' + str(r['rmse_all'])
    # + '\nAVG. OBJ. RMSE ,' + str(r['rmse_obj'])
    # + '\nAVG. NON. RMSE ,' + str(r['rmse_non'])
    # + '\nAVG. OBJ. Attenuation ,' + str(r['obj_mean'])
    # + '\nAVG. NON. Attenuation ,' + str(r['non_mean'])
    # + '\nAVG.')
