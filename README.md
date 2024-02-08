# asns-citizenship
A set of scripts to get info from RIPE DB about changes in ASN's citizenships and draw these ASNs on a map.

This is a collection of scripts to work with the country attributes of ASNs from the RIPE NCC site. I give a way that I used them one by one and then shortly
describe every script. Feel free to contact the author if you have questions or suggestions.

## Work step-by-step

I had to find ASNs that changed their country code from RU to UA during the war and place them on the map according to the data from RIPE DB. Of course, my work was caused by the strange behavior of some resources, but you can use these scripts for another purpose with other country codes. Let's start...

I selected two dates to check the changes from the first date to the second. Let's name them &lt;date1&gt; and &lt;date2&gt;.

From the _https://ftp.ripe.net/pub/stats/ripencc/_ I took files _delegated-ripencc-&lt;date1&gt;_ and _delegated-repencc-&lt;date2&gt;_

With **split_file.py** I split these files on ASN, IPv4, and IPv6 parts and got 6 files. Really for further research, I used only _ansn-&lt;date1&gt;_ and 
_asns-&lt;date2&gt;_. But files with IP addresses also can be compared by one of the scripts.

With **asns_check.py** I take two files with ASNs prepared by split_file.py, define "from the country", and "to the country" and get the file with dates, citizenship and current org hanles.

_Here must be description of NWI-10, getting list to exclustion and the result._

With **get_address.py** I receive RL contact data from org handles (name, address, phone number, and email) by requests to _http://rdap.db.ripe.net/entity/_

This is the most complicated and weak part of the set. I had to find latitude and longitude by the address from the org handle. First of all as far as I could find to use the Google API for this purpose you have to be its client and have a Google Cloud Project. I didn't have one so I looked for another conversion service. As a result, I came to maptiler.com. It makes this kind of conversion although a little bit worse than Google. To use it you have to register there and get the key that you will use in every request. There is a limit of requests but it is bigger than needed to make conversion for this task.
