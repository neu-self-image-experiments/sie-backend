#!/usr/bin/python3

from flask import Flask
from flask import request

import os
import base64
import json

from server.stimuli_ci import generate_stimuli, generate_ci

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

        file_identifier = data["name"]  # should be participant_id/neutral.jpg
        print("file_identifier:", file_identifier)
        participant_id, file_name = file_identifier.split("/")
        file_type = file_name.split(".")[-1]

        if file_type.lower() == "csv":
            try:
                generate_ci(participant_id, file_name)
                return ("Generating ci images...", 202)
            except Exception:
                return ("Failed to generate ci", 204)
        else:
            try:
                generate_stimuli(participant_id, file_name)
                return ("Generating stimuli images...", 202)
            except Exception as e:
                print(e)
                return ("Failed to generate stimuli", 204)

    return ("data missing in pub/sub message", 500)


@app.route("/status", methods=["GET"])
def status():
    return ("OK", 200)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally.
    # Gunicorn is used to run the application on Cloud Run.
    # See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
