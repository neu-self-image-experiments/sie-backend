from flask import escape
from firestore import update_user_doc


PARTICIPANT_ID_FIELD = "participant_id"
EXPERIMENT_ID_FIELD = "experiment_id"


def catch_qualtrics_requests(request):
    request_args = request.args

    participant_id = ""
    experiment_id = ""

    if request_args:
        if PARTICIPANT_ID_FIELD in request_args:
            participant_id = request_args[PARTICIPANT_ID_FIELD]
        if EXPERIMENT_ID_FIELD in request_args:
            experiment_id = request_args[EXPERIMENT_ID_FIELD]

    qualtrics_responses = {
        key: value
        for key, value in request_args.items()
        if key not in ["participant_id", "experiment_id"]
    }
    try:
        update_user_doc(participant_id, experiment_id, qualtrics_responses)
    except Exception as e:
        print(e)

    return "Hello {}!".format(escape(participant_id))
