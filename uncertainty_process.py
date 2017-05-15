import pandas as pd
import numpy as np
import math
import random as rd
import pywt
from utils import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from pylab import *
from demand_model import *
def get_raw_uncertainty(inputs, DCL):
    uc1 = []
    uc2 = []
    uc3 = []
    uc = []
    for ipt in inputs:
        wc = WaveletClass(ipt, 'haar', 'constant', 4)
        wc.decompose()
        (tmp1, tmp2, tmp3) = wc.get_uncertainty(3)
        tmpuc = wc.get_uccomp()
        uc1.append(tmp1)
        uc2.append(tmp2)
        uc3.append(tmp3)
        uc.append(tmpuc)
    uc1 = np.array(uc1)
    uc2 = np.array(uc2)
    uc3 = np.array(uc3)
    uc = np.array(uc)
    return [uc1, uc2, uc3, uc]
def uc_process(inputs,DCL):
    uc1 = []
    uc2 = []
    uc3 = []
    uc = []
    for ipt in inputs:
        wc = WaveletClass(ipt, 'haar', 'constant', 4)
        wc.decompose()
        for case in switch(DCL):
            if case(1):
                (tmp1) = wc.get_uncertainty(3)
                tmpuc = wc.get_uccomp()
                uc1.append(tmp1)
                uc.append(tmpuc)
                break
            if case(2):
                (tmp1, tmp2) = wc.get_uncertainty(3)
                tmpuc = wc.get_uccomp()
                uc1.append(tmp1)
                uc2.append(tmp2)
                uc.append(tmpuc)
                break
            if case(3):
                (tmp1, tmp2, tmp3) = wc.get_uncertainty(3)
                tmpuc = wc.get_uccomp()
                uc1.append(tmp1)
                uc2.append(tmp2)
                uc3.append(tmp3)
                uc.append(tmpuc)
                break
            if case(4):
                (tmp1, tmp2, tmp3, tmp4) = wc.get_uncertainty(3)
                tmpuc = wc.get_uccomp()
                uc1.append(tmp1)
                uc2.append(tmp2)
                uc3.append(tmp3)
                uc4.append(tmp4)
                uc.append(tmpuc)
                break
            if case():# in default situation, go for decomposition level = 3
                (tmp1, tmp2, tmp3) = wc.get_uncertainty(3)
                tmpuc = wc.get_uccomp()
                uc1.append(tmp1)
                uc2.append(tmp2)
                uc3.append(tmp3)
                uc.append(tmpuc)
    ## uc modelling step 2: create uc model class
    for case in switch(DCL):
        if case(1):
            uc1 = np.array(uc1)
            uc = np.array(uc)
            ucm = cal_uc_std_mean(uc)
            ucd = cal_uc_std_date(uc)
            uct = cal_uc_std_tpnts(uc)
            umm1 = cal_uc_std_mean(uc1)
            umd1 = cal_uc_std_date(uc1)
            umt1 = cal_uc_std_tpnts(uc1)
            uclist = [umm1, umd1, umt1, ucm, ucd, uct]
            break
        if case(2):
            uc1 = np.array(uc1)
            uc2 = np.array(uc2)
            uc = np.array(uc)
            ucm = cal_uc_std_mean(uc)
            ucd = cal_uc_std_date(uc)
            uct = cal_uc_std_tpnts(uc)
            umm1 = cal_uc_std_mean(uc1)
            umm2 = cal_uc_std_mean(uc2)
            umd1 = cal_uc_std_date(uc1)
            umd2 = cal_uc_std_date(uc2)
            umt1 = cal_uc_std_tpnts(uc1)
            umt2 = cal_uc_std_tpnts(uc2)
            uclist = [umm1, umm2, umd1, umd2, umt1, umt2, ucm, ucd, uct]
            break
        if case(3):
            uc1 = np.array(uc1)
            uc2 = np.array(uc2)
            uc3 = np.array(uc3)
            uc = np.array(uc)
            ucm = cal_uc_std_mean(uc)
            ucd = cal_uc_std_date(uc)
            uct = cal_uc_std_tpnts(uc)
            umm1 = cal_uc_std_mean(uc1)
            umm2 = cal_uc_std_mean(uc2)
            umm3 = cal_uc_std_mean(uc3)
            umd1 = cal_uc_std_date(uc1)
            umd2 = cal_uc_std_date(uc2)
            umd3 = cal_uc_std_date(uc3)
            umt1 = cal_uc_std_tpnts(uc1)
            umt2 = cal_uc_std_tpnts(uc2)
            umt3 = cal_uc_std_tpnts(uc3)
            uclist = [umm1, umm2, umm3, umd1, umd2, umd3, umt1, umt2, umt3, ucm, ucd, uct]
            break
        if case(4):
            uc1 = np.array(uc1)
            uc2 = np.array(uc2)
            uc3 = np.array(uc3)
            uc4 = np.array(uc4)
            uc = np.array(uc)
            ucm = cal_uc_std_mean(uc)
            ucd = cal_uc_std_date(uc)
            uct = cal_uc_std_tpnts(uc)
            umm1 = cal_uc_std_mean(uc1)
            umm2 = cal_uc_std_mean(uc2)
            umm3 = cal_uc_std_mean(uc3)
            umm4 = cal_uc_std_mean(uc4)
            umd1 = cal_uc_std_date(uc1)
            umd2 = cal_uc_std_date(uc2)
            umd3 = cal_uc_std_date(uc3)
            umd4 = cal_uc_std_date(uc4)
            umt1 = cal_uc_std_tpnts(uc1)
            umt2 = cal_uc_std_tpnts(uc2)
            umt3 = cal_uc_std_tpnts(uc3)
            umt4 = cal_uc_std_tpnts(uc4)
            uclist = [umm1, umm2, umm3, umm4, umd1, umd2, umd3, umd4, umt1, umt2, umt3, umt4, ucm, ucd, uct]
            break
        if case():# in default situation, go for decomposition level = 3
            uc1 = np.array(uc1)
            uc2 = np.array(uc2)
            uc3 = np.array(uc3)
            uc = np.array(uc)
            ucm = cal_uc_std_mean(uc)
            ucd = cal_uc_std_date(uc)
            uct = cal_uc_std_tpnts(uc)
            umm1 = cal_uc_std_mean(uc1)
            umm2 = cal_uc_std_mean(uc2)
            umm3 = cal_uc_std_mean(uc3)
            umd1 = cal_uc_std_date(uc1)
            umd2 = cal_uc_std_date(uc2)
            umd3 = cal_uc_std_date(uc3)
            umt1 = cal_uc_std_tpnts(uc1)
            umt2 = cal_uc_std_tpnts(uc2)
            umt3 = cal_uc_std_tpnts(uc3)
            uclist = [umm1, umm2, umm3, umd1, umd2, umd3, umt1, umt2, umt3, ucm, ucd, uct, ucm, ucd, uct]
    #picname = "pic/decompose-cus(" + str(Cus) + ')-date-(' + Date + ").png"
    #wc.plt_data(picname)
    #Image(picname, width=1100)
    return uclist
