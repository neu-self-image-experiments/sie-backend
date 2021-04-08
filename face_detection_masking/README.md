## Face detection and masking pipeline

### Description
This is the first part of the image processing pipeline. When a user uploads a photo it will stored in `sie-raw-images` bucket. The image filename should be of the form `user_id-experiment_id.jpg` (seperated by '-'). Once uploaded, the event will trigger the `trigger_detect_and_mask()` function (check `main.py`) which will validate and process the image. 

The cloud function will validate the image (see Exceptions below) and resize, crop, grayscale, and mask the image for generating stimuli. Once the processing is completed it will be stored in `sie-masked-image` bucket at `user_id-experiment_id/neutral.jpg` location. 

### Local Development

For developing locally, you will need an IAM token for the service account: `cloud-vision@cs6510-spr2021.iam.gserviceaccount.com`. 

- You can get the token from GCP console or ask the GCP project owner to provide you one. 
- Once you get the json file (eg: GVServiceAccountToken.json), place it in your /home directory. 
- Set `GOOGLE_APPLICATION_CREDENTIALS` in your .bashrc:
 `export GOOGLE_APPLICATION_CREDENTIALS="/home/<user>/GVServiceAccountToken.json`
- This token will allow you to use the Google Vision API.


### Run Unit Tests

Make sure to cd into `/face_dectection_masking` folder. Then run the following command:

```
pytest test_face_detection_masking.py
```

### Upload Cloud Function

Push your local cloud functions to google cloud. First make sure to cd into `/face_dectection_masking` folder. Then run the following command:

```
gcloud functions deploy trigger_detect_and_mask --runtime python38 --trigger-bucket sie-raw-images
```

### Exceptions

Here is the list of exceptions thrown by the face detection and masking pipeline.

| Exception       | Message        | Status code  | Description |
|:------------- |:-------------|:-----| :-----|
| InvalidFaceImage | Please make sure your image has neutral facial expression. | 400 | When face expression in not neutral (like smiling, crying etc) |
| InvalidFaceImage | Please make sure your image is well-lit. | 400 | When the image is dark |
| InvalidFaceImage | Please make sure your image is clear. | 400 | When image is blurry or noisy |
| InvalidFaceImage | Please face straight towards your camera, avoid tiliting. | 400 | When face is not straight upright |
| InvalidFaceImage | Please ensure exactly ONE face is in the image. | 400 | When there is not exactly ONE face in the image |
| InvalidFaceImage | Please ensure your full face is visible in the image, including both ears. | 400 | When face attributes are partially covered |