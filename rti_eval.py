# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:54:08 2021

@author: krong
"""
import numpy as np
import math

from rti_rec import RecordIndex, result_record, conclude_record
from rti_plot import plotRTIIm, plotDerivative, process_boxplot, process_plot


class RTIEvaluation:
    def __init__(self, **kw):
        self.paramset = kw['paramset']
        if 'paramlabel' in kw:
            self.paramlabel = kw['paramlabel']
        else:
            self.paramlabel = self.paramset
        self.resultset = kw['resultset']
        self.gfx_enabled = False
        self.rec_enabled = False
        if 'gfx_enabled' in kw:
            self.gfx_enabled = kw['gfx_enabled']
        if 'der_plot_enabled' in kw:
            self.der_plot_enabled = kw['der_plot_enabled']
        if 'record_enabled' in kw:
            self.rec_enabled = kw['record_enabled']
        self.data = {}
        datadim = []
        if 'param1' in kw:
            self.param1 = kw['param1']
            datadim.append(len(kw['param1']))
        if 'param2' in kw:
            self.param2 = kw['param2']
            datadim.append(len(kw['param2']))
        if 'param3' in kw:
            self.param3 = kw['param3']
            datadim.append(len(kw['param3']))
        else:
            if 'sample_size' in kw and kw['sample_size'] > 1:
                self.sample_size = kw['sample_size']
                datadim.append(kw['sample_size'])
        for l in self.resultset:
            self.data[l] = np.zeros(datadim)

    def evaluate(self, sim, l_a, reF, imagE, savepath, key, **kw):
        # evaluation of RMSE
        r = RMSEEvaluation(reF, imagE)
        # evaluation of image derivative
        r.update(derivativeEval(reF, imagE))
        atitle = ''
        rec_e = self.rec_enabled
        if 'rec_enabled' in kw:
            rec_e = kw['rec_enabled']
        gfx_e = self.gfx_enabled
        if 'gfx_enabled' in kw:
            gfx_e = kw['gfx_enabled']
        der_plot = self.der_plot_enabled
        if 'der_plot_enabled' in kw:
            der_plot = kw['der_plot_enabled']
        if 'add_title' in kw:
            atitle = kw['add_title'] + '-'
        for i, e in enumerate(self.resultset):
            if len(self.data[e].shape) == 1:
                self.data[e][kw['data_idx1']] = r[e]
            elif len(self.data[e].shape) == 2:
                self.data[e][kw['data_idx1']][kw['data_idx2']] = r[e]
            elif len(self.data[e].shape) == 3:
                self.data[e][kw['data_idx1']][kw[
                    'data_idx2']][kw['data_idx3']] = r[e]
            else:
                raise ValueError('dimension mismatch')
        if rec_e:
            result_record(savepath['rec'],
                          key,
                          True,
                          x=sim.coorD(axis=0),
                          y=sim.coorD(axis=1),
                          ref=reF,
                          image=imagE,
                          ev=r)
        if gfx_e:
            plotRTIIm(sim.scheme,
                      imagE,
                      path=savepath['gfx'],
                      filename=sim.getTitle('', True) + '_' + key,
                      title=atitle + key + '-' + sim.getTitle(),
                      label='Rel. Attenuation',
                      rmse=r[RecordIndex.RMSE_ALL])
        if der_plot:
            plotDerivative(sim.scheme,
                           r,
                           path=savepath['gfx'],
                           filename=sim.getTitle('', True) + '_' + key,
                           title=atitle + key + '-' + sim.getTitle(),
                           label='Derivative of Attenuation',
                           caption='border@'
                           + '{:.3f}'.format(r[RecordIndex.DERIVATIVE_BORDERRATIO])
                           + ', '
                           + 'non-border@'
                           + '{:.3f}'.format(r[RecordIndex.DERIVATIVE_NONBORDERRATIO]))
        return r

    def conclude(self, savepath, setting, **kw):
        # record results
        conclude_record(savepath, setting, self)
        # show gfx
        if 'gfx' in kw:
            ptitle = ''
            if 'area_dimension' in setting:
                ptitle += ('a@(' + str(setting['area_dimension'][0]) + ','
                           + str(setting['area_dimension'][1]) + ')')
            if 'voxel_dimension' in setting:
                ptitle += ('v@(' + str(setting['voxel_dimension'][0]) + ','
                           + str(setting['voxel_dimension'][1]) + ')')
            if 'object_dimension' in setting:
                ptitle += ('o@(' + str(setting['object_dimension'][0]) + ','
                           + str(setting['object_dimension'][1]) + ')')
            if 'n_sensor' in setting:
                ptitle += 'n@' + str(setting['n_sensor'])
            if ptitle:
                ptitle += '-'
            if 'schemeType' in setting:
                ptitle += setting['schemeType']
            if 'weightalgorithm' in setting:
                ptitle += setting['weightalgorithm']
            if 'add_title' in kw:
                ptitle = kw['add_title'] + '-' + ptitle
            if kw['gfx'] == 'boxplot':
                for e in self.resultset:
                    yLabel = e.name
                    p = self.paramset[0]
                    xlabel = self.paramlabel[1]
                    for i, v in enumerate(self.param1):
                        tlv = p + '@' + str(v) + ptitle
                        process_boxplot(self.data[e][i].T,
                                        title=tlv,
                                        xlabel=xlabel,
                                        ylabel=yLabel,
                                        ticklabel=self.param2,
                                        path=savepath,
                                        filename=e.short + '-' + tlv)

                for e in self.resultset:
                    yLabel = e.name
                    p = self.paramset[1]
                    xlabel = self.paramlabel[0]
                    for i, v in enumerate(self.param2):
                        tlv = p + '@' + str(v) + ptitle
                        data = []
                        for j in range(len(self.param1)):
                            data.append(self.data[e][j][i])
                        process_boxplot(data,
                                        title=tlv,
                                        xlabel=xlabel,
                                        ylabel=yLabel,
                                        ticklabel=self.param1,
                                        path=savepath,
                                        filename=e.short + '-' + tlv)
            if kw['gfx'] == 'imshow':
                for e in self.resultset:
                    if hasattr(self, 'sample_size'):
                        dt = self.data[e].mean(axis=2)
                    else:
                        dt = self.data[e]
                    yLabel = e.name
                    plotRTIIm(kw['scheme'],
                              dt,
                              path=savepath,
                              filename=e.short + '-' + ptitle,
                              title=ptitle,
                              label=yLabel,
                              color='BrBG')
            if kw['gfx'] == 'plot':
                if hasattr(self, 'param2'):
                    raise Exception('plot process and parameter mismatch')
                process_plot(self.data,
                             title=ptitle,
                             path=savepath,
                             filename=ptitle,
                             xlabel=self.paramlabel[0],
                             X=self.param1,
                             **kw)
                i = 0
                for k, e in self.data.items():
                    process_plot(e,
                                 title=ptitle,
                                 path=savepath,
                                 filename=k.short + '-' + ptitle,
                                 xlabel=self.paramlabel[0],
                                 ylabel=k.name,
                                 graphindex=i,
                                 X=self.param1,
                                 **kw)
                    i += 1


def RMSEEvaluation(reF, reS):
    results = {}
    idx_obJ = (reF == 1)
    idx_noN = (reF == 0)

    results[RecordIndex.OBJ_MEAN] = reS[idx_obJ].mean()
    results[RecordIndex.NON_MEAN] = reS[idx_noN].mean()
    results[RecordIndex.OBJ_RATIO] = abs(results[RecordIndex.OBJ_MEAN]
                                         / results[RecordIndex.NON_MEAN])
    results[RecordIndex.RMSE_ALL] = math.sqrt(
        np.square(np.subtract(reF,
                              reS)).mean())
    results[RecordIndex.RMSE_OBJ] = math.sqrt(
        np.square(np.subtract(reF[idx_obJ],
                              reS[idx_obJ]))
        .mean())
    results[RecordIndex.RMSE_NON] = math.sqrt(
        np.square(np.subtract(reF[idx_noN],
                              reS[idx_noN]))
        .mean())
    return results


def derivativeEval(reF, reS):
    results = {}

    idx_obJ = (reF == 1)
    idx_bordeR = _getBorderIdx(idx_obJ, corner=1)
    idx_nonBordeR = (~idx_bordeR[0])
    idx_noN = (reF == 0)

    results[RecordIndex.DERIVATIVE_X] = calDerivative(reS,
                                                      axis='x',
                                                      direction='c')

    results[RecordIndex.DERIVATIVE_Y] = calDerivative(reS,
                                                      axis='y',
                                                      direction='c')

    results[RecordIndex.DERIVATIVE_ABS] = np.sqrt(results[RecordIndex
                                                          .DERIVATIVE_X
                                                          ]**2
                                                  + results[RecordIndex
                                                            .DERIVATIVE_Y
                                                            ]**2)

    results[RecordIndex.DERIVATIVE_MEAN] = results[RecordIndex
                                                   .DERIVATIVE_ABS
                                                   ].mean()

    results[RecordIndex.DERIVATIVE_OBJ] = (results[RecordIndex
                                                   .DERIVATIVE_ABS
                                                   ]
                                           [idx_obJ]
                                           .mean())
    results[RecordIndex.DERIVATIVE_NON] = (results[RecordIndex
                                                   .DERIVATIVE_ABS
                                                   ]
                                           [idx_noN]
                                           .mean())
    results[RecordIndex.DERIVATIVE_BORDER] = (results[RecordIndex
                                                      .DERIVATIVE_ABS
                                                      ]
                                              [idx_bordeR[0]]
                                              .mean())
    results[RecordIndex.DERIVATIVE_BORDER_X] = (results[RecordIndex
                                                        .DERIVATIVE_ABS
                                                        ]
                                                [idx_bordeR[1]]
                                                .mean())
    results[RecordIndex.DERIVATIVE_BORDER_Y] = (results[RecordIndex
                                                        .DERIVATIVE_ABS
                                                        ]
                                                [idx_bordeR[2]]
                                                .mean())
    results[RecordIndex.DERIVATIVE_NONBORDER] = (results[RecordIndex
                                                         .DERIVATIVE_ABS
                                                         ]
                                                 [idx_nonBordeR]
                                                 .mean())
    results[RecordIndex.DERIVATIVE_BORDERRATIO] = (results[RecordIndex
                                                           .DERIVATIVE_BORDER
                                                           ]
                                                   / results[RecordIndex
                                                             .DERIVATIVE_MEAN
                                                             ])
    results[RecordIndex.DERIVATIVE_BORDERRATIO_X] = (results[RecordIndex
                                                             .DERIVATIVE_BORDER_X
                                                             ]
                                                     / results[RecordIndex
                                                               .DERIVATIVE_MEAN
                                                               ])
    results[RecordIndex.DERIVATIVE_BORDERRATIO_Y] = (results[RecordIndex
                                                             .DERIVATIVE_BORDER_Y
                                                             ]
                                                     / results[RecordIndex
                                                               .DERIVATIVE_MEAN
                                                               ])
    results[RecordIndex.DERIVATIVE_NONBORDERRATIO] = (results[RecordIndex
                                                              .DERIVATIVE_NONBORDER
                                                              ]
                                                      / results[RecordIndex
                                                                .DERIVATIVE_MEAN
                                                                ])
    results[RecordIndex.DERIVATIVE_RATIO_BN] = (results[RecordIndex
                                                        .DERIVATIVE_BORDER
                                                        ]
                                                / results[RecordIndex
                                                          .DERIVATIVE_NONBORDER
                                                          ])
    results[RecordIndex.DERIVATIVE_RATIO_XN] = (results[RecordIndex
                                                        .DERIVATIVE_BORDER_X
                                                        ]
                                                / results[RecordIndex
                                                          .DERIVATIVE_NONBORDER
                                                          ])
    results[RecordIndex.DERIVATIVE_RATIO_YN] = (results[RecordIndex
                                                        .DERIVATIVE_BORDER_Y
                                                        ]
                                                / results[RecordIndex
                                                          .DERIVATIVE_NONBORDER
                                                          ])

    return results


def calDerivative(iM, **kw):
    axis = 'x'
    if 'axis' in kw:
        axis = kw['axis']
    direct = 'c'
    if 'direction' in kw:
        direct = kw['direction']

    kernel = np.zeros((3, 1))
    if direct == 'f':
        kernel[1] = -1
        kernel[2] = 1
    elif direct == 'c':
        kernel[0] = -1
        kernel[2] = 1
    elif direct == 'b':
        kernel[0] = -1
        kernel[1] = 1
    else:
        raise ValueError('derivative direction is not defined')

    if axis == 'x':
        pass
    elif axis == 'y':
        kernel = kernel.T
    else:
        raise ValueError('axis of derivative is not defined')

    return convolve2D(iM, kernel)


def convolve2D(iM, kernel, **kw):
    """
    Calculation of convolution between image and kernel

    Parameters
    ----------
    iM : 2D Numpy Array
        2D image matrix.
    kernel : 2D Numpy Array
        2D Filter.
    **kw : Keyword Arguments
        paddingDirection = {'c'|'b'|'f'}

    Raises
    ------
    ValueError
        Keyword Padding direction can only be {'c', 'f', 'b'}.
        Padding direction 'c' requires kernel size in odd number, i.e.,
        (3x3, 5x5, ...)
    Returns
    -------
    output : 2D Numpy Array
        DESCRIPTION.

    """
    padDir = 'c'
    if 'paddingDirection' in kw:
        padDir = kw['paddingDirection']

    k_x = kernel.shape[0]
    k_y = kernel.shape[1]

    iM_x = iM.shape[0]
    iM_y = iM.shape[1]

    padSize_x = k_x-1
    padSize_y = k_y-1

    temP = np.zeros((iM_x+padSize_x, iM_y+padSize_y))

    if padDir == 'c':
        if (padSize_x % 2 or padSize_y % 2):
            raise ValueError('Padding is not symmetric')
        padSize_x = int(padSize_x/2)
        padSize_y = int(padSize_y/2)

        temP[padSize_x:padSize_x
             + iM_x, padSize_y:padSize_y+iM_y] = iM
        for i in range(padSize_x):
            temP[i] = temP[padSize_x]
            idx = i+1
            temP[-idx] = temP[-(padSize_x+1)]
        for i in range(padSize_y):
            temP[:, i] = temP[:, padSize_y]
            idx = i+1
            temP[:, -1] = temP[:, -(padSize_y+1)]
    elif padDir == 'b':
        temP[padSize_x:iM_x + padSize_x, padSize_y:iM_y + padSize_y] = iM
        for i in range(padSize_x):
            temP[:, i] = temP[:, padSize_x]
        for i in range(padSize_y):
            temP[i] = temP[padSize_y]
    elif padDir == 'f':
        temP[0:iM_x, 0:iM_y] = iM
        for i in range(padSize_y):
            idx = i+1
            temP[:, -idx] = temP[:, -(padSize_y+1)]
        for i in range(padSize_y):
            temP[-(i+1)] = temP[-(padSize_y+1)]
    else:
        raise ValueError('Padding direction not defined')

    output = np.zeros((iM.shape[0], iM.shape[1]))
    for x in range(iM_x):
        for y in range(iM_y):
            output[x, y] = (kernel * temP[x:x+k_x, y:y+k_y]).sum()

    return output


def _getBorderIdx(idx_obJ, **kw):
    w = 1
    if 'width' in kw and kw['width'] > 0:
        w = kw['width']
    c = 0
    if 'corner' in kw and kw['corner'] > 0:
        c = kw['corner']
    bL = np.roll(idx_obJ, -1, axis=0)
    bL = (bL != idx_obJ)
    bR = np.roll(idx_obJ, 1, axis=0)
    bR = (bR != idx_obJ)
    bU = np.roll(idx_obJ, -1, axis=1)
    bU = (bU != idx_obJ)
    bD = np.roll(idx_obJ, 1, axis=1)
    bD = (bD != idx_obJ)

    for i in range(w-1):
        bL |= np.roll(bL, -1, axis=0)
        bR |= np.roll(bR, 1, axis=0)
        bU |= np.roll(bU, -1, axis=1)
        bD |= np.roll(bD, 1, axis=1)

    if c:
        bLU = np.roll(bL, -1, axis=1)
        bLD = np.roll(bL, 1, axis=1)
        bRU = np.roll(bR, -1, axis=1)
        bRD = np.roll(bR, 1, axis=1)

        bUR = np.roll(bU, -1, axis=0)
        bUL = np.roll(bU, 1, axis=0)
        bDR = np.roll(bD, -1, axis=0)
        bDL = np.roll(bD, 1, axis=0)

        for i in range(c-1):
            bLU |= np.roll(bLU, -1, axis=1)
            bLD |= np.roll(bLD, 1, axis=1)
            bRU |= np.roll(bRU, -1, axis=1)
            bRD |= np.roll(bRD, 1, axis=1)

            bUR |= np.roll(bU, -1, axis=0)
            bUL |= np.roll(bU, 1, axis=0)
            bDR |= np.roll(bD, -1, axis=0)
            bDL |= np.roll(bD, 1, axis=0)

    if 'setdirection' in kw:
        di = kw['setdirection']
        a = np.zeros(idx_obJ.shape)
        a = (a == 1)
        for ch in di:
            if ch == 'u':
                a |= bU
            elif ch == 'd':
                a |= bD
            elif ch == 'l':
                a |= bL
            elif ch == 'r':
                a |= bR
            elif ch == 'x':
                return bU | bD
            elif ch == 'y':
                return bL | bR
            else:
                raise ValueError('direction not defined')
            if c:
                if ('u' in di) and ('l' in di):
                    a |= (bUL | bLU)
                if ('u' in di) and ('r' in di):
                    a |= (bUR | bRU)
                if ('d' in di) and ('l' in di):
                    a |= (bDL | bLD)
                if ('d' in di) and ('r' in di):
                    a |= (bDR | bRD)
        return a
    else:
        if c:
            return [(bU | bD | bL | bR | bUL | bUR | bDL | bDR | bLU | bLD | bRU | bRD),
                    (bL | bR),
                    (bU | bD)]
            return [(bU | bD | bL | bR),
                    (bL | bR),
                    (bU | bD)]
