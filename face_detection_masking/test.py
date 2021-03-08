import os
import main
from google.cloud import storage


def test_upload_processed_images(request):
    """Unit test for the function upload_processed_images.
    Args:
        request = "HTTP request"

    Returns:
        String if all assertion passed;
    """
    # print(request)
    request_args = request.args
    bucket_name = request_args["bucket_name"]
    source_file_folder = request_args["source_file_folder"]

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
