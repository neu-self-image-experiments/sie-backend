import time
import os

from google.cloud import storage

"""
This is the thread class which send post request to the GCP
"""

RAW_BUCKET = "sie-raw-images"
STIMULI_BUCKET = "sie-stimuli"


class thread:
    def __init__(self, bucket_name, sleep_time, start_queue, end_queue):
        self.participant_id = bucket_name
        self.sleep_time = sleep_time
        self.start_queue = start_queue
        self.end_queue = end_queue

    def run(self, file_dir, file_name):
        start_time = time.time()
        self.start_queue.put(start_time)
        self.upload_image(file_dir, file_name)

        while self.check_finish() is False:
            time.sleep(self.sleep_time)
        end_time = time.time()
        self.end_queue.put(end_time)

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
        bucket_name = f"{STIMULI_BUCKET}/{self.participant_id}"
        return storage.Blob(
            bucket=bucket_name, name=self.bucket_name + "_20.jpg"
        ).exists(storage_client)
