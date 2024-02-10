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

With **asns_check.py** I take two files with ASNs prepared by split_file.py, define "from the country", and "to the country" and get the file with dates, citizenship, and current org hanles.

_Here must be description of NWI-10, getting list to exclustion and the result._

With **get_address.py** I receive RL contact data from org handles (name, address, phone number, and email) by requests to _http://rdap.db.ripe.net/entity/_

This is the most complicated and weak part of the set. I had to find latitude and longitude by the address from the org handle. First of all as far as I could find to use the Google API for this purpose you have to be its client and have a Google Cloud Project. I didn't have one so I looked for another conversion service. As a result, I came to maptiler.com. Although it makes this kind of conversion a little bit worse than Google. You have to register there and get the key you will use in every request. There is a limit of requests but it is bigger than needed to make conversion for this task.

So we need to prepare the URLs to make conversation requests. I used **build_urls.py** for this purpose. The script is interactive. It shows you the address you can edit and reenter and then requests the country. It is caused by assigning occupied territories of Ukraine to ru. Therefore the conversation engine works very poorly in such circumstances. So sometimes adding a separate field "country" to request can improve the result. It prepares file _request-urls.json_ with URLs to use in requests.

The next step is making requests to _https://api.maptiler.com/geocoding/_ to receive the coordinates of each address. First of all, you have to get the key for access to conversion. You can do it here _https://cloud.maptiler.com/account/keys/_. You have to register there (or just authenticate by Google account) to get the key. Then with **get_geo_for_asns.py** I make requests to the prepared by build_urls.py URLs adding the key. The script can be used interactively when it shows an address, and the corresponding URL and asks questions. Or the -q option may be given and then it silently gets all data. Just printing dots to show that it is alive -- getting this information can take a bit of time. The script prints the result to AS<number>-location.json files. Every response _can_ contain a few variants of an answer so the following processing is needed. The response also can miss the coordinates. If the response contains more than one response every response has weight (relevance). The highest weight showed the best relevance but it does not guarantee the right place. If you miss coordinates in the AS<number>-location.json file you have to work with the source RL (real life) address. Try to give "maptiles" a better description of the address. Or try to convert this address with another resource. 

We are still moving through the complicated part of the set. With **for_map.py** I prepare the data to place points on a map. The data is prepared in plain text to allow easy editing. It prints output data to stdout and errors to stderr, so you can redirect ready data end errors to different files and handle the errors separately.
