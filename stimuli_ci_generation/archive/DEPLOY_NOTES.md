# Deploy Stimuli Generation

* Create the docker container: 
   ```
docker build -f Dockerfile_3 -t si_rocker_1 .
 docker build -f Docker_4 -t si_rocker_2 .
docker build -t gcr.io/ubc-sea-projects/stimuli_gen -f Dockerfile_5 -t . 
docker push gcr.io/ubc-sea-projects/stimuli_gen
gcloud run deploy self-image-stimuli-gen --image gcr.io/ubc-sea-projects/stimuli_gen --region northamerica-northeast1
docker run -t -d -p 16502:8080 -v 
   ```