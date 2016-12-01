#!/usr/bin/python

# Specify raw intensity file 
file = "/media/local-disk/common/gsexport/moba12-1692-bad-plate-samples-reclust/moba12-1692-bad-plate-samples-fulldata.txt"

# Open the file with read only permission
f = open(file, "r")

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
indexfile = open('indexfile.txt', 'w')
for i in index: 
   indexfile.write(str(i)+'\n')


