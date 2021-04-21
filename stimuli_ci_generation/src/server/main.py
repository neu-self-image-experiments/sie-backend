#!/usr/bin/env python

from flask import Flask
from flask import request

import os
import base64
import json

from server.firestore import update_user_doc
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

        file_identifier = data[
            "name"
        ]  # should be participant_id-experiment_id/neutral.jpg
        print("file_identifier:", file_identifier)
        file_identifier_parts = file_identifier.split("/")
        if len(file_identifier_parts) > 2:
            print(f"invalid file identifier {file_identifier}")
            return f"Invalid file identifier {file_identifier}", 204
        identifier, file_name = file_identifier_parts
        file_type = file_name.split(".")[-1]

        try:
            participant_id, experiment_id = identifier.split("-")
        except ValueError:
            return f"Failed to parse identifer {identifier}", 204

        # returning 2xx here to ack pub/sub msg
        # or else storage trigger will keep retrying
        if file_type.lower() == "csv":
            # this is for after participants finishes with their img selections
            try:
                generate_ci(identifier, file_name)
                update_user_doc(
                    participant_id,
                    experiment_id,
                    {"sie_ci_generation_status": "completed"},
                )
                return ("Generating ci images...", 202)
            except Exception as e:
                print(e)
                update_user_doc(
                    participant_id,
                    experiment_id,
                    {"sie_ci_generation_status": "incomplet"},
                )
                return ("Failed to generate ci", 204)
        else:
            # this is for after participants upload their images
            # and the images pass facial detection
            try:
                generate_stimuli(identifier, file_name)
                update_user_doc(
                    participant_id,
                    experiment_id,
                    {"sie_stimuli_generation_status": "completed"},
                )

                return ("Stimuli generated", 202)
            except Exception as e:
                print(e)
                update_user_doc(
                    participant_id,
                    experiment_id,
                    {"sie_stimuli_generation_status": "incomplete"},
                )
                return ("Failed to generate stimuli", 204)

    print("data missing in pub/sub message")
    return ("data missing in pub/sub message", 204)


@app.route("/status", methods=["GET"])
def status():
    return ("OK", 200)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally.
    # Gunicorn is used to run the application on Cloud Run.
    # See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
