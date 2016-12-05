#!/usr/bin/env Rscript

################################################################################
# Script to plot a cluster plot from input file

args <- commandArgs(TRUE)

input.file <- args[1]
#input.file <- '/home/oyvind/harvest/media/local-disk/oyvindhe/scripts/import_intensities_to_sqlite/tmpout.txt'
#input.file <- '/media/local-disk/oyvindhe/scripts/import_intensities_to_sqlite/tmpout.txt'
output.path <- args[2]
#output.path <- '/home/oyvind/harvest/media/local-disk/oyvindhe/scripts/import_intensities_to_sqlite/'
#output.path <- '/media/local-disk/oyvindhe/scripts/import_intensities_to_sqlite/'
#output.file <- args[3]
#plot.file.prefix <- args[4]

library(ggplot2)
library(tidyr)
library(parallel)

# Load input data
snp <- read.table(input.file, header = F, stringsAsFactors = F)

# Convert first row containing sample info to a data frame with 3 columns
sample.row <- as.data.frame(matrix(unlist(snp[1,], use.names=FALSE),ncol=3, byrow=TRUE))
# set header and remove header line
colnames(sample.row) <- as.character(unlist(sample.row[1,]))
sample.row <- sample.row[-1, ]

# Function to plot a clusterplot from one row
plot.row <- function(row){
  # convert second/snp row to data frame with 3 columns
  snp.row <- as.data.frame(matrix(unlist(row, use.names=FALSE),ncol=3, byrow=TRUE))

  # extract first column of snp row for marker info
  snp.name <- as.character(snp.row[1,1])
  snp.chr <- as.character(snp.row[1,2])
  snp.pos <- as.character(snp.row[1,3])

  # remove first column with snp info from snp.row
  snp.row <- snp.row[-1, ]

  # name columns in snp row
  names(snp.row) <- c('Call','X','Y')

  sample.id <- separate(sample.row, col = Name, into = c('SentrixID', 'gtype'), sep = '\\.')$SentrixID

  # column bind the sample ID and SNP intensities
  total <- cbind(sample.id,snp.row)

  # convert to character and integer
  total$Call <- as.character(total$Call)
  total$X <- as.numeric(as.character(total$X))
  total$Y <- as.numeric(as.character(total$Y))

  # plot
  p <- ggplot(total) + geom_point(aes(X,Y, col=Call)) + ggtitle(snp.name)

  # save plot to drive
  ggsave(filename = paste0(snp.name,".png"),
         plot = p,
         path = output.path,
         width = 12,
         height = 8,
         device = "png")

}

# Calculate the number of cores
no_cores <- detectCores() - 1

# Initiate cluster
cl <- makeCluster(no_cores, type="FORK")

parApply(cl, snp[2:dim(snp)[1],], 1, FUN = plot.row)

#apply(snp[2:dim(snp)[1],], 1, FUN = plot.row)

# plot a chopped version where some signal intensisites are subset
#p2 <- ggplot(subset(total, X<3 & Y < 10)) + geom_point(aes(X,Y, col=Call)) + ggtitle(snp.name)

#ggsave(filename = paste0('chopped_', output.file),
#       plot = p,
#       path = output.path,
#       width = 12,
#       height = 8,
#       device = "png")

#ggplot(total) +
#  geom_point(aes(X,Y, col=as.factor(ifelse(sentrix %in% good.plate.samples,1,2)))) +
#  ggtitle('exm447541') +
#  scale_color_discrete(name="Experimental\nCondition", labels=c("Good", "Bad"))

# ggplot(z) + geom_point(aes(X,Y, col=as.factor(ifelse(sentrix %in% bad.plate.samples,0,1))))
