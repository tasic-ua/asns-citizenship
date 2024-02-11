#!/usr/bin/python3

'''
The script takes ASNs from the file addresses<date>-<time>.json file (should be
an argument to the script, and asn by asn takes most relevant coordinates from
files AS<number>location.json. Option -p path has to point to the directory
where the files are located. If a path is not specified the script expects files
in the current directory. The script prints prepared data to stdout, and error
messages to stderr.

Possible errors are:
    - there are no coordinates in the AS<number>-location.json file
    - there is no appropriate AS<number>-location.json

If you redirect script output to the file you get the prepared data in the file
and a list of errors on the screen. If there are no coordinates in the JSON file
it means that maptiles did not find any coordinates by the given address. You
have to handle this situation in some way.

If there is no JSON file it means that for some reason you miss to prepare this
ASN for a request to maptiler.

Maptiler can return more than one pair of coordinates. It attributes every pair
to a relevance level. The first pair has the highest relevance. So the program
takes the first pair of coordinates from AS<number>-location.json file. I did
not have a case when the less relevance points to the right location. But you
can check...

The output of this script (and the corresponding input of the script to place
points on a map) is used with plain text data to allow easy editing of the
prepared data.
'''

import json
import os
import sys

def prepare_coords(f_name, path=""):
    '''
    Function to prepare data for locating pointers on the map.
    Parameters:
    --------------
    f_name : str
        filename of json data with the ASNs list
    path : str
        path to directory with AS<number>-location.json files
    '''
    with open(f_name) as f:
        x = f.read()

    jsn = json.loads(x)

    empty = []
    for asn in jsn:
        as_f_name = path+"/AS"+str(asn[0])+"-location.json"
        try:
            with open(as_f_name) as f:
                x = f.read()
        except:
            print(f'Missing filename for AS{asn[0]}',file=sys.stderr)
            continue
        loc_info = json.loads(x)
        try:
            print(asn[0],loc_info["features"][0]["geometry"]["coordinates"][1],loc_info["features"][0]["geometry"]["coordinates"][0])
        except:
            empty.append((asn[0],asn[1]))

    if len(empty) > 0:
        print("ASes without coordinate", file=sys.stderr)
        for i in empty:
            print(i[0],"\n",i[1],"\n\n", file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Usage:")
        print("----------")
        print(f'{sys.argv[0]} [-p path] <filename>')
        print("\tpath -- path to catalog with AS*-location.json files")
        quit()
    i=1
    path = ""
    f_name = ""
    while i<len(sys.argv):
        if sys.argv[i][:2] == '-p':
            if len(sys.argv[i]) > 2:
                path = sys.argv[i][2:]
            else:
                i += 1
                path = sys.argv[i]
        else:
            f_name = sys.argv[i]
        i += 1
    if len(f_name) == 0:
        quit("Missing mandatory filename.")

    prepare_coords(f_name, path)
