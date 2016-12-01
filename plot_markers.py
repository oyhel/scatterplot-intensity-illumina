#!/usr/bin/env python3

import sys
import argparse
import subprocess
import os

### PARSE COMMAND LINE ARGUMENTS

parser = argparse.ArgumentParser(description='Extract intensity info rows from file')
parser.add_argument('-t', '--table', help='path to full intensity table')
parser.add_argument('-i', '--indexfile', help='corresponding index file for fulltable')
parser.add_argument('-m', '--markerlist', help='list of markers to plot')
parser.add_argument('-o', '--outpath', help='output path of plots and index')
parser.add_argument('-r', '--reindex', help='reindex intensity file', action='store_true')
args = parser.parse_args()


table = open(args.table, "r")


def index_intensity_file(f):
    # Create index tmp list
    index = []

    # Get position of beginning of file (obviously 0)
    pos = f.tell()

    # Read the first line, cursor will move to beginning of next line
    line= f.readline()

    # Get the name of the "marker" in the first line, will be "Name"
    marker = line.partition("\t")[0]

    # Create the row and append to list
    tmp = marker + "\t" + str(pos)
    index.append(tmp)

    # Loop over rest of file
    while line:
        # Get the position of the current position before reading the line
        # which will move the position (we want the pos at the start of the line)
        pos = f.tell()

        # Read the line starting with the position above (cursor will then move)
        line = f.readline()

        # Extract the marker name
        marker = line.partition("\t")[0]

        # Create the row and save to index
        tmp = marker + "\t" + str(pos)

        if marker:
            index.append(tmp)

    # Write to indexfile
    indexfile = open(os.path.join(args.outpath, args.indexfile), 'w')
    for i in index:
        indexfile.write(str(i)+'\n')

ind = ""
if args.reindex:
	index_intensity_file(table)
	ind = os.path.join(args.outpath, args.indexfile)
else:
	ind=args.indexfile

# Load indexfile into lookup dictionary
lookup = {}

with open(ind) as f:
    for line in f:
        (key,val) = line.split()
        #print "key: " + str(key)
        #print "val: " + val
        lookup[key] = val

# Function to append header from fulltable
rowlist=[]

# Function to append header from fulltable
def attach_header():
	table.seek(0,0)
	header = table.readline()
	rowlist.append(header)


# Fetch marker row from intensity file
def fetch_intensity_row(marker, pos):
	table.seek(0,0)
	table.seek(int(pos))
	row = table.readline()
	rowlist.append(row)

attach_header()

for m in open(args.markerlist, "r"):
	marker = m.strip()
	fetch_intensity_row(marker, lookup[marker])

#print(rowlist)

# Write output
tmpout = open(os.path.join(args.outpath, 'tmpout.txt'), 'a+')
for i in rowlist:
   tmpout.write(i)

tmpout.close()

# Call Rscript for plotting the markers
subprocess.call (["/usr/bin/Rscript", "lib/make_cluster_plot.R", os.path.join(args.outpath, 'tmpout.txt'), args.outpath])


# Specify raw intensity file
#file = "/media/local-disk/common/gsexport/moba12-1692-bad-plate-samples-reclust/moba12-1692-bad-plate-samples-fulldata.txt"

# Open the file with read only permission
#f = open(file, "r")
