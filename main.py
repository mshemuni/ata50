# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:52:52 2018

@author: mshem
"""

import io

from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from ata50 import Ui_Form
from PyQt5 import QtWidgets

from sys import argv
from os import mkdir

import gui as g

from time import time
from datetime import datetime

from astropy.coordinates import Angle
from astropy import units as U

from os.path import isfile, isdir

import subprocess

from MyEns import cat
from MyEns import astro

from glob import glob

class MyForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, verb=True):
        super(MyForm, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.cat = cat.query()
        self.tim = astro.time()
        
        self.toggle_obervation()
        self.get_now()
        
        self.reload_record_obs()
        self.add_region()
        self.add_area()
        self.add_dev()
        self.add_prob()
        
        self.verb = verb
        
        self.ui.tabWidget.setTabEnabled(2,False)
        self.ui.tabWidget_2.setTabEnabled(2,False)
        
        
        self.ui.pushButton_2.clicked.connect(lambda: (self.get_now()))
        self.ui.pushButton_7.clicked.connect(lambda: (self.get_now2()))
        self.ui.comboBox.currentTextChanged.connect(lambda: (
                self.fill_combos()))
        
        self.ui.comboBox_3.currentTextChanged.connect(lambda: (
                self.add_area()))
        
        self.ui.comboBox_4.currentTextChanged.connect(lambda: (
                self.add_dev()))
        
        self.ui.comboBox_5.currentTextChanged.connect(lambda: (
                self.add_prob()))
        
        self.ui.comboBox_6.currentTextChanged.connect(lambda: (
                self.read_prob()))
        
        self.ui.pushButton_4.clicked.connect(lambda: (self.create_obs()))
        self.ui.pushButton_6.clicked.connect(lambda: (self.create_pro()))
        
        self.ui.pushButton_3.clicked.connect(lambda: (self.get_coors()))
        
        self.ui.listWidget.clicked.connect(lambda: (self.get_obs()))
        self.ui.listWidget_2.clicked.connect(lambda: (self.get_pro()))
        
        
        self.reload_record_obs()
        self.reload_record_pro()
            
    def get_pro(self):
        t = datetime.now()
        if self.ui.listWidget_2.currentItem() is not None:
            file = self.ui.listWidget_2.currentItem().text()
        if isdir("report/{}".format(t.strftime('%Y-%m-%d'))):
            the_file = "report/{}/{}".format(t.strftime('%Y-%m-%d'), file)
            tree = ET.parse(the_file)
            root = tree.getroot()
            for child in root:
                if child.tag == "date":
                    dat = datetime.strptime(child.text, '%Y-%m-%dT%H-%M-%S')
                    self.ui.dateTimeEdit_2.setDateTime(dat)
                if child.tag == "id":
                    self.ui.comboBox.setCurrentText(child.text)
                if child.tag == "type":
                    self.ui.comboBox_3.setCurrentText(child.text)
                if child.tag == "area":
                    self.ui.comboBox_4.setCurrentText(child.text)
                if child.tag == "device":
                    self.ui.comboBox_5.setCurrentText(child.text)
                if child.tag == "problem":
                    self.ui.comboBox_6.setCurrentText(child.text)
                if child.tag == "comm":
                    self.ui.plainTextEdit_2.setPlainText(child.text)
        
    def get_obs(self):
        t = datetime.now()
        if self.ui.listWidget.currentItem() is not None:
            file = self.ui.listWidget.currentItem().text()
        if isdir("report/{}".format(t.strftime('%Y-%m-%d'))):
            the_file = "report/{}/{}".format(t.strftime('%Y-%m-%d'), file)
            tree = ET.parse(the_file)
            root = tree.getroot()
            for child in root:
                if child.tag == "type":
                    self.ui.comboBox.setCurrentText(child.text)
                if child.tag == "date":
                    dat = datetime.strptime(child.text, '%Y-%m-%dT%H-%M-%S')
                    self.ui.dateTimeEdit.setDateTime(dat)
                if child.tag == "observers":
                    self.ui.lineEdit_5.setText(child.text)
                if child.tag == "id":
                    self.ui.lineEdit_4.setText(child.text)
                if child.tag == "exptime":
                    self.ui.doubleSpinBox.setValue(float(child.text))
                if child.tag == "filter":
                    self.ui.comboBox_2.setCurrentText(child.text)
                if child.tag == "object_name":
                    self.ui.lineEdit.setText(child.text)
                if child.tag == "ra":
                    self.ui.lineEdit_2.setText(child.text)
                if child.tag == "dec":
                    self.ui.lineEdit_3.setText(child.text)
                    
                if child.tag == "BMag":
                    self.ui.doubleSpinBox_2.setValue(float(child.text))
                if child.tag == "VMag":
                    self.ui.doubleSpinBox_3.setValue(float(child.text))
                if child.tag == "RMag":
                    self.ui.doubleSpinBox_4.setValue(float(child.text))
                    
                if child.tag == "weather":
                    self.ui.comboBox_19.setCurrentText(child.text)
                    
                if child.tag == "comm":
                    self.ui.plainTextEdit.setPlainText(child.text)
        
    def reload_record_obs(self):
        t = datetime.now()
        
        if isdir("report/{}".format(t.strftime('%Y-%m-%d'))):
            files = sorted(glob("report/{}/*obs.xml".format(
                    t.strftime('%Y-%m-%d'))))
            
            all_list = []
            for i in files:
                all_list.append(i.split("\\")[1])
                
            g.replace_list_con(self, self.ui.listWidget, all_list)
            
    def reload_record_pro(self):
        t = datetime.now()
        
        if isdir("report/{}".format(t.strftime('%Y-%m-%d'))):
            files = sorted(glob("report/{}/*pro.xml".format(
                    t.strftime('%Y-%m-%d'))))
            
            all_list = []
            for i in files:
                all_list.append(i.split("\\")[1])
                
            g.replace_list_con(self, self.ui.listWidget_2, all_list)
        
    def fill_combos(self):
        if self.ui.comboBox.currentText() == "Obje":
            self.ui.doubleSpinBox.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.doubleSpinBox_2.setEnabled(True)
            self.ui.doubleSpinBox_3.setEnabled(True)
            self.ui.doubleSpinBox_4.setEnabled(True)
            self.ui.comboBox_19.setEnabled(True)
            self.ui.plainTextEdit.setEnabled(True)
            
        elif self.ui.comboBox.currentText() == "Bias":
            self.ui.doubleSpinBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            self.ui.comboBox_19.setEnabled(True)
            self.ui.plainTextEdit.setEnabled(True)
            
        elif self.ui.comboBox.currentText() == "Dark":
            self.ui.doubleSpinBox.setEnabled(True)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            self.ui.comboBox_19.setEnabled(True)
            self.ui.plainTextEdit.setEnabled(True)
            
        elif self.ui.comboBox.currentText() == "Dark":
            self.ui.doubleSpinBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            self.ui.comboBox_19.setEnabled(True)
            self.ui.plainTextEdit.setEnabled(True)

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def create_pro(self):
        tm = self.ui.dateTimeEdit_2.dateTime().toString('yyyy-MM-ddTHH-mm-ss')
        dt = self.ui.dateTimeEdit_2.dateTime().toString('yyyy-MM-dd')
        the_id = self.ui.dateTimeEdit_2.dateTime().toString('yyyyMMddHHmmss')
        
        the_folder = "report/{}".format(dt)
        
        if not isdir(the_folder):
            mkdir(the_folder)
            
        file = "report/{}/{}_pro.xml".format(dt, tm)
        
        top = Element('top')
    
        comment = Comment('Generated for ATA50')
        top.append(comment)
        
        dat= SubElement(top, 'date')
        dat.text = str(tm)
        
        xml_id= SubElement(top, 'id')
        xml_id.text = str(the_id)
        
        typ= SubElement(top, 'type')
        typ.text = str(self.ui.comboBox_3.currentText())
        
        are = SubElement(top, 'area')
        are.text = str(self.ui.comboBox_4.currentText())
        
        dev = SubElement(top, 'device')
        dev.text = str(self.ui.comboBox_5.currentText())
        
        pro = SubElement(top, 'problem')
        pro.text = str(self.ui.comboBox_6.currentText())
        
        sol = SubElement(top, 'solved')
        sol.text = str("N")
        
        comm = SubElement(top, 'comm')
        comm.text = str(self.ui.plainTextEdit_2.toPlainText())
        
        with io.open(file, "w", encoding="utf-8") as f:
            f.write(self.prettify(top))
            
        print("asd")
            
        self.reload_record_pro()
        
    def create_obs(self):
        tm = self.ui.dateTimeEdit.dateTime().toString('yyyy-MM-ddTHH-mm-ss')
        dt = self.ui.dateTimeEdit.dateTime().toString('yyyy-MM-dd')
        the_id = self.ui.dateTimeEdit.dateTime().toString('yyyyMMddHHmmss')
        
        the_folder = "report/{}".format(dt)
        
        if not isdir(the_folder):
            mkdir(the_folder)
            
        file = "report/{}/{}_obs.xml".format(dt, tm)
        
        top = Element('top')
    
        comment = Comment('Generated for ATA50')
        top.append(comment)
        
        file_type = SubElement(top, 'type')
        file_type.text = str(self.ui.comboBox.currentText())
        
        date = SubElement(top, 'date')
        date.text = tm
        
        observers = SubElement(top, 'observers')
        observers.text = str(self.ui.lineEdit_5.text().strip())
        
        xml_id = SubElement(top, 'id')
        xml_id.text = str(the_id)
        
        exptime = SubElement(top, 'exptime')
        exptime.text = str(self.ui.doubleSpinBox.value())
        
        the_filter = SubElement(top, 'filter')
        the_filter.text = str(self.ui.comboBox_2.currentText())
        
        object_name = SubElement(top, 'object_name')
        object_name.text = str(self.ui.lineEdit.text().strip())
                
        ra = SubElement(top, 'ra')
        ra.text = str(self.ui.lineEdit_2.text().strip())
        
        dec = SubElement(top, 'dec')
        dec.text = str(self.ui.lineEdit_3.text().strip())
        
        BMag = SubElement(top, 'BMag')
        BMag.text = str(self.ui.doubleSpinBox_2.value())
        
        VMag = SubElement(top, 'VMag')
        VMag.text = str(self.ui.doubleSpinBox_3.value())
        
        RMag = SubElement(top, 'RMag')
        RMag.text = str(self.ui.doubleSpinBox_4.value())
        
        weather = SubElement(top, 'weather')
        weather.text = str(
                self.ui.comboBox_19.currentText().split("(")[0].strip())
        
        comm = SubElement(top, 'comm')
        comm.text = str(self.ui.plainTextEdit.toPlainText())
        
        with io.open(file, "w", encoding="utf-8") as f:
            f.write(self.prettify(top))
            
        self.reload_record_obs()
        
        
    def get_now(self):
        ts = time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        the_time = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
        self.ui.dateTimeEdit.setDateTime(the_time)
        self.ui.dateTimeEdit_2.setDateTime(the_time)
        
    def get_now2(self):
        ts = time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        the_time = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
        self.ui.dateTimeEdit_2.setDateTime(the_time)
        
    def get_coors(self):
        if not self.ui.lineEdit.text() == "":
            obj = self.cat.name(self.ui.lineEdit.text())
            self.ui.lineEdit.setText(self.ui.lineEdit.text().upper())
            if not len(obj) == 0:
                ra = obj[0]["RAJ2000"][0]
                dec = obj[0]["DEJ2000"][0]
                
                name = obj[0]['NOMAD1'][0]
                
                bmag = obj[0]["Bmag"][0]
                vmag = obj[0]["Vmag"][0]
                rmag = obj[0]["Rmag"][0]
                
                ra = Angle("{}d".format(str(ra)))
                the_ra = ra.to_string(unit=U.degree, sep=':')
                
                dec = Angle("{}d".format(str(dec)))
                the_dec = dec.to_string(unit=U.degree, sep=':')

                
                self.ui.lineEdit_2.setText(str(the_ra))
                self.ui.lineEdit_3.setText(str(the_dec))
                
                try:
                    bmag = float(bmag)
                except:
                    bmag = ""
                    
                try:
                    vmag = float(vmag)
                except:
                    vmag = ""
                    
                try:
                    rmag = float(rmag)
                except:
                    rmag = ""
                
                if type(bmag) == float:
                    self.ui.doubleSpinBox_2.setValue(bmag)
                if type(vmag) == float:
                    self.ui.doubleSpinBox_3.setValue(vmag)
                if type(rmag) == float:
                    self.ui.doubleSpinBox_4.setValue(rmag)
                    
                cur_text = self.ui.plainTextEdit.toPlainText()
                if not cur_text == "":
                    self.ui.plainTextEdit.setPlainText(
                        QtWidgets.QApplication.translate(
                                "Form", "{}\nNomad adı: {}".format(
                                        cur_text, name), None))
                else:
                    self.ui.plainTextEdit.setPlainText(
                        QtWidgets.QApplication.translate(
                                "Form", "Nomad adı: {}".format(name), None))
                
            else:
                QtWidgets.QMessageBox.critical(
                        self, ("ATA50"), ("Bilinmeyen Obje."))
        else:
            QtWidgets.QMessageBox.critical(
                    self, ("ATA50"), ("Lütfen 'Obje Adı' alanını doldurunuz."))
        
    def toggle_obervation(self):
        
        if self.ui.comboBox.currentIndex() == 0:
            self.ui.doubleSpinBox.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.doubleSpinBox_2.setEnabled(True)
            self.ui.doubleSpinBox_3.setEnabled(True)
            self.ui.doubleSpinBox_4.setEnabled(True)
            
        elif self.ui.comboBox.currentIndex() == 1:
            self.ui.doubleSpinBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            
        elif self.ui.comboBox.currentIndex() == 2:
            self.ui.doubleSpinBox.setEnabled(True)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            
        elif self.ui.comboBox.currentIndex() == 3:
            self.ui.doubleSpinBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.lineEdit_3.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)   
            
            
    def add_region(self):
        folder = sorted(glob("problem/*"))
        self.ui.comboBox_3.clear()
        for i in folder:
            line = i.split("\\")[-1]
            if line[0].isupper():
                self.ui.comboBox_3.addItem(line)
                
    def add_area(self):
        folder = sorted(glob("problem/{}/*".format(
                self.ui.comboBox_3.currentText())))
        self.ui.comboBox_4.clear()
        for i in folder:
            line = i.split("\\")[-1]
            if line[0].isupper():
                self.ui.comboBox_4.addItem(line)
                
    def add_dev(self):
        folder = sorted(glob("problem/{}/{}/*".format(
                self.ui.comboBox_3.currentText(), 
                self.ui.comboBox_4.currentText())))
        self.ui.comboBox_5.clear()
        for i in folder:
            line = i.split("\\")[-1]
            if line[0].isupper():
                self.ui.comboBox_5.addItem(line)
                
    def add_prob(self):
        folder = sorted(glob("problem/{}/{}/{}/*".format(
                self.ui.comboBox_3.currentText(), 
                self.ui.comboBox_4.currentText(), 
                self.ui.comboBox_5.currentText())))
        self.ui.comboBox_6.clear()
        for i in folder:
            line = i.split("\\")[-1]
            if line[0].isupper():
                self.ui.comboBox_6.addItem(line)
                
        self.read_prob()
                
    def read_prob(self):
        file = "./problem/{}/{}/{}/{}".format(
                self.ui.comboBox_3.currentText(),
                self.ui.comboBox_4.currentText(),
                self.ui.comboBox_5.currentText(),
                self.ui.comboBox_6.currentText())
        if file == "./problem/Teknik/Teleskop Binası/Bilgisayar/Veri":
            if self.ping("1", "10.141.3.219"):
                QtWidgets.QMessageBox.information(
                        self, ("ATA50"), ("Üniversite içi bağlantı var!"))
            else:
                QtWidgets.QMessageBox.critical(
                        self, ("ATA50"), ("Üniversite içi bağlantı yok!"))
        if isfile(file):
            cont = open(file, "r")
            ret = ""
            for i in cont:
                ret = "{}\n{}".format(ret, i)
            self.ui.plainTextEdit_3.setPlainText(
                    QtWidgets.QApplication.translate(
                            "Form", ret[1:], None))
        
    def ping(self, count, target):
        try:
            ret = subprocess.check_output(["ping","-n",count,target])
            output = str(ret)
            if "unreachable" in output or "100% loss" in output:
                return False
            else:
                return True
        except:
            return False
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)        
    f = MyForm(verb=True)
    f.show()
    app.exec_()