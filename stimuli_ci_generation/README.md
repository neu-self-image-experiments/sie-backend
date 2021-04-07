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
- Dockerfile: `Dockerfile`
- Docker tag: `stimuli_ci_app`

# How to build
- Locally: 
  - run the build_local.sh script.

- Google Cloud Build
  ```
  // Build docker images
    GCP_PROJECT=<GCP_PROJECT>
    PROJECT_NUMBER=<PROJECT_NUMBER>
    CLOUD_RUN_ENDPOINT=<CLOUD_RUN_ENDPOINT>

    cd stimuli_ci_generation
    gcloud builds submit --config cloudbuild.yml .

    // Or update stimuli_ci_app only
    gcloud builds submit --config cloudbuild-update.yml .

  ```

# How to deploy
- Google Cloud Run
    ```
    // Deploy docker container
    gcloud run deploy sie-image-processing --image gcr.io/$GCP_PROJECT/stimuli_ci_app:latest

    // select [1] Cloud Run (fully managed)
    // select [17] northamerica-northeast1 region
    // Allow unauthenticated invocations to [sie-image-processing] (y/N)?  n

    // Create a pub/sub topic
    gcloud pubsub topics create sie-image-processing

    // Allow pub/sub to create authentication tokens in your project
    gcloud projects add-iam-policy-binding $GCP_PROJECT \
    --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
    --role=roles/iam.serviceAccountTokenCreator

    // Create a service account for the subscription
    gcloud iam service-accounts create sie-cloud-run-pubsub-invoker \
        --display-name "SIE Cloud Run Pub/Sub Invoker"

    gcloud run services add-iam-policy-binding sie-image-processing \
    --member=serviceAccount:sie-cloud-run-pubsub-invoker@$GCP_PROJECT.iam.gserviceaccount.com \
    --role=roles/run.invoker
   
    // Create a pub/sub subscription with service account that you created with
    // the required permissions
    gcloud beta pubsub subscriptions create sie-cloud-run --topic sie-image-processing \
    --push-endpoint=$CLOUD_RUN_ENDPOINT \
    --push-auth-service-account=sie-cloud-run-pubsub-invoker@$GCP_PROJECT.iam.gserviceaccount.com

    // Create storage triggers that sends a message to cloud run
    gsutil notification create -t sie-image-processing -f json -e OBJECT_FINALIZE gs://sie-masked-images

    gsutil notification create -t sie-image-processing -f json -e OBJECT_FINALIZE gs://sie-user-selections

    // Test
    gsutil cp /path/to/local/file gs://bucket
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