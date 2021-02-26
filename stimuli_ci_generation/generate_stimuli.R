## Docs: http://www.rondotsch.nl/wp-content/uploads/2014/09/Reverse-correlation-tutorial-1.pdf


# Install reverse correlation toolbox
# install.packages("rcicr", repos="http://R-Forge.R-project.org")
# REPO <- 'http://cran.us.r-project.org'
# options(repos = c("CRAN" = REPO))
# install.packages(c("splancs", "aspace"), repos="http://R-Forge.R-project.org")
# install.packages("rcicr", type="source", repos="http://R-Forge.R-project.org")

# Load reverse correlation toolbox
library(rcicr)

args <- commandArgs(trailingOnly = TRUE)
local_dir <- args[1]

print("getting ready for rcicr in R")
print(local_dir)

stimuli_des <- paste("./", local_dir, "/stimuli", sep = "")

# Generate and save stimuli
img_dir <- paste("./", local_dir, "/neutral.jpg", sep = "")
print("Looking for image in: ")
print(img_dir)
base_face_files <- list('mnes'=img_dir)
print(base_face_files)

## base_face_files  List containing base face file names (jpegs) used as base images for stimuli
## n_trials Number specifying how many trials the task will have (function will generate two images for each trial per base image: original and inverted/negative noise)
## img_size Number specifying the number of pixels that the stimulus image will span horizontally and vertically (will be square, so only one integer needed)
## stimulus_path Path to save stimuli and .Rdata file to

generateStimuli2IFC(base_face_files, n_trials=200, img_size=128, stimulus_path = stimuli_des)
