# -*- coding: utf-8 -*-
"""
@author: Dr. Martin Hell
"""
#import cora.core
#import cora.core.calibration
import CoraClassHell
import Cora_tools_v2 as tools
import collections
import cv2
import datetime
import glob
import itertools
import json
import time
import sys
import os
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as ticker
import numpy as np
import natsort 
import pandas as pd
import re
import spafile
import serial
import serial.tools.list_ports



from assembling_orca import Orca#, MeasurementMode
from collections import defaultdict
from cora.core.interpolation import get_evenspaced_spectrum, match_x_axes
from cora.core.calibration import relative_intensity_correction, y_axis
from CoreControllGui import Ui_MainWindow
from CoraClassHell import numericalSort
from CoraClassHell import status
from CoraClassHell import statushalf
from CoraClassHell import exp_fit
from CoraClassHell import line_fit
from CoraClassHell import save
from CoraClassHell import Gauss
from CoraClassHell import lorentzian
from CoraClassHell import create785ax
from CoraClassHell import create1064ax
from CoraClassHell import sliderset
from CoraClassHell import slidercall
from CoraClassHell import spadarkextract
from CoraClassHell import starmarker
from CoraClassHell import CoreSet
from CoraClassHell import readprofiles
from CoraClassHell import createfolder
from CoraClassHell import CoreSet
from CoraClassHell import grap
from datetime import date
from datetime import datetime, date
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import dates, pyplot
from matplotlib.ticker import MaxNLocator
from pathlib import Path
from prologix_gpib_osa import OSA_AQ6315A, SerialPorts
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QSlider, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QMenu, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap, QScreen
from scipy.integrate import simps
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import integrate
from USBswitch import set_channel
from serial.tools import list_ports
from serial.tools.list_ports_windows import comports

class EmbedPlotUi(Ui_MainWindow, QMainWindow):
    
#########################       
#########################  GUI Interface Sachen  
#%%     __init__
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_19.clicked.connect(self.capturestd)
        self.pushButton_3.clicked.connect(self.setgainparameter)
        self.pushButton_4.clicked.connect(self.readgainparameter)
        self.pushButton_5.clicked.connect(self.stage)
        self.pushButton_6.clicked.connect(self.move)
        self.pushButton_7.clicked.connect(self.automove)
        self.pushButton_8.clicked.connect(self.savestage)
        self.pushButton_17.clicked.connect(self.savespectra)
        self.pushButton.clicked.connect(self.profiles)
        self.pushButton_2.clicked.connect(self.settprofiles)
        self.pushButton_12.clicked.connect(self.detlinfile)
        self.pushButton_21.clicked.connect(self.detlin)
        self.pushButton_22.clicked.connect(self.savedetlin)
        self.pushButton_9.clicked.connect(self.connect)
        self.pushButton_10.clicked.connect(self.connectosa)
        self.pushButton_20.clicked.connect(self.conosa)
        self.pushButton_11.clicked.connect(self.grabdetlin)
        self.pushButton_13.clicked.connect(self.loadOSAfile)
        
    
#%%     fig5    plot for spectra and darks  
        self.fig5,(self.sp, self.da) = plt.subplots(1,2, sharex=True)                        
        self.canvas5 = FigureCanvas(self.fig5)        
        self.horizontalLayout_25.replaceWidget(self.widget_16, self.canvas5)              
#%%     fig6    plot for std and std difference    
        self.fig6,(self.stdp, self.sstdp) = plt.subplots(1,2, sharex=True)               
        self.canvas6 = FigureCanvas(self.fig6)        
        self.horizontalLayout_56.replaceWidget(self.widget_17, self.canvas6)    
#%%     fig7    plot for stage singel fits  
        self.fig7 = Figure() 
        self.canvas7 = FigureCanvas(self.fig7)        
        self.ax7 = self.fig7.add_subplot(111)                         
        self.canvas7 = FigureCanvas(self.fig7)        
        self.horizontalLayout_22.replaceWidget(self.widget_14, self.canvas7)              
#%%     fig8    plot for all stage spectra 
        self.fig8 = Figure() 
        self.canvas8 = FigureCanvas(self.fig7)        
        self.ax8 = self.fig8.add_subplot(111)                       
        self.canvas8 = FigureCanvas(self.fig8)        
        self.horizontalLayout_52.replaceWidget(self.widget_15, self.canvas8)     
#%%     fig3    plot for detlin  
        self.fig3 = Figure() 
        self.canvas3 = FigureCanvas(self.fig3)        
        self.ax3 = self.fig3.add_subplot(111)                              
        self.canvas3 = FigureCanvas(self.fig3)        
        self.verticalLayout_8.replaceWidget(self.widget_18, self.canvas3)              
#%%     fig4    plot for detlin  
        self.fig4 = Figure() 
        self.canvas4 = FigureCanvas(self.fig4)        
        self.ax4 = self.fig4.add_subplot(111)                              
        self.canvas4 = FigureCanvas(self.fig4)        
        self.verticalLayout_8.replaceWidget(self.widget_4, self.canvas4)             
#%%     fig5    plot for detlin  
        self.fig5 = Figure() 
        self.canvas5 = FigureCanvas(self.fig5)        
        self.ax5 = self.fig5.add_subplot(111)                              
        self.canvas5 = FigureCanvas(self.fig5)        
        self.verticalLayout_8.replaceWidget(self.widget_6, self.canvas5)
#%%     fig6    plot for detlin  
        self.fig6 = Figure() 
        self.canvas6 = FigureCanvas(self.fig6)        
        self.ax6 = self.fig6.add_subplot(111)                              
        self.canvas6 = FigureCanvas(self.fig6)        
        self.verticalLayout_22.replaceWidget(self.widget_10, self.canvas6)
#%%     fig7    plot for detlin  
        self.fig7 = Figure() 
        self.canvas7 = FigureCanvas(self.fig7)        
        self.ax7 = self.fig7.add_subplot(111)                              
        self.canvas7 = FigureCanvas(self.fig7)        
        self.verticalLayout_22.replaceWidget(self.widget_11, self.canvas7)


#%%
    def connect(self):
        try:
            adresse=str(self.lineEdit_14.text())
            CoraClassHell.CoreSet(self,adresse)
            CoraClassHell.statushalf(self,1)
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def capturestd(self):    
        try:
            self.lineEdit_15.setStyleSheet(
                """QLineEdit { background-color: red; color: white }""")
            self.lineEdit_15.setText("in progress")
            CoraClassHell.createfolder(self,"_STD")
            self.sp.clear()   
            self.da.clear()    
            self.stdp.clear()  
            self.sstdp.clear() 
            QCoreApplication.processEvents()
            reps=int(self.lineEdit_2.text())
            self.specs, self.darks={},{}
            if self.checkBox.isChecked():
                start=int(self.lineEdit_3.text())
                step=int(self.lineEdit_35.text())
                stop=int(self.lineEdit_4.text())+step
                self.InTime=np.arange(start, stop, step).astype(float)    
            else:
                self.InTime=[]
                self.InTime.append(float(self.lineEdit.text()))
            t=0 
            colormap = plt.cm.gist_ncar  
            colorst = [colormap(i) for i in np.linspace(0, 0.9, len(self.InTime))] 
            for tim in self.InTime:            
                self.timedarks=[] 
                self.timespecs=[]        
                for i in range (reps):
                    self.setSTDlaser()
                    if self.radioButton_3.isChecked():
                        CoraClassHell.Set532laserOn(self)
                        if self.radioButton_14.isChecked():
                            CoraClassHell.fitrange532c(self)
                        if self.radioButton_15.isChecked():
                            CoraClassHell.fitrange532p(self)
                    if self.radioButton_4.isChecked():
                        CoraClassHell.Set785laserOn(self)
                        if self.radioButton_14.isChecked():
                            CoraClassHell.fitrange785c(self)
                        if self.radioButton_15.isChecked():
                            CoraClassHell.fitrange785p(self)
                    if self.radioButton_5.isChecked():   
                        CoraClassHell.Set1064laserOn(self)
                        if self.radioButton_14.isChecked():
                            CoraClassHell.fitrange1064c(self)
                        if self.radioButton_15.isChecked():
                            CoraClassHell.fitrange1064p(self)
                    CoraClassHell.CoreAquireSpectra(self,tim)
                    CoraClassHell.SetlaserOff(self)
                    CoraClassHell.CoreAquireDark(self,tim)                   
                    self.axis=np.arange(1,len(self.spectra)+1,1).astype(float)
                    CoraClassHell.singlederivation(self,self.dark)
                    self.sp.set_title("Spectra")
                    self.da.set_title("Darks")
                    self.sp.plot(self.axis,self.spectra,color = colorst[t])
                   
                    if self.checkBox_4.isChecked():
                        CoraClassHell.bg(self,self.spectra)
                        self.sp.plot(self.Xrange,self.bgnpy,'g--')
                        
                    self.da.plot(self.axis,self.dark,color = colorst[t])
                    self.sp.set_xlabel('Pixel', fontsize=14)
                    self.da.set_xlabel('Pixel', fontsize=14)
                    self.sp.set_ylabel('Intensity [a.u.]', fontsize=14)
                    self.da.set_ylabel('Intensity [a.u.]', fontsize=14)
                    self.stdp.set_title("Standard deviation for darks")
                    self.stdp.plot(tim,self.std,'o',color = colorst[t])
                    self.stdp.set_xlabel('Integration time', fontsize=14)
                    self.stdp.set_ylabel('Single Std', fontsize=14)
                    self.sstdp.set_ylabel('Diff. Std', fontsize=14)
                    self.sstdp.set_xlabel('Integration time', fontsize=14)
                    self.sstdp.set_title("Standard deviation for difference of 2 darks")
                    print("Finished aquisition "+str(i+1))               
                    self.timedarks.append(self.dark)
                    self.timespecs.append(self.spectra)
                    specinfo=[]
                    specinfo.append("#"+self.lineEdit_11.text())
                    for x in self.spectra:
                        specinfo.append(x)                  
                    CoraClassHell.savefile(self,specinfo,self.addspecname+str(tim)+"s_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv")                    
                    darkinfo=[]
                    darkinfo.append("#"+self.lineEdit_11.text())
                    for x in self.spectra:
                        darkinfo.append(x) 
                    CoraClassHell.savefile(self,darkinfo,self.adddarkname+str(tim)+"s_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv")           
                    self.fig5.tight_layout()                                      
                    self.canvas5.draw()    
                    QCoreApplication.processEvents()              
                    if i>0:
                        CoraClassHell.diffderivation(self,self.timedarks,i)      
                        self.sstdp.plot(tim,self.sstd,'o',color = colorst[t])                              
                    self.fig6.tight_layout()                            
                    self.canvas6.draw()
                    CoraClassHell.sliderset(self,1,2,1,2,len(self.spectra),max(self.spectra),self.drawstd)
                    QCoreApplication.processEvents() 
                t+=1              
            print("Done")
            self.lineEdit_15.setStyleSheet(
                """QLineEdit { background-color: green; color: white }""")
            self.lineEdit_15.setText("finished")
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def drawstd(self): 
        if self.radioButton_3.isChecked():
            if self.radioButton_14.isChecked():
                CoraClassHell.fitrange532c(self)
            if self.radioButton_15.isChecked():
                CoraClassHell.fitrange532p(self)
        if self.radioButton_4.isChecked():
            if self.radioButton_14.isChecked():
                CoraClassHell.fitrange785c(self)
            if self.radioButton_15.isChecked():
                CoraClassHell.fitrange785p(self)
        if self.radioButton_5.isChecked():   
            if self.radioButton_14.isChecked():
                CoraClassHell.fitrange1064c(self)
            if self.radioButton_15.isChecked():
                CoraClassHell.fitrange1064p(self)  
        colorst = plt.cm.gist_ncar(np.linspace(0, 1, len(self.timespecs)))
        self.sp.clear()
        self.sp.set_title("Spectra")
        self.sp.set_xlabel('Pixel', fontsize=14)
        self.sp.set_ylabel('Intensity [a.u.]', fontsize=14)
        CoraClassHell.slidercall(self,1,2,1,2,self.sp)
        for i in range (0,len(self.timespecs)):
            self.sp.plot(self.axis,self.timespecs[i],color = colorst[i])
            if self.checkBox_4.isChecked():
                CoraClassHell.bg(self,self.timespecs[i])
                self.sp.plot(self.Xrange,self.bgnpy,'g--')
        
        self.fig5.tight_layout()
        self.canvas5.draw()            

    def setlaser532(self):
        self.cora.firmware.ProfileSelectSet(self.profile532)
        self.addspecname="Spektra532_"
        self.adddarkname="Dark_532_"

    def setlaser785(self):
        self.cora.firmware.ProfileSelectSet(self.profile785)
        self.addspecname="Spektra785_"
        self.adddarkname="Dark_785_"

    def setlaser1064(self):   
        self.cora.firmware.ProfileSelectSet(self.profile1064)
        self.addspecname="Spektra1064_"
        self.adddarkname="Dark_1064_" 

    def setSTDlaser(self):   
        try:     
            #CoraClassHell.CoreSet(self)  
            if self.radioButton_3.isChecked():
                self.setlaser532()
            elif self.radioButton_4.isChecked():
                self.setlaser785()
            elif self.radioButton_5.isChecked():   
                self.setlaser1064()
            else:
                return                                                
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def setOSAlaser(self):   
        try:     
            #CoraClassHell.CoreSet(self)  
            if self.radioButton_6.isChecked():
                self.setlaser532()
            elif self.radioButton_7.isChecked():
                self.setlaser785()
            elif self.radioButton_8.isChecked():   
                self.setlaser1064()
            else:
                return                                                
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def setSTAGElaser(self):   
        try:     
            #CoraClassHell.CoreSet(self)  
            if self.radioButton_13.isChecked():
                self.setlaser532()
            elif self.radioButton_2.isChecked():
                self.setlaser785()
            elif self.radioButton_3.isChecked():   
                self.setlaser1064()
            else:
                return                                                
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def setDETLINlaser(self):   
        try:     
            #CoraClassHell.CoreSet(self)  
            if self.radioButton_9.isChecked():
                self.setlaser532()
            elif self.radioButton_10.isChecked():
                self.setlaser785()
            elif self.radioButton_11.isChecked():   
                self.setlaser1064()
            else:
                return                                                
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def savespectra(self):
        self.savepath = "C:\\Users\\martin.hell\\Cora5x\\Hell_Spectra\\"               
        os.chdir(self.savepath) 
        CoraClassHell.save(self,"SpectraDark_{}.jpg",self.canvas5,10)  
        CoraClassHell.save(self,"StdSstd{}.jpg",self.canvas6,10)
        self.path = "C:\\Users\\martin.hell\\Cora5x\\"               
        os.chdir(self.path) 

    def readgainparameter(self):
        try:
            self.textBrowser_3.clear()
                
            if self.radioButton.isChecked():   
                self.cora.firmware.ProfileSelectSet(1)                                        
            elif self.radioButton_2.isChecked():   
                self.cora.firmware.ProfileSelectSet(2)               
            else:
                return
            para=self.cora.firmware.VideoAdcGainOffsetGet(True)   
            self.textBrowser_3.clear()                 
            self.textBrowser_3.append("Gain: "+str(para['gain']))
            self.textBrowser_3.append("Offset: "+str(round(para['offset_V'],4))) 
            
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def setgainparameter(self):  
        try:
            gain=float(form.lineEdit_6.text())
            offset=float(form.lineEdit_5.text())
            
            if  self.radioButton.isChecked():   
                self.cora.firmware.ProfileSelectSet(1)
            elif  self.radioButton_2.isChecked():                           
                self.cora.firmware.ProfileSelectSet(2)             
            else: 
                return
            self.cora.firmware.VideoAdcGainOffsetSet(gain,offset)    
            CoraClassHell.status(self,3)  
            para=self.cora.firmware.VideoAdcGainOffsetGet(True)   
            self.textBrowser_3.clear()                 
            self.textBrowser_3.append("new Gain: "+str(para['gain']))
            self.textBrowser_3.append("new Offset: "+str(para['offset_V']))
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def savestage(self):
        self.savepath = "C:\\Users\\martin.hell\\Cora5x\\Hell_Spectra\\"               
        os.chdir(self.savepath)           
        CoraClassHell.save(self,"Stage_{}.jpg",self.canvas8,8)
        self.path = "C:\\Users\\martin.hell\\Cora5x\\"               
        os.chdir(self.path) 

    def stage(self):     
        try:
            #CoraClassHell.CoreSet(self)         
            pos=self.cora.firmware.FocusStageStatusGet(1)    
            self.textBrowser_4.append("position: "+str(round(pos['actualPosition']*1000,6)))
            lim=self.cora.firmware.FocusStageRangeGet(1)
            self.textBrowser_4.append("limit1: "+str(round(lim['min']*1000,6)))
            self.textBrowser_4.append("limit2: "+str(round(lim['max']*1000,6)))
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def move(self):
        try:
            wanted_position_mm = float(self.lineEdit_7.text())
            #CoraClassHell.CoreSet(self)  
            self.cora.firmware.FocusStageMoveToPosition(wanted_position_mm/1000) 
            pos=self.cora.firmware.FocusStageStatusGet(1)    
            self.textBrowser_4.append("new pos.: "+str(round(pos['actualPosition']*1000,6)))           
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def automove(self):
        try:
            self.lineEdit_16.setStyleSheet(
                """QLineEdit { background-color: red; color: white }""")
            self.lineEdit_16.setText("in progress")
            CoraClassHell.createfolder(self,"_STAGE")
            self.ax7.clear()
            self.ax8.clear()
            startpos=float(self.lineEdit_8.text())
            endpos=float(self.lineEdit_9.text())
            step=float(self.lineEdit_41.text())
            posrange=np.arange(startpos, (endpos+0.01), step).astype(float)         
            negrange=np.arange(endpos, (startpos-0.01), -step).astype(float)  
            iterations=int(self.lineEdit_10.text())
            integtime=float(self.lineEdit_30.text())
            colormap = plt.cm.gist_ncar  
            colorst = [colormap(i) for i in np.linspace(0, 0.9, iterations)]  
            absolutpospos=[]
            absolutposmax=[]
            absolutposmax1=[]
            absolutposmax2=[]
            absolutnegpos=[]
            absolutnegmax=[]
            absolutnegmax1=[]
            absolutnegmax2=[]
            for r in range (0,iterations):   
                print("Running iteration: "+str(r))                              
                posarray = []
                maxarray = []
                maxarray1 = []
                maxarray2 = []
                for position in posrange:               
                    self.cora.firmware.FocusStageMoveToPosition(position/1000)    
                    pos=self.cora.firmware.FocusStageStatusGet(1)
                    self.textBrowser_4.append(str(r)+"-new pos.: "+str(round(pos['actualPosition']*1000,6)))    
                    QCoreApplication.processEvents() 
                    if self.radioButton_12.isChecked():                  
                        if self.checkBox_13.isChecked():
                            self.setlaser532()
                            CoraClassHell.fitrange532c(self)
                        if self.checkBox_2.isChecked():
                            self.setlaser785()
                            CoraClassHell.fitrange785c(self)
                        if self.checkBox_3.isChecked():  
                            self.setlaser1064()
                            CoraClassHell.fitrange1064c(self)      
                    if self.radioButton_13.isChecked():                  
                        if self.checkBox_13.isChecked():
                            self.setlaser532()
                            CoraClassHell.fitrange532p(self)
                        if self.checkBox_2.isChecked():
                            self.setlaser785()
                            CoraClassHell.fitrange785p(self)
                        if self.checkBox_3.isChecked():  
                            self.setlaser1064()
                            CoraClassHell.fitrange1064p(self)
                    if self.radioButton_16.isChecked():
                        if self.checkBox_13.isChecked():
                            self.setlaser532()
                            CoraClassHell.fitrangeSRM(self)
                        if self.checkBox_2.isChecked():
                            self.setlaser785()
                            CoraClassHell.fitrangeSRM(self)
                        if self.checkBox_3.isChecked():  
                            self.setlaser1064()
                            CoraClassHell.fitrangeSRM1064(self)
                    if self.checkBox_13.isChecked():
                        CoraClassHell.Set532laserOn(self)
                    if self.checkBox_2.isChecked():
                        CoraClassHell.Set785laserOn(self)
                    if self.checkBox_3.isChecked():   
                        CoraClassHell.Set1064laserOn(self)
                    CoraClassHell.CoreAquireSpectra(self,integtime)
                    CoraClassHell.SetlaserOff(self)
                    specinfo=[]
                    specinfo.append("#"+self.lineEdit_12.text())
                    for x in self.spectra:
                        specinfo.append(x)                  
                    CoraClassHell.savefile(self,specinfo,self.addspecname+str(integtime)+"s_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv")                                    
                    CoraClassHell.CoreAquireDark(self,integtime)  
                    darkinfo=[]
                    darkinfo.append("#"+self.lineEdit_11.text())
                    for x in self.spectra:
                        darkinfo.append(x) 
                    CoraClassHell.savefile(self,darkinfo,self.adddarkname+str(integtime)+"s_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv")                                                                             
                    if self.checkBox_13.isChecked():
                        CoraClassHell.peakfit_old(self,self.spectra)
                    else:
                        CoraClassHell.peakfit(self,self.spectra)    
                    maxarray.append(self.peakmax) 
                    maxarray1.append(self.maxvalue) 
                    maxarray2.append(self.maxvaluewb)  
                    posarray.append(position)   
                    self.ax7.clear()          
                    self.ax7.plot(self.npx,self.npy,'g--',label='data')  ###  pixel
                    self.ax7.plot(self.npx,lorentzian(self.npx,*self.popt),'b--',label='fit')  
                    CoraClassHell.starmarker(self)
                    #self.ax7.plot(posarray,maxarray1, 'r--', marker=self.cut_star, markersize=6)#,color = colorst[r])  ###  pixel                               
                    self.ax7.set_ylabel('Intensity [a.u.]', fontsize=14)
                    self.ax7.set_xlabel('Pixel', fontsize=14)
                    self.fig7.tight_layout()                            
                    self.canvas7.draw()
                    QCoreApplication.processEvents()                 
                    self.ax8.clear()
                    self.ax8.plot(posarray,maxarray, 'r--', marker=self.cut_star, markersize=6)#,color = colorst[r])  ###  pixel
                    self.ax8.set_xlabel('Position [mm]', fontsize=14)
                    self.ax8.set_ylabel('Max. Intensity [a.u.]', fontsize=14)
                    self.fig8.tight_layout()                            
                    self.canvas8.draw()
                    QCoreApplication.processEvents()
                absolutpospos.append(posarray) 
                absolutposmax.append(maxarray) 
                absolutposmax1.append(maxarray1)
                absolutposmax2.append(maxarray2)
                posarray = []
                maxarray = []
                maxarray1 = []
                maxarray2 = []
                for position in negrange:               
                    self.cora.firmware.FocusStageMoveToPosition(position/1000)    
                    pos=self.cora.firmware.FocusStageStatusGet(1)
                    self.textBrowser_4.append(str(r)+"-neue position: "+str(pos['actualPosition']*1000))    
                    QCoreApplication.processEvents()
                    if self.radioButton_12.isChecked():                  
                        if self.checkBox_13.isChecked():
                            self.setlaser532()
                            CoraClassHell.fitrange532c(self)
                        if self.checkBox_2.isChecked():
                            self.setlaser785()
                            CoraClassHell.fitrange785c(self)
                        if self.checkBox_3.isChecked():  
                            self.setlaser1064()
                            CoraClassHell.fitrange1064c(self)      
                    if self.radioButton_13.isChecked():                  
                        if self.checkBox_13.isChecked():
                            self.setlaser532()
                            CoraClassHell.fitrange532p(self)
                        if self.checkBox_2.isChecked():
                            self.setlaser785()
                            CoraClassHell.fitrange785p(self)
                        if self.checkBox_3.isChecked():  
                            self.setlaser1064()
                            CoraClassHell.fitrange1064p(self)     
                    if self.checkBox_13.isChecked():
                        CoraClassHell.Set532laserOn(self)
                    if self.checkBox_2.isChecked():
                        CoraClassHell.Set785laserOn(self)
                    if self.checkBox_3.isChecked():   
                        CoraClassHell.Set1064laserOn(self)
                    CoraClassHell.CoreAquireSpectra(self,integtime)
                    CoraClassHell.CoreAquireDark(self,integtime)                                                             
                    CoraClassHell.peakfit(self,self.spectra)                           
                    maxarray.append(self.peakmax)   
                    maxarray1.append(self.maxvalue) 
                    maxarray2.append(self.maxvaluewb)  
                    posarray.append(position)     
                    self.ax7.clear()        
                    self.ax7.plot(self.npx,self.npy,'g--',label='data')  ###  pixel
                    self.ax7.plot(self.npx,lorentzian(self.npx,*self.popt),'b--',label='fit')
                #    CoraClassHell.starmarker(self)
                #    self.ax7.plot(posarray,maxarray1, 'r--', marker=self.cut_star, markersize=6)#,color = colorst[r])  ###  pixel                                         
                    self.ax8.clear()
                #    self.ax8.plot(posarray,maxarray2, 'r--', marker=self.cut_star, markersize=6)#,color = colorst[r])  ###  pixel   
                    self.ax8.plot(posarray,maxarray, 'r--', marker=self.cut_star, markersize=6)#,color = colorst[r])  ###  pixel
                    self.ax8.set_xlabel('Position [mm]', fontsize=14)
                    self.ax8.set_ylabel('Max. Intensity [a.u.]', fontsize=14)
                    self.fig7.tight_layout()                            
                    self.canvas7.draw()
                    self.fig8.tight_layout()                            
                    self.canvas8.draw()
                    QCoreApplication.processEvents() 
                absolutnegpos.append(posarray) 
                absolutnegmax.append(maxarray)
                absolutnegmax1.append(maxarray1)
                absolutnegmax2.append(maxarray2)
            self.ax8.clear()
            for r in range (0,iterations):           
                self.ax8.plot(absolutnegpos[r],absolutnegmax[r], '--', marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel                       
                self.ax8.plot(absolutpospos[r],absolutposmax[r], marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel               
            #    self.ax8.plot(absolutnegpos[r],absolutnegmax1[r], '--', marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel                       
            #   self.ax8.plot(absolutpospos[r],absolutposmax1[r], marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel               
            #    self.ax8.plot(absolutnegpos[r],absolutnegmax2[r], '--', marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel                       
            #    self.ax8.plot(absolutpospos[r],absolutposmax2[r], marker=self.cut_star, markersize=6,color = colorst[r])  ###  pixel               
                
                self.fig8.tight_layout()                            
                self.canvas8.draw()
            self.lineEdit_16.setStyleSheet(
                """QLineEdit { background-color: green; color: white }""")
            self.lineEdit_16.setText("finished")
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)
    
    def profiles(self):
        self.textBrowser.clear()
        CoraClassHell.readprofiles(self,1)
        self.textBrowser.append("Profil 1: "+str(form.wellenlaenge))       
        CoraClassHell.readprofiles(self,2)
        self.textBrowser.append("Profil 2: "+str(form.wellenlaenge))
     
    def settprofiles(self):
        try:
            if self.checkBox_7.isChecked():
                self.profile532=1
            elif self.checkBox_8.isChecked():
                self.profile532=2        
            
            if self.checkBox_9.isChecked():
                self.profile785=1
            elif self.checkBox_10.isChecked():
                self.profile785=2        
            
            if self.checkBox_11.isChecked():
                self.profile1064=1
            elif self.checkBox_12.isChecked():
                self.profile1064=2        
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)  
        self.lineEdit_21.setStyleSheet("color: rgb(13, 134, 70)")     
        self.lineEdit_21.setText("Profiles assigned")      
        self.lineEdit_22.setStyleSheet("color: rgb(13, 134, 70)")     
        self.lineEdit_22.setText("Profiles assigned") 
        self.lineEdit_23.setStyleSheet("color: rgb(13, 134, 70)")     
        self.lineEdit_23.setText("Profiles assigned")      
        self.lineEdit_29.setStyleSheet("color: rgb(13, 134, 70)")     
        self.lineEdit_29.setText("Profiles assigned")  

    def detlin(self):
        try:
            self.lineEdit_17.setStyleSheet(
                """QLineEdit { background-color: red; color: white }""")
            self.lineEdit_17.setText("in progress")
            CoraClassHell.createfolder(self, "_DetLin")
            self.ax3.clear()   
            self.ax4.clear()   
            self.ax5.clear()
            QCoreApplication.processEvents()
            self.specs={}              
            self.pixelints=collections.defaultdict(list)    
            self.polylist=collections.defaultdict(list)  
            self.polylistm=collections.defaultdict(list)
            self.polylistp=collections.defaultdict(list)          
            start=float(self.lineEdit_31.text())
            step=float(self.lineEdit_34.text())
            stop=float(self.lineEdit_32.text())+step
            self.InTime=np.arange(start, stop, step).astype(float)                   
            if self.radioButton_9.isChecked():
                pixellength=2058
                pixelstep=int(self.lineEdit_42.text())
            elif self.radioButton_10.isChecked():
                pixellength=2058
                pixelstep=int(self.lineEdit_43.text())
            elif self.radioButton_11.isChecked():   
                pixellength=256
                pixelstep=int(self.lineEdit_44.text())
            pixellist=np.arange(1,pixellength+1,pixelstep).astype(int)  
            self.axis=np.arange(1,pixellength+1,1).astype(float)
            colorst = plt.cm.gist_ncar(np.linspace(0, 1, len(pixellist)))
            s=0                  
            for tim in self.InTime:   
                colorindex=self.InTime.index(tim)                                                                       
                self.setDETLINlaser()
                if self.radioButton_9.isChecked():
                    CoraClassHell.Set532laserOn(self)
                if self.radioButton_10.isChecked():
                    CoraClassHell.Set785laserOn(self)
                if self.radioButton_11.isChecked():   
                    CoraClassHell.Set1064laserOn(self)
                CoraClassHell.CoreAquireSpectra(self,tim)  
                CoraClassHell.SetlaserOff(self)
                specinfo=[]
                specinfo.append("#"+self.lineEdit_11.text())
                for x in self.spectra:
                    specinfo.append(x)                  
                CoraClassHell.savefile(self,specinfo,self.addspecname+str(tim)+"s_"+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".txt")                                       
                self.specs[tim]=self.spectra  
                self.ax4.plot(self.axis,self.specs[tim],'.',color = colorst[colorindex])      
                self.ax4.set_title("Intensities of all Pixel")
                self.ax4.set_xlabel('Pixel', fontsize=14)                      
                self.ax4.set_ylabel('Intensity [a.u.]', fontsize=14)                            
                self.fig4.tight_layout()                            
                self.canvas4.draw()
                
                for t in pixellist:               
                    self.pixelints[t].append(self.spectra[t-1])
                    colorindex=pixellist.tolist().index(t)
                    self.ax3.plot(tim,self.spectra[t-1],'o',color = colorst[colorindex])              
                    self.ax3.set_title("PixelIntensities for Integration time")
                    self.ax3.set_xlabel('Integration time [s]', fontsize=14)                      
                    self.ax3.set_ylabel('Intensity [a.u.]', fontsize=14)                            
                    self.fig4.tight_layout()                            
                    self.canvas4.draw()       
                    QCoreApplication.processEvents()   
            
            for t in self.pixellist: 
                intensities=self.pixelints[t]
                fitpoints=[]
                fittimes=[]
                colorindex=self.pixellist.tolist().index(t)
                if np.mean(intensities)>2500:#32768 #entscheide fit-bereich
                    for x in intensities:  #gehe pixel intensitäten daurch
                        if x in range(2500,6000):
                            fitpoints.append(x)
                            fittimes.append(self.InTime[intensities.index(x)])
                        else:
                            pass   
                    coeff = np.polyfit(fittimes,fitpoints,1)
                    poly = np.poly1d(coeff)
                    self.polylist[t].append(poly(self.InTime))
                    self.polylistp[t].append(poly(self.InTime)*1.5)
                    self.polylistm[t].append(poly(self.InTime)*0.5)

                if np.mean(intensities)<2500:#32768 #entscheide fit-bereich
                    for x in intensities:  #gehe pixel intensitäten daurch
                        if x in range(0,2500):
                            fitpoints.append(x)
                            fittimes.append(self.InTime[intensities.index(x)])
                        else:
                            pass   
                    coeff = np.polyfit(fittimes,fitpoints,1)
                    poly = np.poly1d(coeff)
                    self.polylist[t].append(poly(self.InTime))
                    self.polylistp[t].append(poly(self.InTime)*1.5)
                    self.polylistm[t].append(poly(self.InTime)*0.5)        
            self.failpixel=collections.defaultdict(list)
            self.failtimes=collections.defaultdict(list)
            self.passpixel=collections.defaultdict(list)
            self.passtimes=collections.defaultdict(list) 
            self.textBrowser_2.clear()
            self.textBrowser_2.append("Pixel "+"Nr."+" - "+"Inten."+" - "+"IntegTime")      
            for t in self.pixellist: 
                c=0
                sololist=self.pixelints[t]                 
                solopolylist_m=self.polylistm[t][0]                  
                solopolylist_p=self.polylistp[t][0]           
                for x in sololist:
                    a=sololist.index(x)                   
                    if solopolylist_m[a]<x<solopolylist_p[a]:
                        c+=1
                        self.passpixel[t].append(x)
                        self.passtimes[t].append(self.InTime[sololist.index(x)])
                        print("yes")
                    else:
                        self.failpixel[t].append(x)
                        self.failtimes[t].append(self.InTime[sololist.index(x)])
                        self.textBrowser_2.append("Pixel "+str(t)+" - "+str(x)+" - "+str(self.InTime[sololist.index(x)]))
                print(c)
                if c==len(sololist):
                    self.ax3.plot(self.InTime,self.polylist[t][0],color = 'green')
                else:
                    self.ax3.plot(self.InTime,self.polylist[t][0],color = 'red')           
                self.fig3.tight_layout()                            
                self.canvas3.draw()
            
            for t in self.pixellist:
                self.ax5.plot(self.passtimes[t],self.passpixel[t],'o',color = 'green')      
                self.ax5.plot(self.failtimes[t],self.failpixel[t],'o',color = 'red')              
            self.ax5.set_title("Fail/Pass of Pixel per Integration time")
            self.ax5.set_xlabel('Integration time [s]', fontsize=14)                      
            self.ax5.set_ylabel('Intensity [a.u.]', fontsize=14)
            self.fig5.tight_layout()                            
            self.canvas5.draw()

            
            self.lineEdit_17.setStyleSheet(
                """QLineEdit { background-color: green; color: white }""")
            self.lineEdit_17.setText("finished")
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)        

    def detlinfile(self): 
        try:
            self.ax3.clear()   
            self.ax4.clear()   
            self.ax5.clear()
            folder=self.lineEdit_40.text()
            self.path = "C:\\Users\martin.hell\\Cora5x\Hell_Spectra\\"+folder
            os.chdir(self.path)
            self.fileList=glob.glob("*.txt")   
            self.InTime=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0] 
            self.specs={}
            if self.fileList:  
                count=0                                
                for filename in sorted(self.fileList, key=numericalSort):                
                    rawspectra=np.loadtxt(filename)                   
                    self.specs[self.InTime[count]]=rawspectra   
                    count+=1        
                 
                self.pixelints=collections.defaultdict(list)    
                self.polylist=collections.defaultdict(list)    
                self.polylistp=collections.defaultdict(list)
                self.polylistm=collections.defaultdict(list)                  
                self.pixellist=np.arange(1,2059,50).astype(int)  
                self.axis=np.arange(1,2059,1).astype(float)
                colorst = plt.cm.gist_ncar(np.linspace(0, 1, len(self.pixellist)))
                
                for tim in self.InTime:      
                    colorindex=self.InTime.index(tim)                        
                    for t in self.pixellist:               
                        self.pixelints[t].append(self.specs[tim][t])
                    self.ax4.plot(self.axis,self.specs[tim],'.',color = colorst[colorindex])      
                    self.ax4.set_title("Intensities of all Pixel")
                    self.ax4.set_xlabel('Pixel', fontsize=14)                      
                    self.ax4.set_ylabel('Intensity [a.u.]', fontsize=14)                            
                    self.fig4.tight_layout()                            
                    self.canvas4.draw()

                for t in self.pixellist:        
                    colorindex=self.pixellist.tolist().index(t)
                    self.ax3.plot(self.InTime,self.pixelints[t],'o',color = colorst[colorindex])      
                    self.ax3.set_title("PixelIntensities for Integration time")
                    self.ax3.set_xlabel('Integration time [s]', fontsize=14)                      
                    self.ax3.set_ylabel('Intensity [a.u.]', fontsize=14)                            
                    self.fig3.tight_layout()                            
                    self.canvas3.draw()       
                    QCoreApplication.processEvents() 
                    #######################################

                
                for t in self.pixellist: 
                    intensities=self.pixelints[t]
                    fitpoints=[]
                    fittimes=[]
                    colorindex=self.pixellist.tolist().index(t)
                    if np.mean(intensities)>2500:#32768 #entscheide fit-bereich
                        for x in intensities:  #gehe pixel intensitäten daurch
                            if x in range(2500,6000):#[39321,52428]#60-80%
                                fitpoints.append(x)
                                fittimes.append(self.InTime[intensities.index(x)])
                            else:
                                pass   
                        coeff = np.polyfit(fittimes,fitpoints,1)
                        poly = np.poly1d(coeff)
                        self.polylist[t].append(poly(self.InTime))
                        self.polylistp[t].append(poly(self.InTime)*1.5)
                        self.polylistm[t].append(poly(self.InTime)*0.5)

                    if np.mean(intensities)<2500:#32768 #entscheide fit-bereich
                        for x in intensities:  #gehe pixel intensitäten daurch
                            if x in range(0,2500):#[13107,26214]#20-40%
                                fitpoints.append(x)
                                fittimes.append(self.InTime[intensities.index(x)])
                            else:
                                pass   
                        coeff = np.polyfit(fittimes,fitpoints,1)
                        poly = np.poly1d(coeff)
                        self.polylist[t].append(poly(self.InTime))
                        self.polylistp[t].append(poly(self.InTime)*1.5)
                        self.polylistm[t].append(poly(self.InTime)*0.5)        
                
                self.failpixel=collections.defaultdict(list)
                self.failtimes=collections.defaultdict(list)
                self.passpixel=collections.defaultdict(list)
                self.passtimes=collections.defaultdict(list) 
                self.textBrowser_2.clear()
                self.textBrowser_2.append("Pixel "+"Nr."+" - "+"Inten."+" - "+"IntegTime")     
                for t in self.pixellist: 
                    c=0
                    sololist=self.pixelints[t]                 
                    solopolylist_m=self.polylistm[t][0]                  
                    solopolylist_p=self.polylistp[t][0]           
                    for x in sololist:
                        a=sololist.index(x)                   
                        if solopolylist_m[a]<x<solopolylist_p[a]:
                            c+=1
                            self.passpixel[t].append(x)
                            self.passtimes[t].append(self.InTime[sololist.index(x)])
                        else:
                            self.failpixel[t].append(x)
                            self.failtimes[t].append(self.InTime[sololist.index(x)])       
                            self.textBrowser_2.append("Pixel "+str(t)+" - "+str(x)+" - "+str(self.InTime[sololist.index(x)]))
                  
                    if c==len(sololist):
                        self.ax3.plot(self.InTime,self.polylist[t][0],color = 'green')
                    else:
                        self.ax3.plot(self.InTime,self.polylist[t][0],color = 'red')           
                    self.fig3.tight_layout()                            
                    self.canvas3.draw()
                
                for t in self.pixellist:
                    self.ax5.plot(self.passtimes[t],self.passpixel[t],'o',color = 'green')      
                    self.ax5.plot(self.failtimes[t],self.failpixel[t],'o',color = 'red')              
                self.ax5.set_title("Fail/Pass of Pixel per Integration time")
                self.ax5.set_xlabel('Integration time [s]', fontsize=14)                      
                self.ax5.set_ylabel('Intensity [a.u.]', fontsize=14)
                self.fig5.tight_layout()                            
                self.canvas5.draw()

                self.lineEdit_17.setStyleSheet(
                    """QLineEdit { background-color: green; color: white }""")
                self.lineEdit_17.setText("finished")
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def grabdetlin(self):
        CoraClassHell.grap(self,self.widget_9,"DetlinVals_{}.png")

    def savedetlin(self):
        self.savepath = "C:\\Users\\martin.hell\\Cora5x\\Hell_Spectra\\"               
        os.chdir(self.savepath)           
        CoraClassHell.save(self,"Detlin_{}.jpg",self.canvas3,12)
        self.path = "C:\\Users\\martin.hell\\Cora5x\\"               
        os.chdir(self.path) 
    
    def connectosa(self):
        available_ports = SerialPorts("PX1Y9X78A").matching_ports()
        if len(available_ports) != 1:
            print("Cannot find OSA.")
            sys.exit(1)
        self.port = available_ports[0]
        self.serial = serial.Serial(self.port, 19200, 8, timeout=3.0)
        self.osa = OSA_AQ6315A(self.serial, 1) # OSA on GPIB address 1
        print(self.osa.get_idn())

    def conosa(self):
        try:  
            
            logfilename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_laser.log")
            logfile = open(logfilename, 'w')
            logfile.write('# date, time, pd_power, laser_temperature, set_temperature, current, set_current, osa_pwr, osa_cw1, osa_wd, osa_th1\n')
        
            if self.radioButton_6.isChecked():
                self.setlaser532()    
                CoraClassHell.Set532laserOn(self)        
            if self.radioButton_7.isChecked():
                self.setlaser785()
                CoraClassHell.Set785laserOn(self)
            if self.radioButton_8.isChecked():  
                self.setlaser1064()   
                CoraClassHell.Set1064laserOn(self)         

            self.osa.set('CLMES') # constant wave light measuring mode

            print(self.osa.get_avg())
            self.osa.wait_for_sweep_stopped()
            print(self.osa.measure_power_dBm())
            use_auto_sweep = True
            if use_auto_sweep:
                self.osa.set('RESLN 0.05')
            else:
                self.osa.set_start_stop_wl(909.26, 914.60)   
                self.osa.set('RESLN 2.0')
            
             
            spectrum_count = 0
            of=open('osa_tryout.txt', 'w')
            try:           
                if use_auto_sweep:
                    self.osa.set('AUTO')
                    time.sleep(20.0)
                    self.osa.set('STP')
                
                self.osa.do_single_sweep()
                timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                self.zeitstempel=timestamp
                osapwr = self.osa.measure_power_dBm()
                print("Power = {} dBm".format(osapwr))
                    
                self.osa.set('PKSR')
                self.osa.set('CTR=P')
                self.osa.set('PWR')
                print("PWR = {} dBm".format(self.osa.get("ANA?", 'float')))

                self.osa.set('ENVK 1')           # scale width value
                self.osa.set('ENVT2 30.0')       # disregard underneath this level
                self.osa.set('ENVT1 3.0')        # use 3dB points for width
                self.osa.set('SWENV')
                values = self.osa.get("ANA?", 'float')
                (self.cwl, self.wd, self.th1) = values
                print("CWL = {} Width = {} nm TH1={}dB".format(self.cwl, self.wd, self.th1))

                self.path = "C:\\Users\APDE1.RD\\Desktop\\Cora5x\\Recorded\\OSA"
                os.chdir(self.path)
                self.osa.spectrum_to_file("osa_spectrum_" + timestamp.replace(' ','_').replace(',','').replace(':','-') + ".txt")

                self.ax6.clear()           
                self.ax6.plot(self.lengthlist,self.powerlist,'.',color = "red")      
                self.ax6.set_title("OSA")
                self.ax6.set_xlabel('Wavelength', fontsize=14)                      
                self.ax6.set_ylabel('Power', fontsize=14)                            
                self.fig6.tight_layout()                            
                self.canvas6.draw() 

            except Exception as e:
                exception_name = type(e).__name__
                if exception_name == 'KeyboardInterrupt':
                    raise(e)
                else:
                    print(e)
            CoraClassHell.SetlaserOff(self)
        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def loadOSAfile(self):
        try:
            file=self.lineEdit_45.text()+".txt"
            self.osafilepath = "C:\\Users\APDE1.RD\\Desktop\\Cora5x\\Recorded\\OSA"
            os.chdir(self.osafilepath)
            rawspectra=np.loadtxt(file)
            self.ax6.clear()
            for x in rawspectra:
                self.ax6.plot(x[0],x[1],'.',color = "red")      
                self.ax6.set_title("OSA")
                self.ax6.set_xlabel('Wavelength', fontsize=14)                      
                self.ax6.set_ylabel('Power', fontsize=14)                            
            self.fig6.tight_layout()                            
            self.canvas6.draw()    
            print(rawspectra)

        except Exception as err:
            tb = sys.exc_info()[2]           
            print("something went in line:",tb.tb_lineno)  
            print("Error:",err)

    def OSAma(self):
        self.ax7.clear()
        self.ax7.set_title("OSA")
        self.ax7.set_xlabel('Time', fontsize=14)                      
        self.ax7.set_ylabel('Wavelength', fontsize=14)
        iterations=int(self.lineEdit_19.text())
        messpause=float(self.lineEdit_46.text())*60
        centerwavelength=[]
        widths=[]
        messzeiten=[]
        for i in range(iterations):
            self.conosa()
            centerwavelength.append(self.cwl)
            widths.append(self.wd)
            messzeiten.append(self.zeitstempel)
            self.ax7.plot(messzeiten[i],centerwavelength[i],'.',color = "red")                                          
            self.fig7.tight_layout()                            
            self.canvas7.draw()
            time.slepp(messpause)
######################### 
#########################        
app = QApplication([])
form = EmbedPlotUi()
form.show()
app.exec_()
    