# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 14:08:27 2021

@author: krong
"""
import numpy as np
import os
import xlsxwriter
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
    
def result_record(path, title, excel_enabled, **record):
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
    fn_info = os.sep.join([fn_r, 'conclude.txt'])

    np.savetxt(fn_rx, record['x'], delimiter=',')
    np.savetxt(fn_ry, record['y'], delimiter=',')
    np.savetxt(fn_ref, record['ref'], delimiter=',')
    np.savetxt(fn_res, record['image'], delimiter=',')
    np.savetxt(fn_der_x, record['derivative']['x'],delimiter=',')
    np.savetxt(fn_der_y, record['derivative']['y'],delimiter=',')
    np.savetxt(fn_der_abs, record['derivative']['abs'],delimiter=',')
    
    with open(fn_info, 'w') as f:
        f.write(title + '\nRMSE = ' + str(record[RecordIndex.RMSE_ALL.name])
    + '\nAVG. OBJ. RMSE ,' + str(record[RecordIndex.RMSE_OBJ.name])
    + '\nAVG. NON. RMSE ,' + str(record[RecordIndex.RMSE_NON.name])
    + '\nAVG. OBJ. Attenuation ,' + str(record[RecordIndex.OBJ_MEAN.name])
    + '\nAVG. NON. Attenuation ,' + str(record[RecordIndex.NON_MEAN.name])
    + '\nAVG.')

    if excel_enabled:
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

def conclude_record(path, setting, ev):
    fn_conc = os.sep.join([path, 'conclusion.xlsx'])
    wb = xlsxwriter.Workbook(fn_conc)
    ws = {}
    
    
    for rs in ev.resultset:
        lb = rs.name
        ws[lb] = wb.add_worksheet(lb)
        if len(ev.paramset) > 1:
            col = 0    
            for i in range(len(ev.param1)):
                ws[lb].write(0, col, ev.paramset[0])
                ws[lb].write(1, col, ev.paramset[1])
                if len(ev.paramset) == 3:
                    ws[lb].write(2, col, ev.paramset[2])
                    r = 2
                    for l in ev.param3:
                        r += 1
                        ws[lb].write(r, col, l)
                col += 1
                ws[lb].write(0, col, ev.param1[i])
                for j in range(len(ev.param2)):
                    ws[lb].write(1, col+j, ev.param2[j])
                    if hasattr(ev, 'param3'):
                        r = 2
                        for k in range(len(ev.param3())):
                            ws[lb].write(k+2, col+j, ev.data[rs][i][j][k])
                    else:
                        if hasattr(ev, 'sample_size'):
                            for k in range(ev.sample_size):
                                ws[lb].write(k+2, col+j, ev.data[rs][i][j][k])
                        else:
                            ws[lb].write(2, col+j, ev.data[rs][i][j])
                col += (len(ev.param2)+2)
        else:
            col = 0
            ws[lb].write(0, col, ev.paramset[0])
            col += 1
            for i in range(len(ev.param1)):
                ws[lb].write(0, col + i, ev.param1[i])
                if hasattr(ev, 'sample_size'):
                    for j in range(ev.sample_size):
                        ws[lb].write((j+1), col + i, ev.data[rs][i][j])
                else:
                    ws[lb].write(1, col + i, ev.data[lb][i])
    wb.close()