#!/usr/bin/python3

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
    print(f"Downloading {source_blob_name} to {destination_file_name}")

    return destination_file_name


def download_dir(bucket_name, source_dir, destination_dir):
    """Downloads the specified folder from cloud storage
    Args:
        bucket_name: bucket to download from
        source_dir: folder to download
        destination_dir: where to download to

    Returns:
        Local path to downloaded image
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=source_dir)  # Get list of files
    print(f"Downloading {source_dir} to {destination_dir}")
    for blob in blobs:
        blob.download_to_filename(f"{destination_dir}/{blob.name}")

    return destination_dir


def upload_file(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket.

    Args:
        bucket_name: Name of the bucket to upload file
        source_file_name: path of file to upload
    """

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return destination_blob_name


def upload_dir(bucket_name, source_file_folder, file_prefix):
    """Uploads images from a dir to the bucket.
    Args:
        bucket_name: bucket to upload files to
        source_file_folder: Path to the folder to be uploaded
        file_prefix: prefix to file identifier in cloud storage bucket
    Returns:
        None
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    print(f"Uploading files from {source_file_folder} to {bucket_name}")
    for file_name in os.listdir(source_file_folder):
        local_path = os.path.join(source_file_folder, file_name)
        bucket_file_id = f"{file_prefix}/{file_name}"
        blob = bucket.blob(bucket_file_id)
        blob.upload_from_filename(local_path)
