#!/usr/bin/python3

from flask import Flask
from flask import request

import os
import base64
import json
import time

from gcloud_services.cloud_storage import download_file

from server.stimuli_ci import generate_stimuli
from util import mkdir

MASKED_IMAGE_BUCKET = "sie-masked-images"


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

    start = time.time()
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

        file_identifier = data["name"]  # should be participant_id/neutral.jpg
        print("file_identifier:", file_identifier)
        participant_id, file_name = file_identifier.split("/")
        downloaded_path = download_file(
            MASKED_IMAGE_BUCKET, file_identifier, f"{mkdir(participant_id)}/{file_name}"
        )
        print("downloaded_to:", downloaded_path)

        end_download = time.time()
        print("Trigger and download latency:", end_download - start)

        try:
            generate_stimuli(participant_id)
        except Exception:
            return ("Failed to generate stimuli", 500)

        print("Stimuli generation:", time.time() - end_download)

        return ("Processing stimuli...", 204)

    return ("", 500)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally.
    # Gunicorn is used to run the application on Cloud Run.
    # See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
