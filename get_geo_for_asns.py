#!/usr/bin/python3

'''
This script gets prepared URLs from an input file, add key to url and makes
request to https://api.maptiler.com/geocoding/ converting RL address into
latitude/longitude. Ressult of every request outputs to separate file with name
AS<number>-location.json
Usage:
    get_geo_for_asns.py [-q] [-k key] filename
        -q - be quiet, do not ask approve for every request
        -k key - key identificator to maptiler
        filename - file with prepared URLs
'''

import sys
import json
import requests

def get_geodata(f_name,key,quiet):
    '''
    Makes requests to https://api.maptiler.com/geocoding/ converting RL address
    into latitude/longitude.
    Parameters:
    ---------------
    f_name : str
        file with prepared URLs
    key : str
        key identificator to maptiler
    quiet : boolean
        be quiet, do everithin automatically
    '''
    with open(f_name) as f:
        x = f.read()

    jsn = json.loads(x)

    for i in jsn:
        url = i[2]+key
        if not quiet:
            print("AS:",i[0])
            print("Address:",i[1])
            print("URL:",url)
            yn = input("Make request [y/N/q]? ").rstrip()
        else:
            print(".",end='',flush=True)
            yn = 'y'
        if yn.casefold() == 'y':
            data = requests.get(url)
            if int(data.status_code) != 200:
                print("Response code:",data.status_code,file=sys.stderr)
            f_txt = "AS"+str(i[0])+"-location.json"
            with open(f_txt,"w") as f:
                f.write(data.text)
        elif yn.casefold() == 'q':
            break

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print(f'{sys.argv[0]} [-k key] [-q] filename')
        print("\tfilename - file with prepared URLs to request coordinates")
        print("\tkey - key id to make requests")
        print("\t-q - be quiet, just make all requests witout asking approval")
        quit()

    quiet = False
    i = 1
    f_name = None
    key = None
    while i < len(sys.argv):
        if sys.argv[i][:2] == "-q":
            quiet = True
            i += 1
            continue
        elif sys.argv[i][:2] == "-k":
            if len(sys.argv[i]) > 2:
                key = sys.argv[i][2:]
            else:
                i += 1
                key = sys.argv[i]
                i += 1
                continue
        else:
            f_name = sys.argv[i]
            i += 1

    if f_name == None:
        f_name = str(input("Enter filename: ")).rstrip()

    if key == None:
        key = str(input("Enter key: ")).rstrip()

    get_geodata(f_name,key,quiet)

