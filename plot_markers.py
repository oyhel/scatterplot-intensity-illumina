#!/usr/bin/env python3

import sys
import argparse
import subprocess
import os
import warnings

### PARSE COMMAND LINE ARGUMENTS

parser = argparse.ArgumentParser(description='Creates intensity plots for a list of markers using data from Genome Studio export')
parser.add_argument('-t', '--table', help='path to full intensity table')
parser.add_argument('-i', '--indexfile', help='path to corresponding index file for full intensity table (if index file does not exist it will be created at this location)')
parser.add_argument('-m', '--markerlist', help='list of markers to plot (one marker per line)')
parser.add_argument('-o', '--outpath', help='output path of plots')
parser.add_argument('-r', '--reindex', help='reindex intensity file (this is done automatically if indexfile does not exist)', action='store_true')
args = parser.parse_args()

# FUNCTION DECLARATION

def index_intensity_file(f, indexfile):
    """ Indexes the intensity file
    Args:
        f: the file handler for the intensity table
        indexfile: full path to index file
    """
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
    indexfile = open(indexfile, 'w')
    for i in index:
        indexfile.write(str(i)+'\n')


def attach_header(f, l):
    """ Attaches the first line of the input to the list.
    I.e. attaches the header
    Args:
        f: file handler for the file
        l: list to append to
    Returns:
        the list, l, with header appended
    """
    f.seek(0,0)
    header = f.readline()
    l.append(header)
    return l


# Fetch marker row from intensity file
""" Extracts a single row from the intensity file given the marker name
    and the byte position of the start of the line/row
    Args:
        f: file handler for the intensity file
        marker: name of marker to extract
        pos: byte position at the beginning of the line containing intensities for the marker. This is stored in the indexfile
    """
def fetch_intensity_row(f, marker, pos):
    table.seek(0,0)
    table.seek(int(pos))
    row = table.readline()
    rowmarker = row.split()[0]
    if rowmarker != marker:
        print("ERROR: Marker in row does not match expected marker")
        sys.exit()
    rowlist.append(row)


### SCRIPT ###

# Open full intensity table file
table = open(args.table, "r")

# Reindex the intensity file if:
# 1) --reindex flag is specified
# 2) index file does not exist

ind = ""
if args.reindex or not os.path.isfile(args.indexfile):
	print("Indexing the intensity file to: " + str(args.indexfile))
	index_intensity_file(table, args.indexfile)
	ind = args.indexfile
else:
	ind = args.indexfile

# Load indexfile into lookup dictionary
lookup = {}

with open(ind) as f:
    for line in f:
        (key,val) = line.split()
        lookup[key] = val

# Create tmp list to store rows extracted from intensity table
rowlist=[]

# Attach header from the intensity file to tmp list
rowlist = attach_header(table, rowlist)

# Iterate over markers in markerlist and fetch rows
for m in open(args.markerlist, "r"):
    marker = m.strip()
    # Check if marker in list exists in lookuptable (aka. indexfile)
    if marker in lookup:
        fetch_intensity_row(table, marker, lookup[marker])
    else:
        warnings.warn("Marker " + marker + " is not found in intensity file index")

# Specify temporary file
tmpoutfile = os.path.join(args.outpath, 'tmpout-54543463.txt')

# Delete temporary file should it exist (eg. from a failed previous run)
if os.path.isfile(tmpoutfile):
    print("Removing existing temporary file: tmpout.txt")
    os.remove(tmpoutfile)

# Write the row list to tmp file
tmpout = open(tmpoutfile, 'a+')

for i in rowlist:
   tmpout.write(i)

# Close file handler
tmpout.close()

# Call Rscript to plot the markers
subprocess.call (["/usr/bin/Rscript", "lib/make_cluster_plot.R", tmpoutfile, args.outpath])

# Remove tmpout.txt
os.remove(tmpoutfile)
