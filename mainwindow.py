# This Python file uses the following encoding: utf-8
from logging import raiseExceptions
import os
from pathlib import Path
import sys

import numpy 
from numpy import array 
from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("form.ui", self)
        self.show()

        self.plane.toggled.connect(self.process_type)
        self.xy_plane.toggled.connect(self.process_type)
        self.yz_plane.toggled.connect(self.process_type)
        self.xz_plane.toggled.connect(self.process_type)
        self.run.clicked.connect(self.onRun)


    
    def process_data(self):
        self.xx = self.xx.value()
        self.xy = self.xy.value()
        self.xz = self.xz.value()
        self.yx = self.yx.value()
        self.yy = self.yy.value()
        self.yz = self.yz.value()
        self.zx = self.zx.value()
        self.zy = self.zy.value()
        self.zz = self.zz.value()

        self.tensor = array([
            [self.xx,self.xy,self.xz],
            [self.yx,self.yy,self.yz],
            [self.zx,self.zy,self.zz]
        ])

    def process_type(self):
        self.type = None 
        self.plane_bool = False
        self.plane_type = None 
        ErrorText = None 
        
        if self.stress_input.isChecked():
            self.type = "Stress"
        elif self.strain_input.isChecked():
            self.type = "Strain"
        
        else: 
            ErrorText = "Input Type is not selected"

        if self.plane.isChecked():
            self.plane_bool = True
            if self.plane_stress.isChecked():
                self.plane_type = "Plane Stress"
            elif self.plane_stress.isChecked():
                self.plane_type = "Plane Strain"

        else: 
            self.plane_bool = False
        if self.plane_bool:
            self.xy_plane.setEnabled(True)
            self.yz_plane.setEnabled(True)
            self.xz_plane.setEnabled(True)

            if self.xy_plane.isChecked():
                self.xz.setEnabled(False)
                self.yz.setEnabled(False)
                self.zz.setEnabled(False)
                self.zy.setEnabled(False)
                self.zx.setEnabled(False)

                self.yx.setEnabled(True)
                self.xx.setEnabled(True)
                self.xy.setEnabled(True)
                self.yy.setEnabled(True)
   

            elif self.yz_plane.isChecked():
                self.xz.setEnabled(False)
                self.zx.setEnabled(False)
                self.yx.setEnabled(False)
                self.xx.setEnabled(False)
                self.xy.setEnabled(False)


                self.yz.setEnabled(True)
                self.zz.setEnabled(True)
                self.zy.setEnabled(True)
                self.yy.setEnabled(True)



            elif self.xz_plane.isChecked():
                self.yy.setEnabled(False)
                self.yx.setEnabled(False)
                self.xy.setEnabled(False)
                self.yz.setEnabled(False)
                self.zy.setEnabled(False)

                self.xz.setEnabled(True)
                self.zx.setEnabled(True)
                self.xx.setEnabled(True)
                self.zz.setEnabled(True)
        
        elif self.plane_bool == False: 
            self.xy_plane.setEnabled(False)
            self.yz_plane.setEnabled(False)
            self.xz_plane.setEnabled(False)

            self.xx.setEnabled(True)
            self.xy.setEnabled(True)
            self.xz.setEnabled(True)
            self.yx.setEnabled(True)
            self.yy.setEnabled(True)
            self.yz.setEnabled(True)
            self.zx.setEnabled(True)
            self.zy.setEnabled(True)
            self.zz.setEnabled(True)

            return self.type, self.plane_bool

    def process_transform_material(self):
        if self.transformation.isChecked():
            self.angle = self.angle.value()

        else:
            self.angle.setEnabled(False)
        
        self.E = self.E.value()
        self.v=self.v.value()
        
    def process_tensor(self):
        if self.plane.isChecked():
            if self.xy_plane.isChecked():
                self.xz = 0
                self.yz = 0
                self.zy = 0
                self.zx = 0   

            elif self.yz_plane.isChecked():
                self.xz = 0
                self.zx = 0
                self.yx = 0
                self.xy = 0

            elif self.xz_plane.isChecked():
                self.yx = 0
                self.xy = 0
                self.yz = 0
                self.zy = 0
            
        constant = (self.E*(1-self.v))/((1+self.v)*(1-(2*self.v)))
        prop = array([
                [1,(self.v/(1-self.v)),(self.v/(1-self.v)),0,0,0],
                [(self.v/(1-self.v)),1,(self.v/(1-self.v)),0,0,0],
                [(self.v/(1-self.v)),(self.v/(1-self.v)),1,0,0,0],
                [0,0,0,(1-(2*self.v))/(2*(1-self.v)),0,0],
                [0,0,0,0,(1-(2*self.v))/(2*(1-self.v)),0],
                [0,0,0,0,0,(1-(2*self.v))/(2*(1-self.v))]
            ])

        if self.type == "Strain":
            if self.plane_bool:
                if self.plane_type == "Plane Strain":
                    if self.xy_plane.isChecked():
                        strain = array([
                        [self.xx],
                        [self.yy],
                        [0],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])
                    elif self.yz_plane.isChecked():
                        strain = array([
                        [0],
                        [self.yy],
                        [self.zz],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])

                    elif self.xz_plane.isChecked():
                        strain = array([
                        [self.xx],
                        [0],
                        [self.zz],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])
                elif self.plane_type == "Plane Stress":
                    if self.xz_plane.isChecked():
                        strain = array([
                        [self.xx],
                        [(-self.v/(1-self.v)) * (self.xx + self.zz)],
                        [self.zz],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])

                    elif self.xy_plane.isChecked():
                        strain = array([
                        [self.xx],
                        [self.yy],
                        [(-self.v/(1-self.v)) * (self.xx + self.yy)],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])

                    elif self.yz_plane.isChecked():
                        strain = array([
                        [(-self.v/(1-self.v)) * (self.zz + self.yy)],
                        [self.yy],
                        [self.zz],
                        [self.xy*2],
                        [self.xz*2], 
                        [self.yz*2]
                        ])

                    self.new_tensor = constant * (prop.dot(strain))

                    self.xx_new = self.new_tensor[0]
                    self.yy_new = self.new_tensor[1]
                    self.zz_new = self.new_tensor[2]
                    self.xy_new = self.new_tensor[3]
                    self.xz_new = self.new_tensor[4]
                    self.yz_new = self.new_tensor[5]
            else:
                    
                strain = array([
                    [self.xx],
                    [self.yy],
                    [self.zz],
                    [self.xy*2],
                    [self.xz*2], 
                    [self.yz*2]
                ])
                self.new_tensor = constant * (prop.dot(strain))

                self.xx_new = self.new_tensor[0]
                self.yy_new = self.new_tensor[1]
                self.zz_new = self.new_tensor[2]
                self.xy_new = self.new_tensor[3]
                self.xz_new = self.new_tensor[4]
                self.yz_new = self.new_tensor[5]

        elif self.type == "Stress":
            stress = array([
                [self.xx],
                [self.yy],
                [self.zz],
                [self.xy],
                [self.xz], 
                [self.yz]
            ])

            self.new_tensor = (1/constant)*(numpy.linalg.inv(prop).dot(stress))

            self.xx_new = self.new_tensor[0]
            self.yy_new = self.new_tensor[1]
            self.zz_new = self.new_tensor[2]
            self.xy_new = self.new_tensor[3]/2
            self.xz_new = self.new_tensor[4]/2
            self.yz_new = self.new_tensor[5]/2
        

        return self.xx_new,self.yy_new, self.zz_new, self.xy_new, self.xz_new, self.yz_new
    def onRun(self):
        self.process_type()
        self.process_data()
        self.process_transform_material()
        self.process_tensor()

        self.pages.setCurrentIndex(1)
        if self.type == "Strain":
            self.xx_label.setText("Oxx")
            self.yy_label.setText("Oyy")
            self.zz_label.setText("Ozz")
            self.xy_label.setText("Txy")
            self.xz_label.setText("Txz")
            self.yz_label.setText("Tyz")
        elif self.type == "Stress":

            self.xx_label.setText("exx")
            self.yy_label.setText("eyy")
            self.zz_label.setText("ezz")
            self.xy_label.setText("exy")
            self.xz_label.setText("exz")
            self.yz_label.setText("eyz")



        self.xx_out.setText(str(self.xx_new))
        self.yy_out.setText(str(self.yy_new))
        self.zz_out.setText(str(self.zz_new))
        self.xy_out.setText(str(self.xy_new))
        self.xz_out.setText(str(self.xz_new))
        self.yz_out.setText(str(self.yz_new))

        

  

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
        
    
