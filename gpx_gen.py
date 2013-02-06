#!   /usr/bin/env   python
#    coding: utf8

# Copyright CERN, 2013
# Author: Matthieu Cattin <matthieu.cattin@cern.ch>
# Licence: GPL v2 or later.


import sys
from datetime import date, timedelta
import xml.etree.ElementTree as et

def replace_date(element, new_date, verbose=False):
    # Search for all "time" tags
    times = element.findall(".//{http://www.topografix.com/GPX/1/1}time")
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

    return element


def add_track(root, track, name):
    root.append(track)
    

if __name__ == "__main__":


    input_file = "to_work.gpx"
    output_file = "to_work_out.gpx"

    ns = "http://www.topografix.com/GPX/1/1"
    day = date.today()


    tree = et.parse(input_file)

    et.register_namespace('', ns)

    root = tree.getroot()

    #print et.tostring(root, pretty_print=True)

    children = root.getchildren()

    #for child in children:
    #    print et.tostring(child, pretty_print=True)

    trk_tag = str(et.QName(ns, "trk"))
    #for track in root.getiterator(trk_tag):
    for track in root.findall(".//{http://www.topografix.com/GPX/1/1}trk"):
        root.append(track)
    for name in track.findall("./{http://www.topografix.com/GPX/1/1}name"):
        print name.text
        name.text = "from work"
        print name.text
    for text in track.findall(".//{http://www.topografix.com/GPX/1/1}text"):
            print text.text
            text.text = "from work"
            print text.text

    #print et.tostring(root)

    #print et.tostring(root)

    for track in root.getiterator(trk_tag):
        track = replace_date(track, day , False)
        day = day + timedelta(days=1)

    """

    #print root.nsmap
    #print root

    #print root.attrib
    #print root.attrib.get('xmlns')
    """

    print et.tostring(root)

    tree.write(output_file, xml_declaration=True, encoding='utf-8')

