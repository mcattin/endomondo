#!   /usr/bin/env   python
#    coding: utf8

# Copyright CERN, 2013
# Author: Matthieu Cattin <matthieu.cattin@cern.ch>
# Licence: GPL v2 or later.


import sys
from datetime import *
import xml.etree.ElementTree as et


def replace_track_date(track, new_date, verbose=False):
    # Search for all "time" tags
    times = track.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time")
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
    tracks = root.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Track")
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


if __name__ == "__main__":


    input_file = "to_work.tcx"
    input_file_2 = "from_work.tcx"
    output_file = "to_work_out.tcx"

    start_date = datetime.strptime("2013-02-04", "%Y-%m-%d")
    end_date   = datetime.strptime("2013-02-12", "%Y-%m-%d")
    start_date = start_date.date()
    end_date = end_date.date()

    #ns = "http://www.topografix.com/GPX/1/1"
    ns = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"

    tree = et.parse(input_file)
    #tree_2 = et.parse(input_file_2)
    et.register_namespace('', ns)
    root = tree.getroot()
    #root_2 = tree_2.getroot()

    print et.tostring(root)

    #trk_tag = str(et.QName(ns, "trk"))

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

    # rename the "way back from work" track in from_work
    tracks, nb_tracks = get_tracks(root, True)
    #rename_track(root, tracks[-1], "from_work", True)

    # FOR TEST
    day = start_date
    print day

    # replace the date on the two tracks (to_work and from_work)
    replace_track_date(tracks[0], day)
    replace_track_date(tracks[1], day)

    # if more than one day, copy the two tracks
    if end_date != start_date:
        while day < end_date:
            day = day + timedelta(days=1)

            print day, day.weekday()

            if day.weekday() > 4:
                print("It's weekend")
                continue

            tracks, nb_tracks = get_tracks(root, True)
            add_track(root, tracks[0])
            add_track(root, tracks[1])

            # replace the date on the copied tracks
            tracks, nb_tracks = get_tracks(root, True)
            replace_track_date(tracks[-2], day)
            replace_track_date(tracks[-1], day)


    """
    #print root.nsmap
    #print root

    children = root.getchildren()
    for child in children:
        print et.tostring(child, pretty_print=True)

    #print root.attrib
    #print root.attrib.get('xmlns')
    """

    # FOR TEST
    print et.tostring(root)

    # save to output file
    tree.write(output_file, xml_declaration=True, encoding='utf-8')

