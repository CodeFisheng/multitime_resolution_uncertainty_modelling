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


class DemandFile:
    def __init__(self, *args):
        for count, thing in enumerate(args):
            if count == 0:
                arg1 = thing
            elif count == 1:
                arg2 = thing
        if count == 1:
            self.dataframe = importExcelData(arg1, arg2)
        elif count == 0:
            self.dataframe = arg1        
        self.date = self.dataframe['Date']
        self.date_ud = unduplicate(self.date)
        self.CusID = self.dataframe['CustomerID']
        self.CusID_ud = unduplicate(self.CusID)
    def getDataframeAll(self):
        return self.dataframe
    def getDate(self):
        return self.date
    def getCusID(self):
        return self.CusID
    def getCusID_ud(self):
        return self.CusID_ud
    def getDate_ud(self):
        return self.date_ud
       
class UncertaintyModel:
    def __init__(self, cus, uclist):
        self.customer = cus
        for case in switch(len(uclist)):
            if case(6):
                self.mean_uc1 = uclist[0]
                self.date_uc1 = uclist[1]
                self.tpnts_uc1 = uclist[2]
                self.uc_mean = uclist[3]
                self.uc_date = uclist[4]
                self.uc_tpnts = uclist[5]
                self.level = 1
                break
            if case(9):
                self.mean_uc1 = uclist[0]
                self.date_uc1 = uclist[2]
                self.tpnts_uc1 = uclist[4]
                self.mean_uc2 = uclist[1]
                self.date_uc2 = uclist[3]
                self.tpnts_uc2 = uclist[5]
                self.uc_mean = uclist[6]
                self.uc_date = uclist[7]
                self.uc_tpnts = uclist[8]
                self.level = 2
                break
            if case(12):
                self.mean_uc1 = uclist[0]
                self.date_uc1 = uclist[3]
                self.tpnts_uc1 = uclist[6]
                self.mean_uc2 = uclist[1]
                self.date_uc2 = uclist[4]
                self.tpnts_uc2 = uclist[7]
                self.mean_uc3 = uclist[2]
                self.date_uc3 = uclist[5]
                self.tpnts_uc3 = uclist[8]
                self.uc_mean = uclist[9]
                self.uc_date = uclist[10]
                self.uc_tpnts = uclist[11]
                self.level = 3
                break
            if case(15):
                self.mean_uc1 = uclist[0]
                self.date_uc1 = uclist[4]
                self.tpnts_uc1 = uclist[8]
                self.mean_uc2 = uclist[1]
                self.date_uc2 = uclist[5]
                self.tpnts_uc2 = uclist[9]
                self.mean_uc3 = uclist[2]
                self.date_uc3 = uclist[6]
                self.tpnts_uc3 = uclist[10]
                self.mean_uc4 = uclist[3]
                self.date_uc4 = uclist[7]
                self.tpnts_uc4 = uclist[11]
                self.uc_mean = uclist[12]
                self.uc_date = uclist[13]
                self.uc_tpnts = uclist[14]
                self.level = 4
                break
            if case():
                print "error in feeding uclist #3"
    def getlv(self):
        return self.level
    def getuc(self):
        return (self.mean_uc1, self.mean_uc2, self.mean_uc3, self.date_uc1, self.date_uc2, self.date_uc3, self.tpnts_uc1, self.tpnts_uc2, self.tpnts_uc3, self.uc_mean, self.uc_date, self.uc_tpnts)
        
        
class WaveletClass:
    def __init__(self, x, mwt, mode, level):
        self.x = x
        self.level = level
        self.motherwvlet = pywt.Wavelet('db1')
        self.mode = mode
    def get_uccomp(self):
        return self.uc
    def decompose(self):
        self.ca4, self.cd4, self.cd3, self.cd2, self.cd1 = pywt.wavedec(self.x, self.motherwvlet, mode = self.mode, level = self.level)
        self.data_d1 = pywt.waverec((0*self.ca4, 0*self.cd4, 0*self.cd3, 0*self.cd2, self.cd1), self.motherwvlet)
        self.data_a1 = pywt.waverec((self.ca4, self.cd4, self.cd3, self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_d2 = pywt.waverec((0*self.ca4, 0*self.cd4, 0*self.cd3, self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_a2 = pywt.waverec((self.ca4, self.cd4, self.cd3, 0*self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_d3 = pywt.waverec((0*self.ca4, 0*self.cd4, self.cd3, 0*self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_a3 = pywt.waverec((self.ca4, self.cd4, 0*self.cd3, 0*self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_d4 = pywt.waverec((0*self.ca4, self.cd4, 0*self.cd3, 0*self.cd2, 0*self.cd1), self.motherwvlet)
        self.data_a4 = pywt.waverec((self.ca4, 0*self.cd4, 0*self.cd3, 0*self.cd2, 0*self.cd1), self.motherwvlet)
        self.uc = self.data_d1 + self.data_d2 + self.data_d3
        #print self.ca4, self.cd4, self.cd3, self.cd2, self.cd1
        #print self.data_d1,self.data_a1
        #print self.data_d2,self.data_a2
        #print self.data_d3,self.data_a3
        #print self.data_d4,self.data_a4
    def plt_data(self, picname):
        t = np.array(range(48))
        losses = []
        label_a3 = r"uncertainty"
        label_d1 = r"high freq uncertainty"
        label_d2 = r"mid freq uncertainty"
        label_d3 = r"low freq uncertainty"
        fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        ax.plot([0,1,2], [10,20,3])
        pl = plt.subplot()
        pl.plot(t, self.uc, '-.', label=label_a3, linewidth=1.5)
        pl.plot(t, self.data_d3, '-.', label=label_d3, linewidth=0.5)
        pl.plot(t, self.data_d2, '-', label=label_d2, linewidth=0.5)
        pl.plot(t, self.data_d1, '-', label=label_d1, linewidth=0.5)
        pl.set_ylabel("Demand (kWh)",fontsize=14)
        pl.set_xlabel("Time (hr)",fontsize=14)
        pl.grid(True)
        pl.legend()
        #plt.plot(t,Prmse[24*day:24*(day+1)],'*',linewidth=2)
        plt.legend(loc='upper right', bbox_to_anchor=(0.7, .2), fontsize = 9)
        plt.savefig(picname)
    def get_uncertainty(self, level):
        #use different sentence for different decomposition levels
        for case in switch(level):
            if case(1):
                return (self.data_d1)
                break
            if case(2):
                return (self.data_d1, self.data_d2)
                break
            if case(3):
                return (self.data_d1, self.data_d2, self.data_d3)
                break
            if case(4):
                return (self.data_d1, self.data_d2, self.data_d3, self.data_d4)
                break
            if case():
                return (self.data_d1, self.data_d2, self.data_d3)
    
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
        
        
