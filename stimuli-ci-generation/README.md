# Stimuli and ci generation for SIE

This is a docker containerized app that generates stimuli and ci on processed human face images.

Files in /archive are legacy files that are no longer needed for the current build of the app.

# Hierarchy of containers
Containers must be built in the following order and use the correct tags:

1\. rocker
- Dockerfile: `Dockerfile_rocker`
- Docker tag: `stimuli_ci_rocker`

2\. base
- Dockerfile: `Dockerfile_base`
- Docker tag: `stimuli_ci_base`

3\. app
- Dockerfile: `Dockerfile_app`
- Docker tag: `stimuli_ci_app`

# How to build
* Locally: 
 - run the build_local.sh script.

* Google Cloud Build
 - to be added

 # How to deploy
 * Google Cloud Run
  - Register the built image
 `docker push gcr.io/[gcp-project-name]/stimuli_ci_app`
  - Lunch cloud run instance from image: 
 `gcloud run deploy sie-stimuli-ci --image gcr.io/[gcp-project-name]/stimuli_ci_app --region northamerica-northeast1 docker run -t -d -p 16502:8080 -v`

