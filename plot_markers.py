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

# Open full table file
table = open(args.table, "r")


def index_intensity_file(f):
    # Create index tmp list
    index = []

    # Get position of beginning of file (obviously 0)
    pos = f.tell()

    # Read the first line, cursor will move to beginning of next line
    # ie. it will skip the first line with the sample headers when
    # creating the indexfile
    line= f.readline()

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
	ind= os.path.join(args.outpath, args.indexfile)

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
    # Check if marker in list exists in lookuptable (aka. indexfile)
    if marker in lookup:
        print(marker)
        fetch_intensity_row(marker, lookup[marker])


# Write only the rows to tmp output before sending it to R script
tmpout = open(os.path.join(args.outpath, 'tmpout.txt'), 'a+')
for i in rowlist:
   tmpout.write(i)

tmpout.close()

# Call Rscript for plotting the markers
subprocess.call (["/usr/bin/Rscript", "lib/make_cluster_plot.R", os.path.join(args.outpath, 'tmpout.txt'), args.outpath])

# Remove tmpout.txt
os.remove(os.path.join(args.outpath, 'tmpout.txt'))
