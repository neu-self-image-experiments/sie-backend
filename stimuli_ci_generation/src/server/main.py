#!/usr/bin/env python

from flask import Flask
from flask import request

import os
import base64
import json

from gcloud_services.cloud_storage import download_file

# from server.stimuli_ci import generate_stimuli
from util import mkdir

RAW_IMG_BUCKET = "sie-raw-images"


app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # Decode the Pub/Sub message.
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            data = json.loads(base64.b64decode(pubsub_message["data"]).decode())

        except Exception as e:
            msg = (
                "Invalid Pub/Sub message: "
                "data property is not valid base64 encoded JSON"
            )
            print(f"error: {e}")
            return f"Bad Request: {msg}", 400

        # Validate the message is a Cloud Storage event.
        if not data["name"] or not data["bucket"]:
            msg = (
                "Invalid Cloud Storage notification: "
                "expected name and bucket properties"
            )
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        file_name = data["name"]  # file_name should be participant_id.jpg
        print("file_name:", file_name)
        participant_id = file_name.split(".")[0]
        downloaded_path = download_file(
            RAW_IMG_BUCKET, file_name, f"{mkdir(participant_id)}/{file_name}"
        )
        print("downloaded_to:", downloaded_path)
        # generate_stimuli(downloaded_path, participant_id)

        return ("Processing stimuli...", 204)

    return ("", 500)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally.
    # Gunicorn is used to run the application on Cloud Run.
    # See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
