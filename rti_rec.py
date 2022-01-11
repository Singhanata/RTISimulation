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
    X = 0
    Y = 1
    REF = 2
    IMAGE = 3
    DERIVATIVE_X = 4
    DERIVATIVE_Y = 5
    DERIVATIVE_ABS = 6
    DERIVATIVE_MEAN = 7
    DERIVATIVE_OBJ = 8
    DERIVATIVE_NON = 9
    DERIVATIVE_BORDER = 10
    DERIVATIVE_NONBORDER = 11
    DERIVATIVE_BORDERRATIO = 12
    DERIVATIVE_NONBORDERRATIO = 13
    DERIVATIVE_BORDER_X = 14
    DERIVATIVE_BORDERRATIO_X = 15
    DERIVATIVE_BORDER_Y = 16
    DERIVATIVE_BORDERRATIO_Y = 17
    DERIVATIVE_RATIO_BN = 18
    DERIVATIVE_RATIO_XN = 19
    DERIVATIVE_RATIO_YN = 20
    OBJ_MEAN = 21
    NON_MEAN = 22
    OBJ_RATIO = 23
    RMSE_ALL = 24
    RMSE_OBJ = 25
    RMSE_NON = 26
    
    def getDERIndex():
        return 4
    def getEVIndex():
        return 7
    def getOBJIndex():
        return 21
    def getRMSEIndex():
        return 24
    @property
    def short(self):
        return {
            RecordIndex.X : 'X',
            RecordIndex.Y : 'Y',
            RecordIndex.REF : 'REF',
            RecordIndex.IMAGE : 'IM',
            RecordIndex.DERIVATIVE_X : 'DE_X',
            RecordIndex.DERIVATIVE_Y : 'DE_Y',
            RecordIndex.DERIVATIVE_ABS : 'DE_ABS',
            RecordIndex.DERIVATIVE_MEAN : 'DE_M',
            RecordIndex.DERIVATIVE_OBJ : 'DE_O',
            RecordIndex.DERIVATIVE_NON : 'DE_N',
            RecordIndex.DERIVATIVE_BORDER : 'DE_B',
            RecordIndex.DERIVATIVE_NONBORDER : 'DE_NB',
            RecordIndex.DERIVATIVE_BORDERRATIO : 'DE_BR',
            RecordIndex.DERIVATIVE_NONBORDERRATIO : 'DE_NBR',
            RecordIndex.DERIVATIVE_BORDER_X : 'DE_BX',
            RecordIndex.DERIVATIVE_BORDERRATIO_X :'DE_BRX',
            RecordIndex.DERIVATIVE_BORDER_Y : 'DE_BY',
            RecordIndex.DERIVATIVE_BORDERRATIO_Y : 'DE_BRY',
            RecordIndex.DERIVATIVE_RATIO_BN : 'DE_R_BN',
            RecordIndex.DERIVATIVE_RATIO_XN : 'DE_R_XN',
            RecordIndex.DERIVATIVE_RATIO_YN : 'DE_R_YN',
            RecordIndex.OBJ_MEAN : 'OBJ',
            RecordIndex.NON_MEAN : 'NON',
            RecordIndex.OBJ_RATIO : 'R_ON',
            RecordIndex.RMSE_ALL : 'RMSE',
            RecordIndex.RMSE_OBJ : 'RMSE_O',
            RecordIndex.RMSE_NON : 'RMSE_N'
            }.get(self)
    
def result_record(path, title, 
                  excel_enabled = True, 
                  text_enabled = True, **record):
    fn_r = os.sep.join([path, title])
    try:
        os.mkdir(fn_r)
    except:
        print('Folder ' + fn_r + ' is already exist')
    if 'text_enabled': 
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
        np.savetxt(fn_der_x, record['ev'][RecordIndex.DERIVATIVE_X],delimiter=',')
        np.savetxt(fn_der_y, record['ev'][RecordIndex.DERIVATIVE_Y],delimiter=',')
        np.savetxt(fn_der_abs, record['ev'][RecordIndex.DERIVATIVE_ABS],
                   delimiter=',')
        
        st = title
        for k, v in record['ev'].items():
            if k.value >= RecordIndex.getEVIndex():
                st += '\n' + k.name + '=' + str(v)
        with open(fn_info, 'w') as f:
            f.write(st)

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
                ws4.write(i, j, record['ev'][RecordIndex.DERIVATIVE_X][i][j])
                ws5.write(i, j, record['ev'][RecordIndex.DERIVATIVE_Y][i][j])
                ws6.write(i, j, record['ev'][RecordIndex.DERIVATIVE_ABS][i][j])
        
        rol = 0
        for key, value in record['ev'].items():
            if key.value < RecordIndex.getEVIndex():
                continue
            else:
                ws7.write(rol, 0, key.name)
                ws7.write(rol, 1, value)
            rol += 1
        wb.close()

def conclude_record(path, setting, ev):
    fn_conc = os.sep.join([path, 'conclusion.xlsx'])
    wb = xlsxwriter.Workbook(fn_conc)
    ws = {}
    ws['setting'] = wb.add_worksheet('setting')
    rol = 0
    for ke, vl in setting.items():
        ws['setting'].write(rol, 0, ke)
        ws['setting'].write(rol, 1, str(vl))
        rol += 1
                
    for rs in ev.resultset:
        lb = rs.name
        ws[lb] = wb.add_worksheet(lb)
        if (hasattr(ev, 'param1') 
            and not hasattr(ev, 'param2') 
            and not hasattr(ev, 'param3')):
            col = 0
            ws[lb].write(0, col, ev.paramset[0])
            col += 1
            for i in range(len(ev.param1)):
                ws[lb].write(0, col + i, ev.param1[i])
                if hasattr(ev, 'sample_size'):
                    for j in range(ev.sample_size):
                        ws[lb].write((j+1), col + i, ev.data[rs][i][j])
                else:
                    ws[lb].write(1, col + i, ev.data[rs][i])
        elif (hasattr(ev, 'param1') 
            and hasattr(ev, 'param2') 
            and not hasattr(ev, 'param3')):
            if hasattr(ev, 'sample_size'):
                col = 0    
                for i in range(len(ev.param1)):
                    ws[lb].write(0, col, ev.paramset[0])
                    ws[lb].write(1, col, ev.paramset[1])
                    col += 1
                    ws[lb].write(0, col, ev.param1[i])
                    for j in range(len(ev.param2)):
                        ws[lb].write(1, col+j, ev.param2[j])
                        for k in range(ev.sample_size):
                            ws[lb].write(k+2, col+j, ev.data[rs][i][j][k])
                    col += (len(ev.param2)+2)
            else:
                ws[lb].write(0, 0, ev.paramset[0])
                ws[lb].write(0, 1, ev.paramset[1])
                for i, v1 in enumerate(ev.param1):
                    ws[lb].write(1+i, 0, v1)
                    for j, v2 in enumerate(ev.param2):
                        ws[lb].write(0, 2+j, v2)
                        ws[lb].write(1+i, 2+j, ev.data[rs][i][j])
        elif (hasattr(ev, 'param1') 
            and hasattr(ev, 'param2') 
            and hasattr(ev, 'param3')):
            if hasattr(ev, 'sample_size'):
                raise ValueError('sample size of 3 parameter set not defined')
            col = 0
            for i, v1 in enumerate(ev.param1):
                ws[lb].write(0, col, ev.paramset[0])
                ws[lb].write(1, col, ev.paramset[1])
                ws[lb].write(2, col, ev.paramset[2])
                
                ws[lb].write(0, col+1, v1)
                for j, v2 in enumerate(ev.param1):
                    ws[lb].write(1, col+1+j, v2)
                    for k, v3 in enumerate(ev.param1):
                        ws[lb].write(3+k, col, v3)
                        ws[lb].write(3+k, col+1+j, ev.data[rs][i][j][k])
                col += (len(ev.param2)+2)
        else:
            pass
            
    wb.close()