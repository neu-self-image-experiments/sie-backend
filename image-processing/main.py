# This cloud function gets triggered by a change
# in `sie-raw-images` storage bucket
# It picks up the newly created image and sends it
# to cloud vision API for pre-processing
# Then runs the provided R-script to generate processed images

import os
from google.cloud import storage


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
        # TODO(abi) call cloud vision API with this image
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

def upload_processeed_images(bucket_name, source_file_name, destination_blob_name):
    """Uploads image files to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for file_name, blob_name in zip(source_file_name, destination_blob_name):
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_name)
    
        print(
            "File {} uploaded to {}.".format(
                file_name, blob_name
            )
        )
