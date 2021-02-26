from flask import Flask
from flask import request
from google.cloud import storage
import subprocess
import glob
import os
import shutil
import sys
import errno

SELFIE_NAME = "MNES.jpg"
USER_SELECTION = "user_selection.csv"

app = Flask(__name__)


# upload a file to google cloud storage
def upload_file(file_name, bucket_name):
    upload_destination = file_name[(len(bucket_name) + 1) :]
    print("upload destination: {}".format(upload_destination), file=sys.stderr)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(upload_destination)
    blob.upload_from_filename(file_name)
    return "File {} uploaded to {}.".format(file_name, upload_destination)


# download a file from google cloud storage
def download_file(dest_dir, file_name, bucket_name):
    destination = dest_dir
    print("saving file to {}".format(destination), file=sys.stderr)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    destination_uri = "{}/{}".format(dest_dir, blob.name)
    print("saving blob to {}".format(destination_uri), file=sys.stderr)
    blob.download_to_filename(destination_uri)
    print(f"Blob {file_name} dwonloaded to {destination_uri}", file=sys.stderr)
    return "Blob {} downloaded to {}.".format(file_name, destination)


# download a folder from google cloud storage
def download_folder(folder_name, bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name)  # Get list of files
    create_bucket_folder(bucket_name + "/" + folder_name)
    for blob in blobs:
        blob.download_to_filename(bucket_name + "/" + blob.name)


def clean_local_dir(directory):
    shutil.rmtree(directory)


def create_bucket_folder(bucket_name):
    try:
        os.makedirs(bucket_name)
    except OSError as exc:
        print("Creation of the directory %s failed" % bucket_name)
        print(f"Creation of the directory {bucket_name} failed", file=sys.stderr)
        if exc.errno != errno.EEXIST:
            raise
    else:
        print(f"Successfully created the directory {bucket_name}")


@app.route("/stimuli", methods=["POST"])
def generate_stimuli():
    bucket_name = request.args.get("bucket")
    file_name = request.args.get("file")
    ppt_id = request.args.get("pptId")
    dest_dir = bucket_name + "/" + ppt_id
    create_bucket_folder(dest_dir)
    result = download_file(bucket_name, file_name, bucket_name)
    print(result, file=sys.stderr)

    # subprocess.check_call(
    #   ['Rscript', 'generate_stimuli.R', dest_dir], shell=False
    # )
    subprocess.run(["Rscript", "generate_stimuli.R", dest_dir], shell=False)
    files = glob.glob(dest_dir + "/stimuli/*.jpg")
    uploaded = "item"
    for f in files:
        uploaded += upload_file(f, bucket_name)
    r_data = glob.glob(dest_dir + "/stimuli/*.Rdata")[0]
    upload_file(r_data, bucket_name)
    clean_local_dir(bucket_name)
    return "stimuli " + uploaded + "uploaded"


@app.route("/ci", methods=["POST"])
def generate_ci():
    bucket_name = request.args.get("bucket")
    create_bucket_folder(bucket_name)
    download_file(USER_SELECTION, bucket_name)
    download_folder("stimuli", bucket_name)
    subprocess.check_call(["Rscript", "generate_ci.R", bucket_name], shell=False)
    files = glob.glob(bucket_name + "/cis/*.jpg")
    uploaded = "emtpy item"
    for f in files:
        uploaded = upload_file(f, bucket_name)
    clean_local_dir(bucket_name)
    return "classification image " + uploaded


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        threaded=True,
    )
