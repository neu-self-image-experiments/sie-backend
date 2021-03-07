#!/bin/bash
GCP_PROJECT='cs6510-spr2021'

docker build -f Dockerfile_rocker -t stimuli_ci_rocker . 
docker build -f Dockerfile_base_local -t stimuli_ci_base . 
docker build -f Dockerfile_local -t stimuli_ci_app . 

# docker build -f Dockerfile_local -t gcr.io/$GCP_PROJECT/stimuli_ci_app .