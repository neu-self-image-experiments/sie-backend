# This cloud function gets triggered by a change
# in `sie-raw-images` storage bucket
# It picks up the newly created image and sends it
# to cloud vision API for pre-processing
# Then runs the provided R-script to generate processed images

import os
from google.cloud import vision
from google.cloud import storage


def face_detection(uri):
    """
    This function detects the faces in the file
    located in Google Cloud Storage or the web
    Args:
        uri: the file located in Google Cloud Storage or the web
    returns:
        None: Prints the likelihood of the face expressions
        or returns an errors resonse in string format
    """
    vision_client = vision.ImageAnnotatorClient()
    print(vision_client)

    image = vision.Image()
    image.source.image_uri = uri

    response = vision_client.face_detection(image=image)
    faceAnnotations = response.face_annotations

    # Making sure that there's only one person in the frame
    if len(faceAnnotations) != 1:
        return "Please ensure exactly ONE face is in the image."

    # Lables of likelihood from google.cloud.vision.enums

    likelihood = (
        "unknown",
        "Very unlikely",
        "Unlikely",
        "Possibly",
        "Likely",
        "Very likely",
    )

    for face in faceAnnotations:
        print("Detection Confidence:  {0}".
              format(face.detection_confidence))
        print("Angry likelyhood:  {0}"
              .format(likelihood[face.anger_likelihood]))
        print("Joy likelyhood:  {0}".
              format(likelihood[face.joy_likelihood]))
        print("Sorrow likelyhood:  {0}".
              format(likelihood[face.sorrow_likelihood]))
        print("Surprise likelyhood:  {0}".
              format(likelihood[face.surprise_likelihood]))
        print("Headwear likelyhood:  {0}".
              format(likelihood[face.headwear_likelihood]))


def trigger_event(event, context):
    """
    Background Cloud Function to be triggered by Cloud Storage.
    This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                        The `data` field contains a description of the event in
                        the Cloud Storage `object` format described here:
                        https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    bucket_name = event["bucket"]
    source_img = event["name"]
    tmp_download_path = f"/tmp/{source_img}"

    try:
        download_image(bucket_name, source_img, tmp_download_path)
        print(f"Image {source_img} downloaded to {tmp_download_path}")
        # currenlty this makes sure there's one person
        # in the frame and prints a few other details
        face_detection(tmp_download_path)
        # TODO(jerry) call R script with features returned from Abi's part
        # TODO(hantao) put processed images to `sie-processed-images` bucket
    except Exception:
        pass
    finally:
        if os.path.isfile(tmp_download_path):
            os.remove(tmp_download_path)
        else:
            print("Error: %s file not found" % tmp_download_path)


def download_image(bucket_name, source_blob_name, destination_file_name):
    """Downloads the specified image from cloud storage
    Args:
        bucket_name = "your-bucket-name"
        source_blob_name = "image-name"
        destination_file_name = "local/path/to/file"

    Returns:
        Local path to downloaded image
    """

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_processed_images(bucket_name, source_file_folder):
    """Uploads images to the bucket.
    Args:
        bucket_name = "your-bucket-name"
        source_file_folder = Path to the folder that contains
                                all the processed images

    Returns:
        None;
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for file_name in os.listdir(source_file_folder):
        blob = bucket.blob(file_name)
        blob.upload_from_filename(os.path.join(source_file_folder, file_name))

        print("File {} uploaded to {}.".format(file_name, bucket_name))
