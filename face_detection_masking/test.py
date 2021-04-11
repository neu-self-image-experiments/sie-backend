import os
import main
from google.cloud import storage


def test_upload_processed_images():
    """Unit test for the function upload_processed_images.

    Returns:
        String if all assertion passed;
    """
    bucket_name = "sie-raw-images"
    source_file_folder = "test_assets/test_upload_images/"

    # Create connection to the storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    main.upload_processed_images(bucket_name, source_file_folder)

    # Iterate through the files inside the folder
    for file_name in os.listdir(source_file_folder):
        # Aessert if the blob exist in the bucket
        assert (
            storage.Blob(bucket=bucket, name=file_name).exists(storage_client) is True
        )
        # You can use print to see if the assertion is correct

    # Make a falsy test to ensure that it returns false
    assert (
        storage.Blob(bucket=bucket, name="Falsy_test").exists(storage_client) is False
    )

    # If all assertions passed, then return test pass
    return "Test passed"


def test_upload_image():
    """Unit test for the function upload_images.

    Returns:
        String if all assertion passed;
    """
    bucket_name = "sie-face-detection-testing-assets"
    source_file_name = "test_assets/test_upload_images/fakeID-011.jpg"
    destination_blob_name = "fakeID-011"

    # Create connection to the storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    main.upload_image(bucket_name, source_file_name, destination_blob_name)

    # Aessert if the blob exist in the bucket
    assert (
        storage.Blob(bucket=bucket, name=destination_blob_name).exists(storage_client)
        is True
    )

    # Make a falsy test to ensure that it returns false
    assert (
        storage.Blob(bucket=bucket, name="Falsy_test").exists(storage_client) is False
    )

    # If all assertions passed, then return test pass
    return "Test passed"


def test_download_image():
    """Unit test for the function download_image.

    Returns:
        String if all assertion passed;
    """
    bucket_name = "sie-face-detection-testing-assets"
    source_blob_name = "face_neutral.jpg"
    destination_file_name = "test_assets/test_upload_images/test_download.jpg"

    main.download_image(bucket_name, source_blob_name, destination_file_name)

    assert os.path.isfile(destination_file_name) is True

    os.remove(destination_file_name)

    return "Test passed"
