# Install reverse correlation toolbox
install.packages("rcicr", repos="http://R-Forge.R-project.org")

# Load reverse correlation toolbox
library(rcicr)
args <- commandArgs(trailingOnly = TRUE)
bucket <- args[1]
csv_dir <- paste("./", bucket, "/user_selection.csv", sep = "")
rawData <- read.csv(file = csv_dir)

stimuli_dir <- paste("./", bucket, "/stimuli/", sep = "")
# setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
filename = list.files(path = stimuli_dir, pattern = "*.Rdata")
filename = paste(stimuli_dir, filename, sep="")
groupci <- generateCI2IFC(rawData$stimulus, rawData$response,
                          'mnes', filename, saveasjpeg=FALSE,
                          targetpath = paste("./", bucket, "/cis", sep = ""))
groupci <- autoscale(list('groupci'=groupci),
                     targetpath = paste("./", bucket, "/cis", sep = ""))