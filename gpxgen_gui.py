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

from datetime import *
import xml.etree.ElementTree as et

# Constants declaration
FormClass = PyQt4.uic.loadUiType('gpxgen_gui.ui')[0]

class MainWindow(QMainWindow, FormClass):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

def selectToWorkFile():
    m.ToWorkFileEdit.setText(QFileDialog.getOpenFileName())

def selectFromWorkFile():
    m.FromWorkFileEdit.setText(QFileDialog.getOpenFileName())

def selectOutputFile():
    m.OutputFileEdit.setText(QFileDialog.getOpenFileName())

def handleSameTrackClicked():
    if bool(m.SameTrackCheckBox.checkState()):
        m.FromWorkButton.setEnabled(False)
        m.FromWorkLabel.setEnabled(False)
        m.FromWorkFileEdit.setEnabled(False)
    else:
        m.FromWorkButton.setEnabled(True)
        m.FromWorkLabel.setEnabled(True)
        m.FromWorkFileEdit.setEnabled(True)

def findFileInCurrentDir(f_to_find):
    files = filter(os.path.isfile, os.listdir(os.curdir))
    for f in files:
        if f_to_find == f:
            os.path.join(".", f)
            return f
    return ""

def addDayToList():
    date_to_add = m.RemoveDateEdit.date()
    m.DayToRemoveList.addItem(date_to_add.toString("MM-dd-yyyy"))

def clearList():
    m.DayToRemoveList.clear()

def delDay():
    print("Delete Day")

def replace_lap_date(lap, new_date, verbose=False):
    # Format new date
    new_date = new_date.strftime("%Y-%m-%d")
    # Replace Lap tag StartTime
    old_date, old_time = lap.get("StartTime").split('T')
    lap.set("StartTime", new_date+"T"+old_time)
    # Search for all "time" tags
    times = lap.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time")
    if verbose==True:
        print("Found %d tags"%(len(times)))
    # Loop through "time" tags and replace the date
    for time in times:
        old_date, old_time = time.text.split('T')
        time.text = new_date+"T"+old_time
        if verbose==True:
            print("Found date:%s replaced by:%s"%(old_date, new_date))

def get_laps(root, verbose=False):
    laps = root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap")
    if verbose==True:
        print("Number of lap(s): %d"%(len(laps)))
        for lap in laps:
            print "Lap : ", lap
    return laps, len(laps)

def get_activity(root, verbose=False):
    activity = root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity")
    if verbose==True:
        print("Number of activity: %d"%(len(activity)))
        for activ in activity:
            print "Activity : ", activity
    return activity, len(activity)

def get_activities(root, verbose=False):
    activities = root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activities")
    if verbose==True:
        print "Activities : ", activities
    return activities[0]

def add_lap(activity, lap, verbose=False):
    if verbose==True:
        print "Adding one lap!"
    activity.append(et.fromstring(et.tostring(lap)))

def add_activity(activities, activity, verbose=False):
    if verbose==True:
        print "Adding one activity!"
    activities.append(et.fromstring(et.tostring(activity)))

def check_file(f):
    ok = 0
    if f == "" or f[-4:] != ".tcx":
        print("Enter a .tcx file")
        QMessageBox.warning(m, 'Message Title', 'Please enter a .tcx file', QMessageBox.Ok)
        ok = -1
    return ok

def generateGpx():
    f_to_work = m.ToWorkFileEdit.text()
    f_from_work = m.FromWorkFileEdit.text()
    same_track = bool(m.SameTrackCheckBox.checkState())
    f_out = m.OutputFileEdit.text()
    start_date = m.StartDateEdit.date()
    end_date = m.EndDateEdit.date()
    remove_weekends = bool(m.RemoveWeekendsCheckBox.checkState())
    days_to_remove = m.DayToRemoveList.findItems("*", PyQt4.QtCore.Qt.MatchWildcard)

    print "track to work input file: ",f_to_work
    print "track from work input file: ",f_from_work
    print "from work same track as to work: ",same_track
    print "output file: ",f_out

    ok = 0
    ok += check_file(f_to_work)
    if not(same_track):
        ok += check_file(f_from_work)
    ok += check_file(f_out)
    if ok < 0:
        return

    # Convert Qdate in normal date
    start_date = start_date.toPyDate()
    end_date = end_date.toPyDate()
    print "start date: ",start_date
    print "end date  : ",end_date
    print "remove weekends from date range :",remove_weekends

    # Convert list items in date
    remove_date = []
    for d in days_to_remove:
        remove_date.append(datetime.strptime(str(d.text()), "%m-%d-%Y"))
    remove_date = [remove_date[i].date() for i in range(len(remove_date))]
    print("%d days to remove"%len(days_to_remove))

    # xml name space
    ns = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
    et.register_namespace('', ns)

    # Parse to_work file, also used to build the output file
    tree = et.parse(f_to_work)
    root = tree.getroot()

    if same_track:
        laps, nb_laps = get_laps(root, False)
    else:
        # Parse from_work file
        tree_2 = et.parse(f_from_work)
        root_2 = tree_2.getroot()
        laps, nb_laps = get_laps(root_2, False)

    # Input file must have only 1 lap
    if nb_laps == 1:
        # Add the way back from work
        activity, nb_activity = get_activity(root, False)
        add_lap(activity[0], laps[0], False)
    else:
        print("Input file MUST have only one lap! Your file has %d laps."%nb_laps)
        return

    #if same_track:
        # rename the "way back from work" track in from_work
        #tracks, nb_tracks = get_tracks(root, False)
        #rename_track(root, tracks[-1], "from_work", False)

    # replace the date on the two laps (to_work and from_work)
    laps, nb_laps = get_laps(root, False)
    day = start_date
    print day," : KEEP"
    replace_lap_date(laps[0], day)
    replace_lap_date(laps[1], day)

    # if more than one day, copy the two laps
    if end_date != start_date:
        while day < end_date:
            day = day + timedelta(days=1)

            if day.weekday() > 4 and remove_weekends:
                print day," : REMOVE (weekend day)"
                continue

            if day in remove_date:
                print day," : REMOVE"
                continue

            print day," : KEEP"
            activities= get_activities(root, False)
            activity, nb_activity = get_activity(root, False)
            add_activity(activities, activity[0])

            # replace the date of the laps on the copied activity
            laps, nb_laps = get_laps(root, False)
            replace_lap_date(laps[-2], day)
            replace_lap_date(laps[-1], day)

    # save to output file
    tree.write(f_out, xml_declaration=True, encoding='utf-8')

    print("Output file generated!")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    m.setWindowTitle("TCXgen")
    m.setFixedSize(661,548)

    # Initialize display fields
    m.StartDateEdit.setDate(date.today())
    m.EndDateEdit.setDate(date.today())
    m.RemoveDateEdit.setDate(date.today())
    m.statusbar.showMessage("Designed by: mcattin")
    m.ToWorkFileEdit.setText(findFileInCurrentDir("to_work.tcx"))
    m.FromWorkFileEdit.setText(findFileInCurrentDir("from_work.tcx"))
    m.OutputFileEdit.setText(findFileInCurrentDir("out.tcx"))
    handleSameTrackClicked()

    # Connect events to callback functions
    m.ToWorkButton.clicked.connect(selectToWorkFile)
    m.FromWorkButton.clicked.connect(selectFromWorkFile)
    m.OutputButton.clicked.connect(selectOutputFile)
    m.GenerateButton.clicked.connect(generateGpx)
    m.SameTrackCheckBox.stateChanged.connect(handleSameTrackClicked)
    m.AddDayButton.clicked.connect(addDayToList)
    m.ClearListButton.clicked.connect(clearList)

    # Starts Qt applic
    app.exec_()
