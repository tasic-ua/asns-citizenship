# asns-citizenship
A set of scripts to get info from RIPE DB about changes in ASN's citizenships and draw these ASNs on a map.

This is a collection of scripts to work with the country attributes of ASNs from the RIPE NCC site. I give a way that I used them one by one and then shortly
describe every script. Feel free to contact the author if you have questions or suggestions.

## Step-by-step to the result

I had to find ASNs that changed their country code from RU to UA during the war and place them on the map according to the data from RIPE DB. Of course, my work was caused by the strange behavior of some resources, but you can use these scripts for another purpose with other country codes. Let's start...

I selected two dates to check the changes from the first date to the second. Let's name them &lt;date1&gt; and &lt;date2&gt;.

From the _https://ftp.ripe.net/pub/stats/ripencc/_ I took files _delegated-ripencc-&lt;date1&gt;_ and _delegated-repencc-&lt;date2&gt;_

With **split_file.py** I split these files on ASN, IPv4, and IPv6 parts and got 6 files. Really for further research, I used only _ansn-&lt;date1&gt;_ and 
_asns-&lt;date2&gt;_. But files with IP addresses also can be compared by one of the scripts.

With **asns_check.py** I take two files with ASNs prepared by split_file.py, define "from the country", and "to the country" and get the file with dates, citizenship, and current org hanles.

There is a complication in this step. RIPE NCC changed the way they set the country attribute in ASN info according to [NWI-10](https://labs.ripe.net/author/wilhelm/impact-of-nwi-10-on-country-codes-in-delegated-statistics/). They did the changes in two steps and the second step they did on November 10, 2022. So to get clearer results I had to exclude ASNs changed on this date. So I took files with statistics on November 29, and December 1 and excluded from my list ASNs that were changed on this date. asns_check.py accepts as an option "exclude file" where you can point ASNs to exclude from the result.

With **get_address.py** I receive RL contact data from org handles (name, address, phone number, and email) by requests to _http://rdap.db.ripe.net/entity/_

This is the most complicated and weak part of the set. I had to find latitude and longitude by the address from the org handle. First of all as far as I could find to use the Google API for this purpose you have to be its client and have a Google Cloud Project. I didn't have one so I looked for another conversion service. As a result, I came to maptiler.com. Although it makes this kind of conversion a little bit worse than Google. You have to register there and get the key you will use in every request. There is a limit of requests but it is bigger than needed to make conversion for this task.

So we need to prepare the URLs to make conversation requests. I used **build_urls.py** for this purpose. The script is interactive. It shows you the address you can edit and reenter and then requests the country. It is caused by assigning occupied territories of Ukraine to ru. Therefore the conversation engine works very poorly in such circumstances. So sometimes adding a separate field "country" to request can improve the result. It prepares file _request-urls.json_ with URLs to use in requests.

The next step is making requests to _https://api.maptiler.com/geocoding/_ to receive the coordinates of each address. First of all, you have to get the key for access to conversion. You can do it here _https://cloud.maptiler.com/account/keys/_. You have to register there (or authenticate by Google account) to get the key. Then with **get_geo_for_asns.py** I make requests to the prepared by build_urls.py URLs adding the key. The script can be used interactively when it shows an address, and the corresponding URL and asks questions. Or the -q option may be given and then it silently gets all data. Just printing dots to show that it is alive -- getting this information can take a bit of time. The script prints the result to AS<number>-location.json files. Every response _can_ contain a few variants of an answer so the following processing is needed. The response also can miss the coordinates. If the response contains more than one response every response has weight (relevance). The highest weight showed the best relevance but it does not guarantee the right place. If you miss coordinates in the AS<number>-location.json file you have to work with the source RL (real life) address. Try to give "maptiles" a better description of the address. Or try to convert this address with another resource. 

We are still moving through the complicated part of the set. With **for_map.py** I prepare the data to place points on a map. The data is prepared in plain text to allow easy editing. It prints output data to stdout and errors to stderr, so you can redirect ready data end errors to different files and handle them separately.

The last step of my journey is placing marks on a map. With **draw_points.py** I place marks on a map. When you take some part of a map to an image file you have only "an image". To convert this image to a map you have to bind image pixels to longitude/latitude. There are different tools to make it or you can make it yourself with the help of Google and an editor that gives you point coordinates. But at last, you need a file with image point coordinates and appropriate longitude/latitude. A file like this
```
XY,1,0,0
XY,2,1167,0
XY,3,1167,780
XY,4,0,780
LL,1,  30.329430,  49.075565
LL,2,  40.622950,  49.116228
LL,3,  40.672959,  44.485199
LL,4,  30.379439,  44.444536
```
As you can see the first four lines are the coordinates of an image pixels and the second four lines are corresponding longitude/latitude coordinates. The script works with images in PNG format. And the script needs an image of the mark to place on a map. It places the mark sign the way that in the given coordinates is a bottom-center point of the mark image. When you have all of these you can place the marks on a map. There is a directory with example files to see how it works.

## Script descriptions

+ **asns_check.py** -- Compares two files with ASNs received as the output of split_file.py about ASNs that
    changed their "citizenship" from one country to another. During execution
    requests "from" and "to" countries in two-letter ISO format (UA, RU, US, DE, PL,
    etc).
  
    Arguments:
    - asns-20220223 -- first file with ASNs list (output of split_file.py)
    - asns-20231101 -- second file with ASNs list (output of split_file.py)
    - exclude.txt -- text file with ASNs list that must be excluded from comparison, one AS number per line. Optional parameter

    After comparison makes requests to stat.ripe.net and receives the current ORG nick handle of each found ASN.

    Out file named result-<current_date>-<current_time>.json puts in the current directory. An output file contains data:
    - AS number
    - first date
    - from country
    - second date
    - to country
    - current org handle
  
+ **build_urls.py** -- The script in interactive mode builds URLs to make requests for conversation addresses to longitude/latitude. It shows the current address for each ASN taken from the input file and proposes to agree with it or enter a changed address. Then it requests a country of org (enter to skip the country field).

    Arguments:
    - addresses<current_date>-<current_time>.json -- filename

    In the output JSON file are the next fields
    - AS number
    - RL address
    - URL to make a request (without key)
  
+ **draw_points.py** -- This script can place points on a map. To get the result you have to have:
    - image file with map (PNG file);
    - text file provided binding image map to geo coordinates;
    - text file with ASNs and coordinates to place marks on a map;
    - PNG image with mark to place on the image map;
      
    To use an image as a map you have to bind a map on the image to the real longitude latitude. There are different tools on the Internet to do this. Or you may do it yourself with help of the Google and any image editor that can tell you the point position on an image. So you have to make a file like this
```
    XY,1,0,0
    XY,2,1167,0
    XY,3,1167,780
    XY,4,0,780
    LL,1,  30.329430,  49.075565
    LL,2,  40.622950,  49.116228
    LL,3,  40.672959,  44.485199
    LL,4,  30.379439,  44.444536
```
The first four points are the x and y coordinates of the corners of the image, second four points are the longitude/latitude coordinates on the map. So for example you have the image of the map in a file map_image.png (the script expects that it is PNG) then binding information in the above-described format you have to put in the text file map_image.borders

These files (png and borders) must be in the directory where you ran the script. Also, you need a file with AS numbers and corresponding LL coordinates (output of for_map.py, f.e. my_points.txt)

And you need an image of a mark that you are going to place on the map. You may name it mark.png and place it in the current directory or point to it after the -m flag when you run the script.

So in this example, you run the script with the command:
```
draw_points.py -b map_image -p my_points.txt -m mark.png
```
+ **for_map.py** -- The script takes ASNs from the file addresses<date>-<time>.json file (should be an argument to the script, and asn by asn takes most relevant coordinates from files AS<number>location.json. Option -p path has to point to the directory where the files are located. If a path is not specified the script expects files in the current directory. The script prints prepared data to stdout, and error messages to stderr.
  
    Possible errors are:
    - there are no coordinates in the AS<number>-location.json file
    - there is no appropriate AS<number>-location.json

    If you redirect script output to the file you get the prepared data in the file and a list of errors on the screen. If there are no coordinates in the JSON file it means that maptiles did not find any coordinates by the given address. You have to handle this situation in some way.

    If there is no JSON file it means that for some reason you miss to prepare this ASN for request to maptiler.

    Maptiler can return more than one pair of coordinates. It attributes every pair to a relevance level. The first pair has the highest relevance. So the program takes the first pair of coordinates from AS<number>-location.json file. I did not have a case when the less relevance points to the right location. But you can check...

    The output of this script (and the corresponding input of the script to place points on a map) is used with plain text data to allow easy editing of the prepared data.
  
+ **get_address.py**
+ **get_geo_for_asns.py**
+ **print_result.py**
+ **split_file.py**
