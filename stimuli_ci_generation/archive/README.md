# Image Processing Pipeline

Build image:
cloud builds submit --tag gcr.io/ubc-sea-projects/{image_name} --timeout=1200s.

Run image on cloud run:
gcloud run deploy --image gcr.io/ubc-sea-projects/{image_name} --platform managed

input:
google_storage_bucket:user_selection.csv, MNES.jpg


```

// run server in docker container
docker build -t selfimage-r-base .
docker build -f Dockerfile_server -t selfimage-r .

docker run -t -d -p 16502:8080 -v $GOOGLE_APPLICATION_CREDENTIALS:/ubc-sea-projects-b25cc4d712e1.json:ro -e GOOGLE_APPLICATION_CREDENTIALS=ubc-sea-projects-b25cc4d712e1.json selfimage-r:latest

// build and tag images
docker build -f Dockerfile_sie_base -t sie_base .
docker build -f Dockerfile_sie_py_env -t sie_py_server .

// run server
docker run -t -d -p 16502:8080 -v $GOOGLE_APPLICATION_CREDENTIALS:/ubc-sea-projects-b25cc4d712e1.json:ro -e GOOGLE_APPLICATION_CREDENTIALS=ubc-sea-projects-b25cc4d712e1.json sie_py_server

docker run -e PASSWORD=<YOUR_PASS> -p 8787:8787 rocker/rstudio

```



