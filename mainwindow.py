# This Python file uses the following encoding: utf-8
from cmath import sin
from logging import raiseExceptions
import os
from pathlib import Path
import sys

import numpy 
from numpy import array 
from numpy import math 
from math import sin,cos
from PyQt5 import QtWidgets, uic

stress_units = ['Pa', "KPa", 'MPa', 'GPa']
stress_units_values = array([1,10**3,10**6, 10**9])
strain_units = ['Generic', 'MicroStrain']
strain_units_values = array([1, 10**-6])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("form.ui", self)
        self.show()
        self.process_type()
        self.E_units.addItems(stress_units)
        self.stress_input.toggled.connect(self.process_units)
        self.strain_input.toggled.connect(self.process_units)
        self.plane.toggled.connect(self.process_type)
        self.xy_plane.toggled.connect(self.process_type)
        self.yz_plane.toggled.connect(self.process_type)
        self.xz_plane.toggled.connect(self.process_type)
        self.run.clicked.connect(self.onRun)
        self._return.clicked.connect(self.onReturn)
        self.transformation.clicked.connect(self.process_type)
    
        
    def onReturn(self):
        self.close()
        self.__init__()
    
    def process_units(self):
        if self.stress_input.isChecked():
            self.units_dropdown.clear()
            self.units_dropdown.addItems(stress_units)

        elif self.strain_input.isChecked():
            self.units_dropdown.clear()
            self.units_dropdown.addItems(strain_units)
        
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
            [self.xx, self.xy, self.xz],
            [self.yx, self.yy, self.yz],
            [self.zx, self.zy, self.zz]
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
        
        if self.transformation.isChecked():
            self.angle.setEnabled(True)

        
        if self.transformation.isChecked() == False:
            self.angle.setEnabled(False)

        if self.plane.isChecked():
            self.plane_bool = True
            if self.plane_stress.isChecked():
                self.plane_type = "Plane Stress"
            elif self.plane_strain.isChecked():
                self.plane_type = "Plane Strain"

        elif self.plane.isChecked() == False: 
            self.plane_bool = False

        if self.plane_bool:
            self.xy_plane.setEnabled(True)
            self.yz_plane.setEnabled(True)
            self.xz_plane.setEnabled(True)
            self.plane_strain.setEnabled(True)
            self.plane_stress.setEnabled(True)

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
            self.plane_strain.setEnabled(False)
            self.plane_stress.setEnabled(False)

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

    def process_material(self):
        index = self.E_units.currentIndex()
        E_unit = stress_units_values[index]
        E = self.E.value()
        self.E = E * E_unit 
        self.v=self.v.value()
        
    def process_tensor(self):

        if self.type == "Stress":
            index = self.units_dropdown.currentIndex()
            stress_unit = stress_units_values[index]
        elif self.type == "Strain": 
            index = self.units_dropdown.currentIndex()
            strain_unit = strain_units_values[index]
        
        if self.transformation.isChecked() == True and self.type == "Stress":
            index = self.units_dropdown.currentIndex()
            stress_unit = stress_units_values[index]
        
        elif self.transformation.isChecked() == True and self.type == "Strain":
            index = self.units_dropdown.currentIndex()
            strain_unit = strain_units_values[index]
    
            
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

        if self.transformation.isChecked() == False:
            constant = (self.E*(1-self.v))/((1+self.v)*(1-(2*self.v)))
            prop = array([
                    [1,(self.v/(1-self.v)),(self.v/(1-self.v)),0,0,0],
                    [(self.v/(1-self.v)),1,(self.v/(1-self.v)),0,0,0],
                    [(self.v/(1-self.v)),(self.v/(1-self.v)),1,0,0,0],
                    [0,0,0,(1-(2*self.v))/(2*(1-self.v)),0,0],
                    [0,0,0,0,(1-(2*self.v))/(2*(1-self.v)),0],
                    [0,0,0,0,0,(1-(2*self.v))/(2*(1-self.v))]
                    ])

        elif self.transformation.isChecked():
            self.angle = self.angle.value()
            a = self.angle
            Q = array([
                [cos(a), -sin(a), 0],
                [sin(a), cos(a), 0],
                [0,0,1]
                ])  
            Q_t = numpy.matrix.transpose(Q)
            self.new_tensor = Q_t @ self.tensor @ Q 

            self.xx_new = self.new_tensor[0]
            self.yy_new = self.new_tensor[1]
            self.zz_new = self.new_tensor[2]
            self.xy_new = self.new_tensor[3]
            self.xz_new = self.new_tensor[4]
            self.yz_new = self.new_tensor[5]
            
   
        if self.type == "Strain" and self.transformation.isChecked() == False:
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

            else:   
                strain = array([
                    [self.xx],
                    [self.yy],
                    [self.zz],
                    [self.xy*2],
                    [self.xz*2], 
                    [self.yz*2]
                ])

            self.new_tensor = constant * (prop.dot(strain_unit * strain))

            self.xx_new = self.new_tensor[0]
            self.yy_new = self.new_tensor[1]
            self.zz_new = self.new_tensor[2]
            self.xy_new = self.new_tensor[3]
            self.xz_new = self.new_tensor[4]
            self.yz_new = self.new_tensor[5]

        elif self.type == "Stress" and self.transformation.isChecked() == False:
            if self.plane_bool:
                if self.plane_type == "Plane Stress":
                    if self.xy_plane.isChecked():
                        stress = array([
                        [self.xx],
                        [self.yy],
                        [0],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

                        
                    elif self.yz_plane.isChecked():
                        stress = array([
                        [0],
                        [self.yy],
                        [self.zz],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

                  
                    elif self.xz_plane.isChecked():
                        stress = array([
                        [self.xx],
                        [0],
                        [self.zz],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

                     
                elif self.plane_type == "Plane Strain":
                    if self.xy_plane.isChecked():
                        stress = array([
                        [self.xx],
                        [self.yy],
                        [self.v * (self.xx+self.yy)],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

                 

                    elif self.yz_plane.isChecked():
                        stress = array([
                        [self.v * (self.yy + self.zz)],
                        [self.yy],
                        [self.zz],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

                       
                    elif self.xz_plane.isChecked():
                        stress = array([
                        [self.xx],
                        [self.v * (self.xx + self.zz)],
                        [self.zz],
                        [self.xy],
                        [self.xz], 
                        [self.yz]
                        ])

            else: 
                stress = array([
                    [self.xx],
                    [self.yy],
                    [self.zz],
                    [self.xy],
                    [self.xz], 
                    [self.yz]
                    ])
        
            self.new_tensor = (1/constant)*(numpy.linalg.inv(prop).dot(stress_unit * stress))

            self.xx_new = self.new_tensor[0]
            self.yy_new = self.new_tensor[1]
            self.zz_new = self.new_tensor[2]
            self.xy_new = self.new_tensor[3]/2
            self.xz_new = self.new_tensor[4]/2
            self.yz_new = self.new_tensor[5]/2
    
        
        if self.type == "Strain" and self.transformation.isChecked() == False:
            self.u = (1/2) * (numpy.tensordot(self.new_tensor, strain))
        elif self.type == "Stress" and self.transformation.isChecked() == False:
            self.u = (1/2) * (numpy.tensordot(stress,self.new_tensor))

    def change_output(self):
        if self.type == "Stress":
            index = self.output_unit.currentIndex()
            self.out_unit = strain_units_values[index]
        elif self.type == "Strain":
            index = self.output_unit.currentIndex()
            self.out_unit = stress_units_values[index]
        self.xx_out.setText(str(self.xx_new/self.out_unit))
        self.yy_out.setText(str(self.yy_new/self.out_unit))
        self.zz_out.setText(str(self.zz_new/self.out_unit))
        self.xy_out.setText(str(self.xy_new/self.out_unit))
        self.xz_out.setText(str(self.xz_new/self.out_unit))
        self.yz_out.setText(str(self.yz_new/self.out_unit))


    def onRun(self):
        self.process_type()
        self.process_data()
        self.process_material()
        self.process_tensor()
        
        if self.type == 'Strain':
            self.output_unit.addItems(stress_units)
        elif self.type == "Stress":
            self.output_unit.addItems(strain_units)

        self.output_unit.currentIndexChanged.connect(self.change_output)
        self.change_output()
        
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

        self.xx_out.setText(str(self.xx_new/self.out_unit))
        self.yy_out.setText(str(self.yy_new/self.out_unit))
        self.zz_out.setText(str(self.zz_new/self.out_unit))
        self.xy_out.setText(str(self.xy_new/self.out_unit))
        self.xz_out.setText(str(self.xz_new/self.out_unit))
        self.yz_out.setText(str(self.yz_new/self.out_unit))
        self.strain_energy.setText(str(self.u))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
        
    
