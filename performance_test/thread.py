import time
import os

from google.cloud import storage

'''
    This is the thread class which send post request to the GCP
'''

class thread():


    RAW_BUCKET = "sie-raw-images"
    STIMULI_BUCKET = "sie-stimuli"

    def __init__(self, bucket_name, sleep_time):
        self.participant_id = bucket_name
        self.sleep_time = sleep_time

    def run(self, file_dir, file_name):
        self.upload_image(file_dir, file_name)

        while self.check_finish() is False:
            time.sleep(self.sleep_time)

    def upload_image(self, file_dir, file_name):
        """
            Sends an image to sie-raw bucket
        """

        storage_client = storage.Client()
        bucket = storage_client.bucket(RAW_BUCKET)
        blob = bucket.blob(self.participant_id)
        blob.upload_from_filename(os.path.join(file_dir, file_name))

    def check_finish(self):
        """
        Check if the image generation is finished
        """

        storage_client = storage.Client()
        bucket_name = f"{STIMULI_BUCKET}/{participant_id}"
        return storage.Blob(bucket=bucket_name, 
        name=self.bucket_name + "_20.jpg").exists(storage_client)
