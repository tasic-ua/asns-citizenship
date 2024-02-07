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

From the _https://ftp.ripe.net/pub/stats/ripencc/_ I took files
_delegated-ripencc-<date1>_ and _delegated-repencc-<date2>_

With **split_file.py** I split these files on ASN, IPv4, and IPv6 parts and got 6
files. Really for further research, I used only _ansn-<date1>_ and _asns-<date2>_.
But files with IP addresses also can be compared by one of the scripts.

With **asns_check.py** I take two files with ASNs prepared by split_file.py, define
"from the country", and "to the country" and get the file with dates, citizenship and
current org hanles.

With **get_address.py** I receive RL contact data from org handles (name, address,
phone number, and email) by requests to _http://rdap.db.ripe.net/entity/_
