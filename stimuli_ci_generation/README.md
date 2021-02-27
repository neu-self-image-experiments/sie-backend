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
- Locally: 
  - run the build_local.sh script.

- Google Cloud Build
  - to be added

# How to deploy
- Google Cloud Run
  - Register the built image
    ```
    docker push gcr.io/[gcp-project-name]/stimuli_ci_app
    ```
  - Launch cloud run instance from image: 
    ```
    gcloud run deploy sie-stimuli-ci \
    --image gcr.io/[gcp-project-name]/stimuli_ci_app \
    --region northamerica-northeast1 \
    docker run -t -d -p 16502:8080 -v
    ```

# Progress
 - Prelimenary clean-ups of files from previous repo.
 - A few quick bug fixes and clean-up on previous codes.
 - Some documentation on how to build locally and a script.
 - Test build and depolyment on google cloud run.

# Work to be done
* Triggered cloud function to send POST request to the deployed app.
* Testing on the functionality of the app.
* Minor changes to behavior and make compatible with the other component of the pipeline (After complete pipeline design).
* Documentation.
* Code refactoring and optimization.