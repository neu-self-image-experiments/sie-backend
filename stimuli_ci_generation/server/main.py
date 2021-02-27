from flask import Flask
from flask import request

import os
import base64
import json

app = Flask(__name__)


# [START eventarc_gcs_handler]
@app.route("/", methods=["POST"])
def index():
    """
    Listens for message from storage trigger and run image processing
    """

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

    name = "World"
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

        print(data)
        print(data["name"])
        print(data["bucket"])    

    return ("", 204)
# [END eventarc_gcs_handler]


# [START eventarc_gcs_server]
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END eventarc_gcs_server]
