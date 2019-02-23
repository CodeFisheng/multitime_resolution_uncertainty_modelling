import random as rd
import math
import pandas as pd
import numpy as np
import datetime
import time
from IPython.display import Image
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from pylab import *

def importExcelData(filename,sheet):
    xls = pd.ExcelFile(filename)
    dataframe = xls.parse(sheet)
    return dataframe
def date2str(timestamp):
    date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    date_str_short = timestamp.strftime("%Y-%m-%d")
    return date_str, date_str_short
def str2date(timestr):
    ifshort = False
    date_str = ""
    date_str_short = ""
    if len(timestr) < 15:
        date_str_short = timestr
        ifshort = True
    else:
        date_str = timestr
        ifshort = False
    #print ifshort
    if ifshort:
        dt_obj = pd.Timestamp(datetime.datetime.strptime(date_str_short, "%Y-%m-%d"))
    else:
        dt_obj = pd.Timestamp(datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
    return dt_obj
def unduplicate(listname):
    ud_list = list(set(listname))
    ud_list.sort()
    return ud_list
def cal_uc_std_mean(x):
    return np.std(x)
def cal_uc_std_tpnts(x):
    ret = np.zeros(x.shape)
    ind = 0
    for z in x:
        ret[ind] = z
        ind = ind + 1
    return np.std(ret, axis = 0)
def cal_uc_std_date(x):
    ret = np.zeros(x.shape)
    ind = 0
    for z in x:
        ret[ind] = z
        ind = ind + 1
    return np.std(ret, axis = 1)
def trycolor(data, color = cm.Blues):
    zdata = np.array(data)
    im = plt.matshow(zdata, cmap=color, aspect='auto') # pl is pylab imported a pl
    plt.colorbar(im)
    plt.title(color)
    plt.show()
def uc_customer(meanlist1, meanlist2, meanlist3, color = cm.Blues):
    t = np.array(range(len(meanlist1)))
    losses = []
    label_1 = r"high freq uncertainty"
    label_2 = r"mid freq uncertainty"
    label_3 = r"low freq uncertainty"
    fig, ax = plt.subplots( nrows=1, ncols=1,  figsize=(13, 5))  # create figure & 1 axis
    ax.plot([0,1,2], [10,20,3])
    pl = plt.subplot(111)
    pl.bar(t+1-0.2, meanlist1, label=label_1, width=0.16, color = 'r', align = 'center')
    pl.bar(t+1, meanlist2, label=label_2, width=0.16, color = 'g', align = 'center')
    pl.bar(t+1+0.2, meanlist3, label=label_3, width=0.16, color = 'b', align = 'center')
    pl.set_ylabel("Uncertainty (std-kWh)",fontsize=14)
    pl.set_xlabel("Time (hr)",fontsize=14)
    pl.grid(True)
    pl.legend()
    #plt.plot(t,Prmse[24*day:24*(day+1)],'*',linewidth=2)
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize = 9)
    plt.show()
    print 'average std in high frequency level: '+str(np.mean(meanlist1))
    print 'average std in mid frequency level: '+str(np.mean(meanlist2))
    print 'average std in low frequency level: '+str(np.mean(meanlist3))
def uc_parameters_customer_3d(data, color = cm.Blues):
    #===============
    # subplot 1
    #===============
    # 3D analysis
    zdata = data
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(2, 1, 2, projection='3d')
    # Make data.
    X = np.arange(0, np.array(zdata).shape[0], 1)
    Y = np.arange(0, np.array(zdata).shape[1], 1)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    ZZ = np.sin(R)
    Z = np.array(zdata).T
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.Blues,
                           linewidth=0, antialiased=False, shade = True, color = 'g')
    ax.set_ylabel("Date (days)",fontsize=14)
    ax.set_xlabel("Customer (index)",fontsize=14)
    ax.set_zlabel("Uncertainty (std-kWh)",fontsize=14)
    # Customize the z axis.
    ax.set_zlim(0, 1)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    print """


    Figure 1 3d demand uncertainty in differing Dates and differing Customers
    """
    plt.show()
def uc_parameters_customer_heat(data, color = cm.Blues):
    zdata = data
    im = plt.matshow(zdata, cmap=color, aspect='auto') # pl is pylab imported a pl
    plt.colorbar(im)
    plt.title(color)
    print """


    Figure 2 uncertainty heatmap in differing Dates and differing Customers
    """
    plt.show()
def uc_parameters(data, color = cm.Blues):
    zdata1 = np.mean(data, axis = 0)
    t = np.array(range(len(zdata1)))
    fig, ax = plt.subplots( nrows=1, ncols=1,  figsize=(14, 4))  # create figure & 1 axis
    ax.plot([0,1,2], [10,20,3])
    pl = plt.subplot()
    pl.bar(t, zdata1,  width=0.16, color = 'g', align = 'center')
    pl.set_ylabel("Uncertainty (std-kWh)",fontsize=14)
    pl.set_xlabel("Date (days)",fontsize=14)
    pl.grid(True)
    pl.legend()
    #plt.plot(t,Prmse[24*day:24*(day+1)],'*',linewidth=2)
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize = 9)
    print """


    Figure 3 average customer uncertainty in differing Dates
    """
    plt.show()
def uc_dayofweek(data, color = cm.Blues):
    zdata1 = np.mean(data, axis = 0)
    print zdata1.shape
    zdata2 = zdata1.reshape((zdata1.shape[0]/7,7))
    print zdata2.shape
    zdata3 = np.mean(zdata2, axis = 0)
    t = np.array(range(len(zdata3)))
    fig, ax = plt.subplots( nrows=1, ncols=1,  figsize=(14, 4))  # create figure & 1 axis
    ax.plot([0,1,2], [10,20,3])
    pl = plt.subplot()
    pl.plot(t, zdata3, '-.', linewidth=1)
    pl.set_ylabel("Uncertainty (std-kWh)",fontsize=14)
    pl.set_xlabel("Date (days)",fontsize=14)
    pl.grid(True)
    pl.legend()
    #plt.plot(t,Prmse[24*day:24*(day+1)],'*',linewidth=2)
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize = 9)
    print """


    Figure 4 average customer uncertainty in differing Days of Week
    """
    plt.show()
def list_all_color_config(data):
    zdata = np.array(data)
    for cmaps in colormaps():
        plt.rc('font', family='serif')
        fig = plt.figure(figsize=(8, 8/1.618))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('The x values')
        ax.set_ylabel('The y values')
        plt.rc('font', family = 'serif', serif = 'Times')
        plt.rc('xtick', labelsize = 8)
        plt.rc('ytick', labelsize = 8)
        plt.rc('axes', labelsize = 8)
        color = cm.Accent
        im = ax.matshow(data, cmap=color, aspect='auto') # pl is pylab imported a pl
        plt.colorbar(im)
        plt.title(color)
        ax.set_xlabel('Time (hr)')
        ax.set_ylabel('Demand Uncertainty (kWh)')
        plt.show()
def list_all_color_config_3d(data):
    zdata = data
    # 3D selecting surface figure
    X = np.arange(0, np.array(zdata).shape[0], 1)
    Y = np.arange(0, np.array(zdata).shape[1], 1)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    ZZ = np.sin(R)
    Z = np.array(zdata).T
    for cmap in colormaps():
        fig = figure(figsize = (8, 5))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap= cmap)
        title(cmap)