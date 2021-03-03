#!/usr/bin/python3

import subprocess
import os

from server.gcp_cloud_storage import upload_dir, download_file
from server.util import mkdir

import bucket_config


def generate_stimuli(participant_id, file_name):
    """
    Run stimuli generation and save processed images for experiment
    Args:
        participant_id: participant_id extracted from img filename

    Returns:
        None
    """
    downloaded_path = download_file(
        bucket_config.MASKED_IMAGE_BUCKET,
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
    pass
