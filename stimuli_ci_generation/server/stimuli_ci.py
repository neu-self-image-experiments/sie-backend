import subprocess

from stimuli_ci_generation.gcloud_services import upload_files, download_file
from stimuli_ci_generation.util import mkdir


RAW_IMG_BUCKET = "sie-raw-images"
STIMULI_BUCKET = "sie-stimuli"
CI_BUCKET = "sie-classified-images"
USER_SELECTION_BUCKET = "sie-results"


def generate_stimuli(img_file_path, participant_id):
    # run stimuli generation and save processed images for experiment

    output_dir = mkdir(participant_id)
    subprocess.run(["Rscript", "generate_stimuli.R", output_dir], shell=False)

    stimuli_dir = f"{output_dir}/stimuli"
    bucket_name = f"{STIMULI_BUCKET}/{participant_id}"
    upload_files(bucket_name, stimuli_dir)


def generate_ci(participant_id):
    output_dir = mkdir(participant_id)
    # download user_selection.csv to be used in generate_ci.R
    download_file(
        f"{USER_SELECTION_BUCKET}/{participant_id}", "user_selection.csv", output_dir
    )
    subprocess.check_call(["Rscript", "generate_ci.R", output_dir], shell=False)

    ci_dir = f"{output_dir}/cis"
    ci_bucket = f"{CI_BUCKET}/{participant_id}"

    upload_files(ci_bucket, ci_dir)
