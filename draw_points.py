#!/usr/bin/python3

'''
This script can place points on a map. To get the result you have to have:
    - image file with map (png file);
    - text file provided binding image map to geo coordinates;
    - text file with ASNs and coordinates to place marks on map;
    - png image with mark to place on the image map;
To use some image as a map you have to bind a map on the image to the real
longitude latitude. There are different tools on the Internet to make this. Or
you may do it youself with help of the google and any image editor which can
tell you the point position on an image. So you have to make file like this

XY,1,0,0
XY,2,1167,0
XY,3,1167,780
XY,4,0,780
LL,1,  30.329430,  49.075565
LL,2,  40.622950,  49.116228
LL,3,  40.672959,  44.485199
LL,4,  30.379439,  44.444536

First for point is x and y coordinates of cornters of the image, second for
points is they longitude/latitude coordinates on the map. So for example you
have the image of the map in a file
map_image.png (the script expects that it is PNG)
then binding information in the above described format you have to put in text
file 
map_image.borders

These files (png and borders) must be in the directory where you ran the script.
Also you need file with AS numbers and corresponding LL coordinates (output of
for_map.py, f.e. my_points.txt)

And you need image of a mark that you are going to place on the map. You may
name it mark.png and place it in the current directory or point to it after -m
flag when you run the script.

So in this examples you run the script with the command:

draw_points.py -b map_image -p my_points.txt -m mark.png 

'''

import sys
from PIL import Image, ImageDraw, ImageFont


def draw_points(base, in_file, mark_file):
    '''
    Places marker on a map according to the given coordinates.

    Parameters
    -----------------------
        base : str
            basename (without extension) of image map and points that bind image
            to longitude/latitude. Also output file name is based on this name
        in_file : str
            filename with AS numbers an corresponding coordinates
        mark_filw : str
            filename with mark image to place on a map
    '''
    f_bord = base+".borders"

    with open(f_bord) as f:
        coord = f.readlines()

    # to work with indexes from input file (1-4) we make empty 0 element
    xy = [('','')]
    ll = [('','')]

    for k in coord:
        j = k.split(',')
        i = [im.strip() for im in j]
        if i[0] == "XY":
            xy.insert(int(i[1]),(float(i[2]),float(i[3])))
        elif i[0] == "LL":
            ll.insert(int(i[1]),(float(i[2]),float(i[3])))

    with open(in_file) as f:
        points = f.readlines()

    f_inp = base+".png"
    f_out = base+"_result.png"

    # Preparing image file
    img = Image.open(f_inp)
    im = Image.open(mark_file)
    Merged_img = Image.new("RGBA", img.size)
    Merged_img.paste(img, (0, 0))
    _, _, _, mask = im.split()

    # Preparing font to print ASNs
    d = ImageDraw.Draw(Merged_img)
    d.font = ImageFont.load_default(15)
    labels = {}

    for j in points:
        j.strip()
        i = j.split(' ')
        label = "AS"+str(i[0])
        lon = float(i[1])
        lat = float(i[2])

        if lat < ll[1][0] or lat > ll[3][0] or lon < ll[3][1] or lon > ll[1][1]:
            print(label,"with coordinates",lon,lat,"is out of this map.", file=sys.stderr)
            continue

        X = (lat-ll[1][0])*(xy[3][0]-xy[1][0])/(ll[3][0]-ll[1][0])
        Y = (ll[1][1]-lon)*(xy[3][1]-xy[1][1])/(ll[1][1]-ll[3][1])

#    print(X,Y)
        # Position to place the mark
        a = int(X) - im.size[0]//2
        b = int(Y) - im.size[1]

        # Position to print the text near mark
        a1 = a+im.size[0]
        b1 = b
        for m in labels:
            # I try to avoid text overlay
            if abs(m[1]-b1) < 15:
                b1 += 15
        labels.update({(a1,b1): label})
    
        Merged_img.paste(im,(a,b),mask)
#    img.paste(im, box=(a,b))


    for k,m in labels.items():
        d.text((k[0], k[1]), m,fill=(0, 0, 0))
#    d.text((k[0], k[1]), m,fill=(0, 0, 0, 255))

    Merged_img.save(f_out)

if __name__ == '__main__':
    i = 1
    base = ""
    in_file = ""
    mark_file = "mark.png"
    size = ""
    while i < len(sys.argv):
        if sys.argv[i][:2] == '-m':
            if len(sys.argv[i]) > 2:
                mark_file = sys.argv[i][2:]
            else:
                i += 1
                mark_file = sys.argv[i]
        elif sys.argv[i][:2] == '-b':
            if len(sys.argv[i]) > 2:
                base = sys.argv[i][2:]
            else:
                i += 1
                base = sys.argv[i]
        elif sys.argv[i][:2] == '-p':
            if len(sys.argv[i]) > 2:
                in_file = sys.argv[i][2:]
            else:
                i += 1
                in_file = sys.argv[i]
        i += 1

    if len(base) == 0 or len(in_file) == 0:
        quit('''
Missed input data.

Usage:
--------------------
draw_points.py [-m <mark_image_file>] -b <base_name> -p <points_file>
\tmark_image_file -- a PNG file with mark image to place on the map
\tbase_name -- name (without extension) of map file/borders file
\tpoint_file -- input file with ASNs and coordinates
        ''')

    draw_points(base, in_file, mark_file) 

