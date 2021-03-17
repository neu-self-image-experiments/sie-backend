from flask import escape

PARTICIPANT_ID_FIELD = "participant_id"
EXPERIMENT_ID_FIELD = "experiment_id"
RESPONSE_FIELD = "response"


def catch_qualtrics_requests(request):
    request_args = request.args

    participant_id = ""
    experiment_id = ""
    response = ""

    print(request_args)
    if request_args:
        if PARTICIPANT_ID_FIELD in request_args:
            participant_id = request_args[PARTICIPANT_ID_FIELD]
        if EXPERIMENT_ID_FIELD in request_args:
            experiment_id = request_args[EXPERIMENT_ID_FIELD]
        if RESPONSE_FIELD in request_args:
            response = request_args[RESPONSE_FIELD]

    print(participant_id)
    print(experiment_id)
    print(response)

    return "Hello {}!".format(escape(participant_id))
