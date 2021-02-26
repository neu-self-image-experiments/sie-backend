#!/bin/bash
GCP_PROJECT='cs6510-spr2021'

docker build -f Dockerfile_rocker -t stimuli_ci_rocker . |
docker build -f Dockerfile_base -t stimuli_ci_base . |
docker build -f Dockerfile_app -t gcr.io/$GCP_PROJECT/stimuli_ci_app .