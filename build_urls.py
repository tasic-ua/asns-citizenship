#!/usr/bin/python3

'''
The script in interactive mode builds URLs to make requests for conversation 
addresses to longitude/latitude. It shows the current address for each ASN 
taken from the input file and proposes to agree with it or enter a changed
address. Then it requests a country of org (enter to skip the country field).

Arguments:
    addresses<current_date>-<current_time>.json -- filename

In the output JSON file are the next fields
    AS number
    RL address
    URL to make a request (without key)
'''

import sys
import json

def build_urls(f_name):
    '''
    Prepares URLs to make requests
    Parameters
    --------------
    f_name : str
        A filename of JSON data with RL addresses
    '''
    with open(sys.argv[1]) as f:
        x = f.read()
    jsn = json.loads(x)

    result = []
    url = "https://api.maptiler.com/geocoding/"
    trans = {'\n':'%20',' ':'%20', ',':'%2C','/':'%2F'}
    mytable = str.maketrans(trans)

    for i in jsn:
        if len(i)<7:
            print(f"There is no adr in {i[0]}",file=sys.stderr)
            continue;
        print(i[0],"\n")
        print(i[6]["adr"],"\n")
        addr = input("Enter address to search [press Enter to keep this address]: ")
        if addr == "":
            addr = i[6]["adr"]
        sx = addr.translate(mytable)
        cntry = str(input("Enter two-letters country for search [Enter to skip"+
                " adding a country]: ")).rstrip().casefold()
        sec = url+sx+".json?"
        if cntry != "":
            sec += "country="+cntry+"&"
        sec += "autocomplete=false&fuzzyMatch=true&limit=3&key="
        result.append([i[0], i[6]["adr"], sec])

    res = json.dumps(result)
    with open("request-urls.json","w") as f:
        f.write(res)

if __name__ == '__main__':
# The argument must be file addresses...
    if len(sys.argv) < 2:
        quit("Missing data filename")

    build_urls(sys.argv[1])
