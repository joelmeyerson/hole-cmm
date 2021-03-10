#------------------------------------------------- holecmm.py --------------------------------------------
#  
#  Python script to convert the output of HOLE to a CMM file that can be visualized in Chimera or ChimeraX.
#  
#  Usage:
#      python holecmm.py 
#
#  Show inputs:
#      python holecmm.py -h 
#
#  Parameters:
#      -i <input file> (required)
#      -o <output file name> (optional, defaults to input file base name with cmm file extension)
#      -r <value for sphere radius> (optional, defaults to 0.2)
#      -c1 <Hex color value for pore radius < 1.15 Ang> (optional, defaults to red FF0000)
#      -c2 <Hex color value for 1.15 Ang > pore radius < 2.30 Ang> (optional, defaults to green 00FF00)
#      -c3 <Hex color value for pore radius > 2.30 Ang> (optional, defaults to blue 0000FF)
#
#  Examples:
#      python holecmm.py -i dotsurface-kcsa.vmd_plot 
#      python holecmm.py -i dotsurface-kcsa.vmd_plot -o kcsa.cmm -r 0.2 -c1 FF6347 -c2 90EE90 -c3 6495ED
#      python holecmm.py -i hole-surface-dots.dat
#
#---------------------------------------------------------------------------------------------------------

import sys, os, re, argparse

# create argument parser
parser = argparse.ArgumentParser(description='Convert HOLE output to a CMM file.')

parser.add_argument('-i', metavar='input', type=str, help='Input file.', required=True)
parser.add_argument('-o', metavar='output', type=str, default='NA', help='Output file.')
parser.add_argument('-r', metavar='radius', type=float, default='0.2', help='Radius for markers.')
parser.add_argument('-c1', metavar='color', type=str, default='NA', help='Hex color for pore radius less than 1.15 Ang.')
parser.add_argument('-c2', metavar='color', type=str, default='NA', help='Hex color for pore radius between 1.15 Ang and 2.30 Ang.')
parser.add_argument('-c3', metavar='color', type=str, default='NA', help='Hex color for pore radius greater than 2.30 Ang.')

# parse args
args = parser.parse_args()

# parse input
ipath = args.i # input and path
iname = os.path.basename(args.i) # input file name
ibasename = os.path.splitext(iname)[0] # input base name
iext = os.path.splitext(iname)[-1] # input extension

# check input file exists
if os.path.isfile(ipath):
    pass
else:
    print("Input file not found.")
    exit()

# parse output
if args.o == 'NA':
    oname = 'hole.cmm'
else:
    oname = args.o;
    
# parse colors
if args.c1 == 'NA': c1 = 'FF0000'
else: c1 = args.c1

if args.c2 == 'NA': c2 = '00FF00'
else: c2 = args.c2

if args.c3 == 'NA': c3 = '0000FF'
else: c3 = args.c3

if len(c1) == 6 and len(c2) == 6 and len(c3) == 6:
    if c1[1:].isalnum() and c2[1:].isalnum() and c3[1:].isalnum():
        pass
    else:
        print("Colors must be in hex format.")
        exit()
else:
    print("Colors must be in hex format.")
    exit()

# convert from HEX to RGB
c1R, c1G, c1B = int(c1[0:2], 16)/255.0, int(c1[2:4], 16)/255.0, int(c1[4:6], 16)/255.0
c2R, c2G, c2B = int(c2[0:2], 16)/255.0, int(c2[2:4], 16)/255.0, int(c2[4:6], 16)/255.0
c3R, c3G, c3B = int(c3[0:2], 16)/255.0, int(c3[2:4], 16)/255.0, int(c3[4:6], 16)/255.0

# read input file
ifile = open(ipath, 'r')

# create output file and add header
ofile = open(oname, 'w+')
ofile.write('<marker_set name="marker set 1">\n') 

# marker ID counter
id = 0

if iext == '.vmd_plot': # process .vmd_plot file from HOLE

    for line in ifile.readlines():

        # iterate ID counter
        id += 1

        if line.startswith('draw point'):

            # extract x, y, z coordinates from lines in .vmd_plot file
            [x, y, z] = re.findall('\d+\.\d+', line)
            x = float(x)
            y = float(y)
            z = float(z)

            # write line to CMM file
            ofile.write("<marker id=\"%d\" x=\"%5.2f\" y=\"%5.2f\" z=\"%5.2f\" %s radius=\"%2.1f\"/>\n" % (id, x, y, z, color, args.r))
            
        elif line.startswith('draw color yellow'):
            pass

        elif line.startswith('draw color red'):
            color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c1R, c1G, c1B)

        elif line.startswith('draw color green'):
            color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c2R, c2G, c2B)

        elif line.startswith('draw color blue'):
            color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c3R, c3G, c3B)

        else:
            pass
    
elif iext == '.dat': # process .dat file from HOLE in COOT
    
    # true if any colors specified
    customcolor = args.c1 != 'NA' or args.c2 != 'NA' or args.c3 != 'NA'
    
    if customcolor == False: 
        for line in ifile.readlines():

            # iterate ID counter
            id += 1
        
            # extract x, y, z coordinates from lines in .dat file
            x = float(line.split()[0])
            y = float(line.split()[1])
            z = float(line.split()[2])
            r = float(line.split()[3])
            g = float(line.split()[4])
            b = float(line.split()[5])
            
            # set color
            color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (r, g, b)
            
            # write line to CMM file
            ofile.write("<marker id=\"%d\" x=\"%5.2f\" y=\"%5.2f\" z=\"%5.2f\" %s radius=\"%2.1f\"/>\n" % (id, x, y, z, color, args.r))
    else: # use custom colors
        for line in ifile.readlines():

            # iterate ID counter
            id += 1
        
            # extract x, y, z coordinates from lines in .dat file
            x = float(line.split()[0])
            y = float(line.split()[1])
            z = float(line.split()[2])
            r = float(line.split()[3])
            g = float(line.split()[4])
            b = float(line.split()[5])
            
            if r >= g and r >= b:
                color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c1R, c1G, c1B)
                
            elif g >= r and g >= b:
                color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c2R, c2G, c2B)

            else:
                color = "r=\"%3.2f\" g=\"%3.2f\" b=\"%3.2f\"" % (c3R, c3G, c3B)
                
            # write line to CMM file
            ofile.write("<marker id=\"%d\" x=\"%5.2f\" y=\"%5.2f\" z=\"%5.2f\" %s radius=\"%2.1f\"/>\n" % (id, x, y, z, color, args.r))
        
else:
    print("Input file %s does not have .vmd_plot or .dat file extension." % iname)
    exit()

# close input file
ifile.close()
    
# write footer and close output file
ofile.write('</marker_set>')
ofile.close()

