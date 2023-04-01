"""HOLE to CMM

This script converts the output of HOLE to a CMM file that can be visualized in UCSF Chimera or ChimeraX.

Usage:
    python holecmm.py 

Options:
    -i <input file> (required)
    -o <output file name> (optional, defaults to input file base name with cmm file extension)
    -r <value for sphere radius> (optional, defaults to 0.2)
    -c1 <Hex color value for pore radius < 1.15 Ang> (optional, defaults to red FF0000)
    -c2 <Hex color value for 1.15 Ang > pore radius < 2.30 Ang> (optional, defaults to green 00FF00)
    -c3 <Hex color value for pore radius > 2.30 Ang> (optional, defaults to blue 0000FF)

Examples:
    python holecmm.py -i dotsurface-kcsa.vmd_plot 
    python holecmm.py -i dotsurface-kcsa.vmd_plot -o kcsa.cmm -r 0.2 -c1 FF6347 -c2 90EE90 -c3 6495ED
    python holecmm.py -i hole-surface-dots.dat

"""

import argparse
import os
import re
import sys


parser = argparse.ArgumentParser(description="Convert HOLE output to a CMM file.")
parser.add_argument("-i", metavar="input", type=str, help="Input file.", required=True)
parser.add_argument(
    "-o", metavar="output", type=str, default="hole.cmm", help="Output file."
)
parser.add_argument(
    "-r", metavar="radius", type=float, default="0.2", help="Radius for markers."
)
parser.add_argument(
    "-c1",
    type=str,
    default="FF0000",
    help="Hex color for pore radius less than 1.15 Ang.",
)
parser.add_argument(
    "-c2",
    type=str,
    default="00FF00",
    help="Hex color for pore radius between 1.15 Ang and 2.30 Ang.",
)
parser.add_argument(
    "-c3",
    type=str,
    default="0000FF",
    help="Hex color for pore radius greater than 2.30 Ang.",
)

args = parser.parse_args()
input_path = args.i
input_name = os.path.basename(args.i)
input_basename = os.path.splitext(input_name)[0]
input_extension = os.path.splitext(input_name)[-1]
output_file_name = args.o

if not os.path.isfile(input_path):
    print("Input file not found.")
    sys.exit()

try:
    int(args.c1, 16) and int(args.c2, 16) and int(args.c3, 16)
except ValueError as ve:
    print('Colors must be a string in hex format ("23A5B0")')

# Convert from HEX to RGB.
c1r, c1g, c1b = (int(args.c1[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
c2r, c2g, c2b = (int(args.c2[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
c3r, c3g, c3b = (int(args.c3[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

input_file = open(input_path, "r")
output_file = open(output_file_name, "w+")
output_file.write('<marker_set name="marker set 1">\n')

marker_id = 0

if input_extension == ".vmd_plot":
    for line in input_file.readlines():
        marker_id += 1

        if line.startswith("draw color yellow"):
            pass
        elif line.startswith("draw color red"):
            r, g, b = c1r, c1g, c1b
        elif line.startswith("draw color green"):
            r, g, b = c2r, c2g, c2b
        elif line.startswith("draw color blue"):
            r, g, b = c3r, c3g, c3b
        elif line.startswith("draw point"):
            x, y, z = re.findall("\d+\.\d+", line)
            x, y, z = float(x), float(y), float(z)
            output_file.write(
                f'<marker id="{marker_id}" x="{x}" y="{y}" z="{z}" r="{r}" g="{g}" b="{b}" radius="{args.r}"/>\n'
            )
        else:
            pass

elif input_extension == ".dat":
    for line in input_file.readlines():
        marker_id += 1

        x, y, z, dat_red, dat_green, dat_blue = (
            float(value) for value in line.split()[0:6]
        )

        if dat_red >= dat_green and dat_red >= dat_blue:
            r, g, b = c1r, c1g, c1b
        elif dat_green >= dat_red and dat_green >= dat_blue:
            r, g, b = c2r, c2g, c2b
        else:
            r, g, b = c3r, c3g, c3b

        output_file.write(
            f'<marker id="{marker_id}" x="{x}" y="{y}" z="{z}" r="{r}" g="{g}" b="{b}" radius="{args.r}"/>\n'
        )

else:
    print(f"Input file {input_name} does not have a .vmd_plot or .dat file extension.")
    sys.exit()

input_file.close()
output_file.write("</marker_set>")  # Write footer.
output_file.close()
