import time
import os

from google.cloud import storage

RAW_BUCKET = "sie-raw-images"
STIMULI_BUCKET = "sie-stimuli-images"


class PipelineRunnable:
    """
    This is the thread class which uploads image to GCP and record the
    finishing time for the pipeline.
    """

    def __init__(self, participant_id, sleep_time, threshold):
        """
        The function initializes a thread object.
        Args:
            participant_id: The id of the participant
            sleep_time: Sleeping time between request to
                        check whether image processing is finished.
            start_queue: A queue to store the starting time for each thread.
            end_queue: A queue to storee the ending time for each thread.
            threshold: A threshold to determine whether image processing is finished.
        Returns:
            None;
        """
        self.participant_id = participant_id
        self.sleep_time = sleep_time
        if threshold < 10:
            self.threshold = "00" + str(threshold)
        elif threshold < 100:
            self.threshold = "0" + str(threshold)
        else:
            self.threshold = str(threshold)
        self.blob_name = f"rcic_mnes_1_00{self.threshold}_ori.jpg"

    def run(self, file_dir, file_name):
        """
        The function runs a thread including steps like upload image to the
        sie-raw-image bucket and check if certain image is generated in the
        sie-stimuli-image bucket.
        Args:
            file_dir: The local directory of the images location.
            file_name: The name of the image file.
        Returns:
            None;
        """
        start_time = time.time()
        print(f"Start uploading image: {file_name}")
        self.upload_image(file_dir, file_name)
        print(f"Finish uploading image: {file_name}")

        while not self.check_finish():
            time.sleep(self.sleep_time)

        end_time = time.time()
        return start_time, end_time

    def upload_image(self, file_dir, file_name):
        """
        The function uploads an image to sie-raw bucket.
        Args:
            file_dir: The local directory of the images location.
            file_name: The name of the image file.
        Returns:
            None;
        """

        storage_client = storage.Client()
        bucket = storage_client.bucket(RAW_BUCKET)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(os.path.join(file_dir, file_name))

    def check_finish(self):
        """
        The function checks if the image generation is finished.
        Args:
            None;
        Returns:
            A boolean value indicating whether the
            image generation is finished;
        """

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(STIMULI_BUCKET)
        bucket_dir = (
            f"0000{self.participant_id}"
            if self.participant_id < 10
            else f"000{self.participant_id}"
        )
        print(f"Checking on {bucket_dir}/{self.blob_name}")
        return bucket.get_blob(f"{bucket_dir}/{self.blob_name}") is not None
