import os
import main
import gcp_config
from google.cloud import storage
from server.gcp_cloud_storage import upload_dir

# NUM_STIMULI_FILES = (number of images per selection) * (number of selections) + number of rdata file
NUM_STIMULI_FILES = 2 * 200 + 1


def test_stimuli_ci(test_asset_path="./test_asset"):
    storage_client = storage.Client()
    start_time = time.time()

    for identifier in os.listdir(test_asset_path):
        path = test_asset_path + identifier
        if os.path.isdir(path):
            test_start_time = time.time()

            # delete cached test files in bucket
            for blob in storage_client.list_blobs(
                gcp_config.MASKED_IMG_BUCKET, prefix=identifier
            ):
                blob.delete()
            for blob in storage_client.list_blobs(
                gcp_config.STIMULI_IMG_BUCKET, prefix=identifier
            ):
                blob.delete()
            for blob in storage_client.list_blobs(
                gcp_config.USER_SELECTION_BUCKET, prefix=identifier
            ):
                blob.delete()
            for blob in storage_client.list_blobs(
                gcp_config.CI_IMG_BUCKET, prefix=identifier
            ):
                blob.delete()

            upload_file(
                gcp_config.MASKED_IMG_BUCKET,
                test_asset_path + identifier + "masked.jpg",
                identifier + "neutral.jpg",
            )
            stimuli_results = list(
                storage_client.list_blobs(
                    gcp_config.STIMULI_IMG_BUCKET, prefix=identifier
                )
            )
            while len(stimuli_results) < NUM_STIMULI_FILES:
                sleep(100)

            upload_file(
                gcp_config.MASKED_IMG_BUCKET,
                test_asset_path + identifier + "user_selection.csv",
                identifier + "user_selection.csv",
            )
            ci_results = list(
                storage_client.list_blobs(gcp_config.CI_IMG_BUCKET, prefix=identifier)
            )
            while len(stimuli_results) == 0:
                sleep(100)

            print(
                f"test for {identifier} finished in {time.time() - test_start_time} ms."
            )

    print(f"all tests finished in {time.time() - start_time} ms.")
