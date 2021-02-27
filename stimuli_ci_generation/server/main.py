from flask import Flask
from flask import request

import os

app = Flask(__name__)


# [START eventarc_gcs_handler]
@app.route("/", methods=["POST"])
def storage_trigger_event():
    """
    Listens for storage event triggers and run image processing
    """

    bucket = request.headers.get("ce-subject")
    print(f"Detected change in Cloud Storage bucket: {bucket}")
    # TODO(qhoang)
    # extract file_name and participant_id
    # download image file
    # run image processing from stimuli_ci.py

    return (f"Detected change in Cloud Storage bucket: {bucket}", 200)


# [END eventarc_gcs_handler]


# [START eventarc_gcs_server]
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END eventarc_gcs_server]
