#!/usr/bin/python
#    coding: utf8

import sys
import time
import os
import math

import PyQt4
import PyQt4.QtGui
import PyQt4.QtCore
import PyQt4.uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Constants declaration
FormClass = PyQt4.uic.loadUiType('gpxgen_gui.ui')[0]

class MainWindow(QMainWindow, FormClass):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

def selectToWorkFile():
    m.ToWorkFile.setText(QFileDialog.getOpenFileName())

def selectFromWorkFile():
    m.FromWorkFile.setText(QFileDialog.getOpenFileName())

def handleSameTrackClicked():
    if bool(m.SameTrackCheckBox.checkState()):
        m.FromWorkButton.setEnabled(False)
        m.FromWorkLabel.setEnabled(False)
        m.FromWorkFile.setEnabled(False)
    else:
        m.FromWorkButton.setEnabled(True)
        m.FromWorkLabel.setEnabled(True)
        m.FromWorkFile.setEnabled(True)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    m.setWindowTitle("GPXgen")


    # Initialize display fields
    m.statusbar.showMessage("Designed by: mcattin")
    # TODO: init ToWorkFile and FromWorkFile field with to_work.gpx and from_work.gpx if found in the current directory


    # Connect events to callback functions
    m.ToWorkButton.clicked.connect(selectToWorkFile)
    m.FromWorkButton.clicked.connect(selectFromWorkFile)
    m.SameTrackCheckBox.stateChanged.connect(handleSameTrackClicked)

    # Starts Qt applic
    app.exec_()
