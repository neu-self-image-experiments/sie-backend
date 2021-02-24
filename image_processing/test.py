import os
import main
from google.cloud import storage


def test_upload_processed_images(request):
    request_args = request.args

    # try:
    bucket_name = request_args["bucket_name"]
    source_file_folder = request_args["source_file_folder"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    main.upload_processed_images(bucket_name, source_file_folder)

    for file_name in os.listdir(source_file_folder):
        blob = bucket.blob(file_name)
        if not blob.exist():
            return "Test fail, upload unsuccessful"
    
    return "Test passed"
    # except Exception:
    #     return "Exception is thrown, check 
    #       the parameter that are passed into the function"
    # finally:
    #     return "Test passed"