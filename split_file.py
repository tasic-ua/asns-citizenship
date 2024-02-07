#!/usr/bin/python3

'''
The program splits a file delegated-ripencc-<date> taken from
https://ftp.ripe.net/pub/stats/ripencc/ into three parts with ASNs, IPv4,
and IPv6 records. Output files are placed in the current directory.

Example:
    split_file.py delegated-ripencc-20220223

if you did not give filename as argument it asks you to enter filename.

Output:
    asns-20220223
    ipv4--20220223
    ipv6-20220223
files in the current directory
Files contain ASNs, IPv4, and IPv6 records from RIPE DB respectively.
'''

import sys

def split_file(f_name):
    '''
    Gets filename and splits the file to three parts.

    Parameters
    -----------------------
        f_name : str
            The name of file from stat.ripe.net to split
    '''
    l = f_name.split('-')

    asn_f_name = 'asns-' + l[-1]
    ipv4_f_name = 'ipv4-' + l[-1]
    ipv6_f_name = 'ipv6-'+l[-1]

    with open(f_name,'r') as f:
        total = f.readlines()

    f_asn = open(asn_f_name,'w')
    f_ipv4 = open(ipv4_f_name,'w')
    f_ipv6 = open(ipv6_f_name,'w')

    for i in total:
        j = i.split('|')
        if len(j[1]) != 2:
            continue
        if j[2] == 'ipv4':
            f_ipv4.write(i)
        elif j[2] == 'asn':
            f_asn.write(i)
        elif j[2] == 'ipv6':
            f_ipv6.write(i)

    f_asn.close()
    f_ipv4.close()
    f_ipv6.close()

if __name__ == '__main__':
# If you did not give filename as argument it asks you to enter the filename

    if len(sys.argv) > 1:
        f_name = sys.argv[1]
    else:
        f_name = input("Input file name to split:")

    split_file(f_name)
