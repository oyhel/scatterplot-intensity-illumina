#!/usr/bin/env bash

# Script to plot a list of markers in all batches

markerlist=$1

# MOBA12BAD-REC
echo "Plotting markers for MOBA12BAD-RECLUSTERED"
./plot_markers.py \
    -t /media/local-disk/common/gsexport/moba12-1692-bad-plate-samples-reclust/moba12-1692-bad-plate-samples-fulldata.txt \
    -i indexes/moba12badrec-index \
    -m $markerlist \
    -o test/moba12badrec

# MOBA24
echo "Plotting markers for MOBA24"
mkdir -p test/moba24/top-lrr-fail
./plot_markers.py \
    -t /media/local-disk/common/gsexport/moba_24v10_n12874inc135regdup9dualdup_reclust/moba-gs-zt-HCE24v10-n12874inc135regdup9dualdup-20160121-reclust-export-from-gs-fulldata.txt \
    -i indexes/moba24-index \
    -m $markerlist \
    -o test/moba24/top-lrr-fail

# MOBA12GOOD-REC
echo "Plotting markers for MOBA12GOOD-RECLUSTERED"
./plot_markers.py \
    -t /media/local-disk/common/gsexport/moba_12v11_n18972_good_plate_samples_reclust/moba12-18972-good-plate-samples-reclust-fulldata.txt \
    -i indexes/moba12goodrec-index \
    -m $markerlist \
    -o test/moba12goodrec

# MOBA12
echo "Plotting markers for MOBA12-ALL-SAMPLES-JOINT-CALLING CUSTOM CLUSTERFILE"
./plot_markers.py \
    -t /media/local-disk/common/gsexport/moba_12v11_n20664inc222regdup21ratio_2hapmap_reclust/moba-gs-zt-HCE12v11-n20664inc222regdup21ratio-2hapmap-20151221-reclust-fulldata.txt \
    -i indexes/moba12-index \
    -m $markerlist \
    -o test/moba12

# MOBA12ILLU
echo "Plotting markers for MOBA12-ALL-SAMPLES-JOINT-CALLING ILLUMINA CLUSTERFILE"
./plot_markers.py \
    -t /media/local-disk/common/gsexport/gs-export-old/moba_12v11_n20667inc222regdup21ratio_2hapmap/moba-gs-zt-HCE12v11-n20667inc222regdup21ratio-2hapmap-20150616-fulldata.txt \
    -i indexes/moba12illu-index \
    -m $markerlist \
    -o test/moba12illu

# MOBA24ILLU
echo "Plotting markers for MOBA24 ILLUMINA CLUSTERFILE"
./plot_markers.py \
    -t /media/local-disk/common/gsexport/gs-export-old/moba_24v10_n12874inc135regdup9dualdup/moba-gs-zt-HCE24v10-n12874inc135regdup9dualdup-20150610-fulldata.txt \
    -i indexes/moba24illu-index \
    -m $markerlist \
    -o test/moba24illu
