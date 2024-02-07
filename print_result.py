#!/usr/bin/python3

'''
Takes the output filename of get_address.py execution in JSON format and prints
AS number
date country
date country
in human readable format
'''
import json
import sys

def print_result(f_name):
    '''
    Prints JSON from get_address.py in human readable format.

    Parameters
    -----------------------
        f_name : str
            The name of file with data
    '''
    f = open(f_name,"r")
    x = f.read()
    f.close

    jsn = json.loads(x)
    for i in jsn:
        print("AS"+str(i[0]))
        print(i[1],i[2])
        print(i[3],i[4])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        quit("Missing filename")

    print_result(sys.argv[1])
