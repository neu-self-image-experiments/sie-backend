import os
from google.cloud import storage


def download_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads the specified image from cloud storage
    Args:
        bucket_name: bucket to download from
        source_blob_name: file to download
        destination_file_name: where to download to

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


def upload_files(bucket_name, source_file_folder):
    """Uploads images to the bucket.
    Args:
        bucket_name: bucket to upload files to
        source_file_folder: Path to the folder to be uploaded

    Returns:
        None
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for file_name in os.listdir(source_file_folder):
        blob = bucket.blob(file_name)
        blob.upload_from_filename(os.path.join(source_file_folder, file_name))

        print("File {} uploaded to {}.".format(file_name, bucket_name))
