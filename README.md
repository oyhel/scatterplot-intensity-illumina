# scatterplot-intensity-illumina
Utility to create scatter plot from raw Illumina Genome Studio exports

## How it works
- The export is first indexed (to allow for quicker subsequent lookups). Later plots can be plotted much faster by reusing the indexfile.
- A provided list of markers will use the indexfile to locate the specific marker rows in the export
- Rows are extracted to a temporary file
- Temporary file is sent to Rscript for plotting all markers in the temprorary file (plots are plotted in parallel using 1-cores available)

## Dependencies 
- R-packages: ggplot2, tidyr and dplyr

## Expected format
The tool expects a raw intensity GS report to have:
  - A header row 
  - 3 first columns: name, chromosome and position of marker
  - After the 3 first columns - every 3 columns per sample:
      - Genotype
      - X-intensity
       -Y-intensity
