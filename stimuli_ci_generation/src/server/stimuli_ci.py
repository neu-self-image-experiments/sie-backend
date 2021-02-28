#!/usr/bin/python

import subprocess

from gcloud_services.cloud_storage import upload_files, download_file
from util import mkdir


STIMULI_BUCKET = "sie-stimuli"
CI_BUCKET = "sie-classified-images"
USER_SELECTION_BUCKET = "sie-results"


def generate_stimuli(img_file_path, participant_id):
    """
    Run stimuli generation and save processed images for experiment
    Args:
        img_file_path: downloaded image
        participant_id: participant_id extracted from img filename

    Returns:
        None
    """

    output_dir = mkdir(participant_id)
    stimuli_dir = mkdir(participant_id, "stimuli")

    try:
        subprocess.check_call(["Rscript", "generate_stimuli.R", output_dir], shell=True)
        bucket_name = f"{STIMULI_BUCKET}/{participant_id}"
        upload_files(bucket_name, stimuli_dir)
    except subprocess.CalledProcessError as err:
        print("Error running generate_stimuli.R")
        raise err


def generate_ci(participant_id):
    """
    Run ci and upload results to cloud storage
    Args:
        participant_id: participant_id extracted from img filename

    Returns:
        None
    """

    output_dir = mkdir(participant_id)
    ci_dir = mkdir(participant_id, "cis")
    ci_bucket = f"{CI_BUCKET}/{participant_id}"
    # download user_selection.csv to be used in generate_ci.R
    download_file(
        f"{USER_SELECTION_BUCKET}/{participant_id}", "user_selection.csv", output_dir
    )

    try:
        subprocess.check_call(["Rscript", "generate_ci.R", output_dir], shell=True)
        upload_files(ci_bucket, ci_dir)
    except subprocess.CalledProcessError as err:
        print("Error running generate_ci.R")
        raise err
