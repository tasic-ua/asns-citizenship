# asns-citizenship
A set of scripts to get info from RIPE DB about changes in ASN's citizenships and draw
these ASNs on a map.

This is a collection of scripts to work with the country attributes of ASNs from the
RIPE NCC site. I give a way that I used them one by one and then shortly
describe every script. Feel free to contact the author if you have questions or
suggestions.

## Work step-by-step

I had to find ASNs that changed their country code from RU to UA during the war
and place them on the map according to the data from RIPE DB. Of course, my work
was caused by the strange behavior of some resources, but you can use these scripts
for another purpose with other country codes. Let's start...

I selected two dates to check the changes from the first date to the second. Let's name
them <date1> and <date2>.

From the https://ftp.ripe.net/pub/stats/ripencc/ I took files
delegated-ripencc-<date1> and delegated-repencc-<date2>

With split_file.py I split these files on ASN, IPv4, and IPv6 parts and got 6
files. Really for further research, I needed only ansn-<date1> and asns-<date2>

With asns_check.py I take two files with ASNs prepared by split_file, define
"from the country", "to the country" and get the file with dates, citizenship and
current org hanles.

With get_address.py I receive RL contact data from org handles (name, address,
phone number, and email)
