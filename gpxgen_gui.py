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

def replace_track_date(track, new_date, verbose=False):
    # Search for all "time" tags
    times = track.findall(".//{http://www.topografix.com/GPX/1/1}time")
    if verbose==True:
        print("Found %d tags"%(len(times)))
    # Format new date
    new_date = new_date.strftime("%Y-%m-%d")
    # Loop through "time" tags and replace the date
    for time in times:
        old_date, old_time = time.text.split('T')
        time.text = new_date+"T"+old_time
        if verbose==True:
            print("Found date:%s replaced by:%s"%(old_date, new_date))

def get_tracks(root, verbose=False):
    tracks = root.findall(".//{http://www.topografix.com/GPX/1/1}trk")
    if verbose==True:
        print("Number of track(s): %d"%(len(tracks)))
        for track in tracks:
            print track
    return tracks, len(tracks)

def add_track(root, track, verbose=False):
    root.append(et.fromstring(et.tostring(track)))

def rename_track(root, track, name, verbose=False):
    trk_name = track.findall("./{http://www.topografix.com/GPX/1/1}name")
    trk_text = track.findall(".//{http://www.topografix.com/GPX/1/1}text")
    if verbose==True:
        print("Track name, old: %s, new: %s"%(trk_name[0].text, name))
    trk_name[0].text = name
    trk_text[0].text = name

def check_file(f):
    ok = 0
    if f == "" or f[-4:] != ".gpx":
        print("Enter a .gpx file")
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

    print f_to_work
    print f_from_work
    print same_track
    print f_out
    print start_date
    print end_date
    print remove_weekends
    print("%d days to remove"%len(days_to_remove))
    print days_to_remove

    ok = 0
    ok += check_file(f_to_work)
    ok += check_file(f_from_work)
    ok += check_file(f_out)
    if ok < 0:
        return

    # Convert Qdate in normal date
    start_date = start_date.toPyDate()
    end_date = end_date.toPyDate()
    #start_date = start_date.strftime("%Y-%m-%d")
    #end_date = end_date.strftime("%Y-%m-%d")
    print start_date
    print end_date

    # xml name space
    ns = "http://www.topografix.com/GPX/1/1"
    et.register_namespace('', ns)

    # Parse to_work file, also used to build the output file
    tree = et.parse(f_to_work)
    root = tree.getroot()

    # Parse from_work file
    tree_2 = et.parse(f_from_work)
    root_2 = tree_2.getroot()

    if same_track:
        tracks, nb_tracks = get_tracks(root, False)
    else:
        tracks, nb_tracks = get_tracks(root_2, False)

    # Input file must have only 1 track
    if nb_tracks == 1:
        # Add the way back from work
        add_track(root, tracks[0])
    else:
        print("Input file MUST have only one track! Your file has %d tracks."%nb_tracks)

    if same_track:
        # rename the "way back from work" track in from_work
        tracks, nb_tracks = get_tracks(root, False)
        rename_track(root, tracks[-1], "from_work", False)

    # replace the date on the two tracks (to_work and from_work)
    day = start_date
    replace_track_date(tracks[0], day)
    replace_track_date(tracks[1], day)

    # if more than one day, copy the two tracks
    if end_date != start_date:
        while day < end_date:
            day = day + timedelta(days=1)

            print day, day.weekday()

            if day.weekday() > 4 and remove_weekends:
                print("Weekend")
                continue
            tracks, nb_tracks = get_tracks(root, False)
            add_track(root, tracks[0])
            add_track(root, tracks[1])

            # replace the date on the copied tracks
            tracks, nb_tracks = get_tracks(root, False)
            replace_track_date(tracks[-2], day)
            replace_track_date(tracks[-1], day)

    # save to output file
    tree.write(f_out, xml_declaration=True, encoding='utf-8')


if __name__ == "__main__":

    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    m.setWindowTitle("GPXgen")

    # Initialize display fields
    m.StartDateEdit.setDate(date.today())
    m.EndDateEdit.setDate(date.today())
    m.RemoveDateEdit.setDate(date.today())
    m.statusbar.showMessage("Designed by: mcattin")
    m.ToWorkFileEdit.setText(findFileInCurrentDir("to_work.gpx"))
    m.FromWorkFileEdit.setText(findFileInCurrentDir("from_work.gpx"))
    m.OutputFileEdit.setText(findFileInCurrentDir("out.gpx"))

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
