#!/usr/bin/env python

from firestore import update_user_doc


PARTICIPANT_ID_FIELD = "participant_id"
EXPERIMENT_ID_FIELD = "experiment_id"


def catch_qualtrics_requests(request):
    """
    Listens for POST requests from qualtrics survey and updates the
    corresponding firestore documents
    """

    request_args = request.args

    if request_args:
        if PARTICIPANT_ID_FIELD in request_args:
            participant_id = request_args[PARTICIPANT_ID_FIELD]
        if EXPERIMENT_ID_FIELD in request_args:
            experiment_id = request_args[EXPERIMENT_ID_FIELD]

    qualtrics_responses = {
        key: value
        for key, value in request_args.items()
        if key not in [PARTICIPANT_ID_FIELD, EXPERIMENT_ID_FIELD]
    }
    try:
        update_user_doc(participant_id, experiment_id, qualtrics_responses)
    except AttributeError as e:
        print(e)

    return request_args
