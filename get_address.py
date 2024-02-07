#!/usr/bin/python3

'''
The script takes as argument the filename of the file prepared by asns_check.py
collects information from RIPE DB (LIR name, address, phone, email address) and
saves output in json format to file addresses-<cur_date>-<cur_time>.json in
current directory.
Arguments:
    result-<current_date>-<current_time>.json -- filename

In output json file keeps the data from the input file
    AS number
    first date
    from country
    second date
    to country
    current org handle
and add to it available from list "name, address, phone, email" fields from org
handle.
'''
import requests
import json
import sys
import datetime

# The script takes file prepared by asns_check.py and add information taken from
# whois about LIR name, address, phone, and email address

# Output data is saved in file addresses-*.json in JSON format

def get_address(f_name):
    '''
    Gets filename with json data prepared by asns_check.py (see output format
    there), makes requests to RIPE DB and output data in json format to result
    file.

    Parameters
    -----------------------
        f_name : str
            The name of file with data
    '''
    with open(f_name,"r") as f:
        x = f.read()

    as_loaded = json.loads(x)

    prefix = 'http://rdap.db.ripe.net/entity/'

    for i in as_loaded:
        print('.',end='',file=sys.stderr,flush=True)
        if i[5] == None: continue
        url = prefix + i[5]
        x = requests.get(url)
        jsn = json.loads(x.text)
        vcard = {}
        for k in jsn["vcardArray"][1]:
            if k[0] == 'adr':
                vcard["adr"] = k[1]["label"]
            elif k[0] == 'fn':
                vcard["name"] = k[3]
            elif k[0] == 'tel':
                vcard['phone'] = k[3]
            elif k[0] == 'email':
                vcard['email'] = k[3]
        i.append(vcard)

    print("\n",file=sys.stderr)
    result = json.dumps(as_loaded)
    dt = datetime.datetime.now()
    out_file = "addresses" + dt.strftime("%y%m%d-%H%M") + ".json"

    with open(out_file,"w") as f:
        f.write(result)

    for i in as_loaded:
        if len(i)<7 and i[5] != None:
            print(f"For {i[5]} i[6] isn't defined", file=sys.stderr)
#        try:
#            print(i[5],"\n",i[6],"\n")
#        except:
#            print("i[6] isn't defined")

if __name__ == '__main__':

    if len(sys.argv) < 1:
        f_name = input("Data filename:")
    else:
        f_name = sys.argv[1]

    get_address(f_name)
#print(x.text)

#jsn = json.loads(x)
#for i in jsn["vcardArray"][1]:
#    if i[0] == 'adr':
#        print(i[1]["label"])

#print("\n")
#print(len(jsn["data"]["records"][0]))
#for d in jsn["data"]["records"][0]:
#    if d["key"] == "org":
#        print(d["value"])
