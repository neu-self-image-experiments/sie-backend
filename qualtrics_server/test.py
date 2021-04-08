#!/usr/bin/env python
from google.cloud import firestore
from unittest.mock import Mock

from main import catch_qualtrics_requests

from gcp_config import (
    FIRESTORE_USER_COLLECTION,
    FIRESTORE_USER_EXPERIMENT_SUBCOLLECTION,
)

db = firestore.Client()


def test_qualtrics_request():
    """
    Unit test for main.catch_qualtrics_requests
    This test ensures qualtrics data are fetched correctly
    """

    participant_id = "EOiLyNBcz3dMh4uqb1iAxd6vLXm1"
    experiment_id = "4321"
    consent = "yes"

    data = {
        "participant_id": participant_id,
        "experiment_id": experiment_id,
        "consent": consent,
    }

    req = Mock(get_json=Mock(return_value=data), args=data)
    res = catch_qualtrics_requests(req)

    # asserts qualtrics data are fetched correctly
    assert res["participant_id"] == participant_id
    assert res["experiment_id"] == experiment_id
    assert res["consent"] == consent

    # asserts that qualtrics data are stored in firestore
    doc_ref = db.collection(
        f"{FIRESTORE_USER_COLLECTION}/"
        f"{participant_id}/"
        f"{FIRESTORE_USER_EXPERIMENT_SUBCOLLECTION}"
    ).document(experiment_id)

    doc_snapshot = doc_ref.get()
    assert doc_snapshot.exists
    assert doc_snapshot.to_dict()["consent"] == consent
