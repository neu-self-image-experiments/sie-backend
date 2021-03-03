#!/usr/bin/python3

import subprocess
import os

from server.gcp_cloud_storage import upload_dir, download_file, download_dir
from server.util import mkdir

import bucket_config

USER_SELECTION = "user_selection.csv"


def generate_stimuli(participant_id, file_name):
    """
    Run stimuli generation and save processed images for experiment
    Args:
        participant_id: participant_id extracted from img filename

    Returns:
        None
    """
    downloaded_path = download_file(
        bucket_config.MASKED_IMG_BUCKET,
        f"{participant_id}/{file_name}",
        f"{mkdir(participant_id)}/{file_name}",
    )
    print("downloaded_to:", downloaded_path)

    output_dir = mkdir(participant_id)
    stimuli_dir = mkdir(participant_id, "stimuli")
    r_script_path = f"{os.getcwd()}/rscript/generate_stimuli.R"

    try:
        subprocess.check_call(
            ["Rscript", "--vanilla", r_script_path, output_dir], shell=False
        )
        print("Finished running generate_stimuli.R")
        upload_dir(bucket_config.STIMULI_IMG_BUCKET, stimuli_dir, participant_id)

        # TODO: sends message to pub/sub to notify completion of stimuli genetation

    except subprocess.CalledProcessError as err:
        print("Error running generate_stimuli.R", err)
        raise err


def generate_ci(participant_id, file_name):
    """
    Run ci and upload results to cloud storage
    Args:
        participant_id: participant_id extracted from img filename

    Returns:
        None
    """
    ws_dir = mkdir(participant_id)
    ci_dir = mkdir(participant_id, "ci")

    if not os.path.exists(f"{ws_dir}/stimuli"):
        mkdir(participant_id, "stimuli")
        download_dir(
            bucket_config.STIMULI_IMG_BUCKET, participant_id, f"{ws_dir}/stimuli"
        )
        print(f"downloaded stimuli images to {ws_dir}/stimuli")

    download_file(
        bucket_config.USER_SELECTION_BUCKET,
        f"{participant_id}/{USER_SELECTION}",
        f"{ws_dir}/{USER_SELECTION}",
    )
    print(f"user_selection.csv has been downloaded to {ws_dir}/{USER_SELECTION}")

    try:
        subprocess.check_call(["Rscript", "generate_ci.R", ws_dir], shell=False)
        print("Finished running generate_ci.R")
        upload_dir(bucket_config.CI_IMG_BUCKET, ci_dir, participant_id)
    except subprocess.CalledProcessError as err:
        print("Error running generate_ci.R", err)
        raise err
