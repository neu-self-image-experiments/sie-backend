import time
import os

from google.cloud import storage

"""
This is the thread class which send post request to the GCP
"""

RAW_BUCKET = "sie-raw-images"
STIMULI_BUCKET = "sie-stimuli-images"


class thread:
    def __init__(self, participant_id, sleep_time, start_queue, end_queue, threshold):
        self.participant_id = participant_id
        self.sleep_time = sleep_time
        self.start_queue = start_queue
        self.end_queue = end_queue
        self.threshold = "0" + str(threshold) if threshold < 100 else str(threshold)
        self.blob_name = f"rcic_mnes_1_00{self.threshold}_ori.jpg"

    def run(self, file_dir, file_name):
        start_time = time.time()
        self.start_queue.put(start_time)
        print(f"Start uploading image: {file_name}")
        self.upload_image(file_dir, file_name)
        print(f"Finish uploading image: {file_name}")

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
        blob = bucket.blob(file_name)
        blob.upload_from_filename(os.path.join(file_dir, file_name))

    def check_finish(self):
        """
        Check if the image generation is finished
        """

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(STIMULI_BUCKET)
        bucket_dir = f"0000{self.participant_id}" if self.participant_id < 10 else f"000{self.participant_id}"
        print(f"Checking on {bucket_dir}/{self.blob_name}")
        return bucket.get_blob(f"{bucket_dir}/{self.blob_name}") != None
