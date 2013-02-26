#!   /usr/bin/env   python
#    coding: utf8

# Copyright CERN, 2013
# Author: Matthieu Cattin <matthieu.cattin@cern.ch>
# Licence: GPL v2 or later.


import sys
from datetime import date, timedelta
import xml.etree.ElementTree as et

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
    root.append(track)

def rename_track(root, track, name, verbose=False):
    trk_name = track.findall("./{http://www.topografix.com/GPX/1/1}name")
    trk_text = track.findall(".//{http://www.topografix.com/GPX/1/1}text")
    if verbose==True:
        print("Track name, old: %s, new: %s"%(trk_name[0].text, name))
    trk_name[0].text = name
    trk_text[0].text = name


if __name__ == "__main__":


    input_file = "to_work.gpx"
    output_file = "to_work_out.gpx"

    ns = "http://www.topografix.com/GPX/1/1"
    day = date.today()


    tree = et.parse(input_file)
    et.register_namespace('', ns)
    root = tree.getroot()

    trk_tag = str(et.QName(ns, "trk"))

    # get tracks
    tracks, nb_tracks = get_tracks(root, True)

    # input file must have only 1 track
    if nb_tracks == 1:
        # copy track to have the way back from work
        add_track(root, tracks[0])
    else:
        print("Input file MUST have only one track! Your file has %d tracks."%nb_tracks)
        sys.exit()

    # FOR TEST
    tracks, nb_tracks = get_tracks(root, True)

    # save changes
    tree.write(output_file, xml_declaration=True, encoding='utf-8')
    tree = et.parse(output_file)
    root = tree.getroot()

    # rename the "way back from work" track in ffrom_work
    tracks, nb_tracks = get_tracks(root, True)
    rename_track(root, tracks[-1], "from_work", True)

    # replace the date on the two tracks (to_work and from_work)
    replace_track_date(tracks[0], day)
    replace_track_date(tracks[1], day)

    # save changes
    tree.write(output_file, xml_declaration=True, encoding='utf-8')
    tree = et.parse(output_file)
    root = tree.getroot()

    # if more than one day, copy the two tracks
    tracks, nb_tracks = get_tracks(root, True)
    add_track(root, tracks[0])
    add_track(root, tracks[1])

    # save changes
    tree.write(output_file, xml_declaration=True, encoding='utf-8')
    tree = et.parse(output_file)
    root = tree.getroot()

    # FOR TEST
    day = day + timedelta(days=1)

    # replace the date on the copied tracks
    tracks, nb_tracks = get_tracks(root, True)
    replace_track_date(tracks[-2], day)
    replace_track_date(tracks[-1], day)


    """
    for track in root.getiterator(trk_tag):
        track = replace_date(track, day , False)
        day = day + timedelta(days=1)
    """
    """
    #print root.nsmap
    #print root

    children = root.getchildren()
    for child in children:
        print et.tostring(child, pretty_print=True)

    #print root.attrib
    #print root.attrib.get('xmlns')
    """

    print et.tostring(root)

    tree.write(output_file, xml_declaration=True, encoding='utf-8')

