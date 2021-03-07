#!/usr/bin/env Rscript

## Docs: http://www.rondotsch.nl/wp-content/uploads/2014/09/Reverse-correlation-tutorial-1.pdf

# Load reverse correlation toolbox
library(rcicr)

args <- commandArgs(trailingOnly = TRUE)
output_dir <- args[1]

stimuli_des <- paste(output_dir, "/stimuli", sep = "")

# Generate and save stimuli
img_dir <- paste(output_dir, "/neutral.jpg", sep = "")
base_face_files <- list('mnes'=img_dir)

# http://www.rondotsch.nl/rcicr/
generateStimuli2IFC(
    base_face_files, # list of base face file names (jpegs) used as base images for stimuli
    n_trials=200, # num trials the task will have (generate one original and one inverted/negative noise)
    img_size=128, # num pixels of stimulus image
    stimulus_path = stimuli_des # path where stimuli and .Rdata file are saved
)
