# This cloud function gets triggered by a change in `sie-raw-images` storage bucket
# It picks up the newly created image and sends it to cloud vision API for pre-processing
# Then runs the provided R-script to generate processed images


def trigger_event(event, context):
    """
    Background Cloud Function to be triggered by Cloud Storage.
    This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                        The `data` field contains a description of the event in
                        the Cloud Storage `object` format described here:
                        https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print("Event ID: {}".format(context.event_id))
    print("Event type: {}".format(context.event_type))
    print("Bucket: {}".format(event["bucket"]))
    print("File: {}".format(event["name"]))
    print("Metageneration: {}".format(event["metageneration"]))
    print("Created: {}".format(event["timeCreated"]))
    print("Updated: {}".format(event["updated"]))
