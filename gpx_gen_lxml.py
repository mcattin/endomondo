#!   /usr/bin/env   python
#    coding: utf8

# Copyright CERN, 2013
# Author: Matthieu Cattin <matthieu.cattin@cern.ch>
# Licence: GPL v2 or later.


import sys
from datetime import date
import lxml.etree as et
from xml.etree.ElementTree import QName

def replace_date(tree, new_date, verbose=False):
    # Get tree's root
    root = tree.getroot()

    # Search for all "time" tags
    times = root.findall(".//{http://www.topografix.com/GPX/1/1}time")

    # Format new date
    new_date = new_date.strftime("%Y-%m-%d")

    # Loop through "time" tags and replace the date
    for time in times:
        old_date, old_time = time.text.split('T')
        time.text = new_date+"T"+old_time
        if verbose==True:
            print("Found date:%s replaced by:%s"%(old_date, new_date))

    return tree



if __name__ == "__main__":


    input_file = "to_work.gpx"
    output_file = "to_work_out.gpx"

    ns = "http://www.topografix.com/GPX/1/1"

    tree = et.parse(input_file)

    root = tree.getroot()

    #print et.tostring(root, pretty_print=True)

    children = root.getchildren()

    #for child in children:
    #    print et.tostring(child, pretty_print=True)

    trk_tag = str(QName(ns, "trk"))
    for track in root.getiterator(trk_tag):
        print("got one track")
        print track.tag
        print et.tostring(track, pretty_print=True)



    tree = replace_date(tree, date.today(), False)

    """

    #print root.nsmap
    #print root

    #print root.attrib
    #print root.attrib.get('xmlns')
    """

    tree.write(output_file, xml_declaration=True, encoding='utf-8')

