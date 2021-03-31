import datetime
import os
import requests
import subprocess
import constants

from google.cloud import storage
from urllib3.util import Retry


# I am using the credentials of service account cs6510-sie-backend-testing@cs6510-spr2021.iam.gserviceaccount.com.

# Problems I am having right now:
# 1. source venv/bin/activate
# 2. Export the credentials of service account cs6510-sie-backend-testing@cs6510-spr2021.iam.gserviceaccount.com.
# 3. Run the test using 'pytest integ_test.py', I got error like
# requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

# Alternatively, I tried
# 1. source venv/bin/activate
# 2. Export the credentials of service account cs6510-sie-backend-testing@cs6510-spr2021.iam.gserviceaccount.com.
# 3. Run "functions-framework --target=trigger_detect_and_mask --port=9898 --signature-type=event"
# 4. Run "pytest integ_test.py" in another terminal (comment out the process part for functions-framework), I am still getting the same error.

# However, I tried
# 1. source venv/bin/activate
# 2. Don't export the service account credentials
# 3. Run "functions-framework --target=trigger_detect_and_mask --port=9898 --signature-type=event"
# 4. In another terminal, export the service account credentials, and then run "pytest integ_test.py"
# 5. The request did get to trigger_detect_and_mask (I could see debug logs showing up for request parameters), but I am getting
# error in "results = face_detection(uri)"
# google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials.
# Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials and re-run the application. For more information, please see https://cloud.google.com/docs/authentication/getting-started


# So, if I export the credentials when running functions-framework, requests from the integ test just could NOT hit
# the localhost:9898. If I don't export the credentials, the requests could hit localhost:9898, but trigger_detect_and_mask
# fails because of credentials could not be determined.
# Currently blocked as I couldn't figure out the cause of the problem.

def test_trigger_detect_and_mask():
    input_bucket_name = "integ_test_sie-raw-images"
    output_bucket_name = "sie-masked-images"

    # The test image has already been uploaded to the input bucket
    image_name = "integ-test-human.jpeg"

    # Each running framework instance needs a unique port
    port = 9898

    create_timestamp = datetime.datetime.now().isoformat()
    storage_message = {
        'data': {
            'name': image_name,
            'bucket': input_bucket_name,
            'metageneration': '1',
            'timeCreated': create_timestamp,
            'updated': create_timestamp
        }
    }

    # TODO - comment out to run functions-framework separately
    # Run functions-framework instead manually
    # process = subprocess.Popen(
    #     [
    #         'functions-framework',
    #         '--target', 'trigger_detect_and_mask',
    #         '--signature-type', 'event',
    #         '--port', str(port)
    #     ],
    #     cwd=os.path.dirname(__file__),
    #     stdout=subprocess.PIPE
    # )

    # Send HTTP request simulating Pub/Sub message
    # (GCF translates Pub/Sub messages to HTTP requests internally)
    url = f'http://localhost:{port}/'

    retry_policy = Retry(total=6, backoff_factor=1)
    retry_adapter = requests.adapters.HTTPAdapter(max_retries=retry_policy)

    session = requests.Session()
    session.mount(url, retry_adapter)

    response = session.post(url, json=storage_message)

    assert response.status_code == 200

    # Stop the functions framework process
    # process.kill()
    # process.wait()
    # out, err = process.communicate()
    #
    # print(out, err, response.content)
    # assert 'Face detected and masked successfully!' in str(out)

    # # Validate images in the output bucket
    participant_id = os.path.splitext(image_name)[0]
    output_file_name = f"{participant_id}/{constants.PROCESSED_IMAGE}"
    assert validate_file_in_bucket(output_bucket_name, output_file_name)

    # Clean up buckets
    clean_up_bucket(output_bucket_name, participant_id)


def set_up_bucket(bucket_name):
    """
    The function creates a bucket.
    Args:
        bucket_name: the bucket to create
    returns:
        google.cloud.storage.bucket.Bucket
            The newly created bucket.
    """
    storage_client = storage.Client.from_service_account_json('service_account.json')

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )

    return new_bucket


def clean_up_bucket(bucket_name, folder_name):
    """
    The function delete both objects in the specified bucket and the bucket itself.
    Args:
        bucket_name: the bucket to delete
    returns:
        none
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete(force=True)

        blobs = bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            blob.delete()

        print(
            "Deleted objects in folder {} under bucket {} successfully".format(
                folder_name, bucket_name
            )
        )
    except ValueError as error:
        print(
            "Failed to delete bucket {}: {}".format(
                bucket_name, str(error)
            )
        )


def validate_file_in_bucket(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return storage.Blob(bucket=bucket, name=file_name).exists(storage_client)
