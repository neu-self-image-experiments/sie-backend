#!/usr/bin/env Rscript

# Load reverse correlation toolbox
library(rcicr)
args <- commandArgs(trailingOnly = TRUE)
work_dir <- args[1]
csv_dir <- paste(work_dir, "/user_selection.csv", sep = "")
raw_data <- read.csv(file = csv_dir)

stimuli_dir <- paste(work_dir, "/stimuli/", sep = "")
# setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
rdata = list.files(path = stimuli_dir, pattern = "*.Rdata")
rdata = paste(stimuli_dir, rdata, sep="")

groupci <- generateCI2IFC(
    stimuli=raw_data$stimulus, # vector containing seq numbers of presented stimuli
    responses=raw_data$response, # response to stimuli (1 = orig, -1 = inverted)
    baseimage='mnes', # string specifying the key used in list of base images 
    rdata=rdata, 
    saveasjpeg=FALSE,
    targetpath = paste(work_dir, "/ci", sep = "")
)

groupci <- autoscale(
    list('groupci'=groupci),
    targetpath = paste(work_dir, "/ci", sep = "")
)