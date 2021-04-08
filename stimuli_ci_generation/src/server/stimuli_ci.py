#!/usr/bin/env python

import subprocess
import os

from server.gcp_cloud_storage import upload_dir, download_file, download_dir
from server.util import mkdir

import gcp_config

USER_SELECTION = "user_selection.csv"


def generate_stimuli(identifier, file_name):
    """
    Run stimuli generation and save processed images for experiment
    Args:
        identifier: participant_id-experiment_id extracted from img filename

    Returns:
        None
    """
    downloaded_path = download_file(
        gcp_config.MASKED_IMG_BUCKET,
        f"{identifier}/{file_name}",
        f"{mkdir(identifier)}/{file_name}",
    )
    print("downloaded_to:", downloaded_path)

    output_dir = mkdir(identifier)
    stimuli_dir = mkdir(identifier, "stimuli")
    r_script_path = f"{os.getcwd()}/rscript/generate_stimuli.R"

    try:
        subprocess.check_call(
            ["Rscript", "--vanilla", r_script_path, output_dir], shell=False
        )
        print("Finished running generate_stimuli.R")
        upload_dir(gcp_config.STIMULI_IMG_BUCKET, stimuli_dir, identifier)
    except subprocess.CalledProcessError as err:
        print("Error running generate_stimuli.R", err)
        raise err


def generate_ci(identifier, file_name):
    """
    Run ci and upload results to cloud storage
    Args:
        identifier: participant_id-experiment_id extracted from img filename
        file_name: file name of the user selection file
    Returns:
        None
    """
    ws_dir = mkdir(identifier)
    ci_dir = mkdir(identifier, "ci")
    r_script_path = f"{os.getcwd()}/rscript/generate_ci.R"

    if not os.path.exists(f"{ws_dir}/stimuli"):
        stimuli_dir = mkdir(identifier, "stimuli")
        download_dir(gcp_config.STIMULI_IMG_BUCKET, identifier, f"{stimuli_dir}")
        print(f"downloaded stimuli images to {ws_dir}/stimuli")

    print(f"stimuli has {len(os.listdir(f'{ws_dir}/stimuli'))} files.")
    if len(os.listdir(f"{ws_dir}/stimuli")) == 0:
        raise Exception("CI could not be generated due to empty stimuli directory.")

    if file_name != USER_SELECTION:
        raise Exception(f"name of user selections file does not match {USER_SELECTION}")
    download_file(
        gcp_config.USER_SELECTION_BUCKET,
        f"{identifier}/{file_name}",
        f"{ws_dir}/{USER_SELECTION}",
    )
    print(f"user_selection.csv has been downloaded to {ws_dir}/{file_name}")

    try:
        print("started running generate_ci.R")
        subprocess.check_call(["Rscript", r_script_path, ws_dir], shell=False)
        print("Finished running generate_ci.R")
        upload_dir(gcp_config.CI_IMG_BUCKET, ci_dir, identifier)
    except subprocess.CalledProcessError as err:
        print("Error running generate_ci.R", err)
        raise err
