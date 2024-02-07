#!/usr/bin/python3
'''
Compares two files with ASNs received as output of split_file.py about ASNs that
changed their "citizenship" from one country to another. During execution
requests "from" and "to" countries in two-letters ISO format (UA,RU,US,DE,PL,
etc).
Arguments:
    asns-20220223 -- first file with ASNs list (output of split_file.py)
    asns-20231101 -- second file with ASNs list (output of split_file.py)
    exclude.txt -- text file with ASNs list that must be excluded from
    comparision, one AS number per line. Optional parameter

After comparision makes requests to stat.ripe.net and receives current ORG nick
handle of each found ASN.

Out file named result-<current_date>-<current_time>.json puts in the current
directory. Output file contains data:
    AS number
    first date
    from country
    second date
    to country
    current org handle
'''

import sys
import requests
import datetime
import json

def compare_asn_lists(f_file, s_file, f_country, s_country, exclude=None):
    '''
    Get two filenames, two countries and optional exclude list and finds the
    ASNs that changed "citizenship"

    Parameters
    -----------------------
        f_file : str
            The name of file with data at the start date of the period
        s_file : str
            The name of file with data at the end date of the period
        f_country : str
            Two-letters ISO name of "from country"
        s_country : str
            Two-letters ISO name of "to country"
        exclude : str,optional
            The filename with list (one in a string) of ASNs to exclude from
            comparision

    '''
    # Make dates for output
    f_date = f_file[-2:] + '.' + f_file[-4:-2] + '.' + f_file[-8:-4]
    s_date = s_file[-2:] + '.' + s_file[-4:-2] + '.' + s_file[-8:-4]
    dt = datetime.datetime.now()
    out_file = "result-" + dt.strftime("%y%m%d-%H%M") + ".json"

    # Read data in the lists
    with open(f_file,'r') as f:
        F_List = f.readlines()
    with open(s_file,'r') as f:
        S_List = f.readlines()

    f_ind = F_List[-1].split('|')
    a = int(f_ind[3])+1
    s_ind = S_List[-1].split('|')
    b = int(s_ind[3])+1

    m_ind = max(a,b)
    fList = [None for x in range(m_ind)]
    sList = [None for x in range(m_ind)]

    for i in F_List:
        lst = i.split('|')
        ind = int(lst[3])
        fList[ind]=lst[1].strip()

    for i in S_List:
        lst = i.split('|')
        ind = int(lst[3])
        sList[ind]=lst[1].strip()

# We made two lists with ASN as index and country name as a value.
# If ASN isn't in file there is None instead of country name

    as_list = []
    for i in range(m_ind):
        if i in exclude: continue
        if fList[i] == f_country and sList[i] == s_country:
                as_list.append([i,f_date,fList[i],s_date,sList[i]])

# Request to stat.ripe.net about current ORG field of ASN
# If there is no org field write None
    url_req = 'https://stat.ripe.net/data/whois/data.json?resource='
    for i in as_list:
        print(".",end='',flush=True)
        l_url = url_req + "AS" + str(i[0])
        x = requests.get(l_url)
        jsn = json.loads(x.text)
        try:
            i.append(next(item['value'] for item in jsn['data']['records'][0] if item['key'] == 'org'))
        except:
            i.append(None)

    print("\n")
# Output results of requests to file result-<datetime> in JSON format
    result = json.dumps(as_list)
    with open(out_file,"w") as f:
        f.write(result)

if __name__ == '__main__':
# Input data from files

    if len(sys.argv) < 3:
        # File names were not in command line
        f_file = input("Input first file name:")
        s_file = input("Input second file name:")
    else:
        # Take the filenames from command line
        f_file =sys.argv[1]
        s_file =sys.argv[2]

    exclude = []
    if(len(sys.argv) > 3):
        with open(sys.argv[3],'r') as f:
            exLst = f.readlines()
            exclude = [int(i.strip()) for i in exLst]

    print("We are looking for ASNs that changed their country attribute.")
    print("You have to enter contry code in two-letter form for the both countries.")
    f_country = input("Enter country code for the first country (from) [UA]: ")
    f_country.rstrip().capitalize()
    if len(f_country) < 2: f_country="UA"
    s_country = input("Enter country code for the second country (to) [RU]: ")
    s_country.rstrip().capitalize()
    if len(s_country) < 2: s_country="RU"

    compare_asn_lists(f_file, s_file, f_country, s_country, exclude)
