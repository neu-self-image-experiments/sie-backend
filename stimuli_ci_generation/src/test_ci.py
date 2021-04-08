import os
import time
import gcp_config
from google.cloud import storage
from server.gcp_cloud_storage import upload_file

# NUM_STIMULI_FILES =
# (number of images per selection) * (number of selections)
# + number of rdata file
NUM_STIMULI_FILES = 2 * 200 + 1


def test_stimuli_ci(test_asset_path="./test_asset"):
    storage_client = storage.Client()

    # delete cached test files in bucket
    for identifier in os.listdir(test_asset_path):
        path = test_asset_path + identifier
        if os.path.isdir(path):
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

    start_time = time.time()

    for identifier in os.listdir(test_asset_path):
        path = test_asset_path + identifier
        if os.path.isdir(path):
            test_start_time = time.time()

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
                time.sleep(0.1)

            upload_file(
                gcp_config.MASKED_IMG_BUCKET,
                test_asset_path + identifier + "user_selection.csv",
                identifier + "user_selection.csv",
            )
            ci_results = list(
                storage_client.list_blobs(gcp_config.CI_IMG_BUCKET, prefix=identifier)
            )
            while len(ci_results) == 0:
                time.sleep(0.1)

            print(
                f"test for {identifier} finished in {time.time() - test_start_time} ms."
            )

    print(f"all tests finished in {time.time() - start_time} ms.")
