#!/usr/bin/env python

"""
This module contains helper methods to modify firestore documents
"""

from google.cloud import firestore

FIRESTORE_USER_COLLECTION = "Users"
FIRESTORE_USER_EXPERIMENT_SUBCOLLECTION = "Experiments"
db = firestore.Client()


def update_user_doc(participant_id: str, experiment_id: str, attributes: dict):
    """
    Update a firestore user document with corresponding attributes.
    The purpose of this function is to let the frontend team know
    about any InvalidFaceImage exception messages.
    Args:
        participant_id: user's uid
        experiment_id: experiment's id
        attributes: dict of doc attributes to update (containing error message)
    Returns:
        None
    """

    user_doc_ref = db.collection(FIRESTORE_USER_COLLECTION).document(participant_id)
    if not user_doc_ref.get().exists:
        raise AttributeError("Participant id does not exists.")

    doc_ref = db.collection(
        f"{FIRESTORE_USER_COLLECTION}/"
        f"{participant_id}/"
        f"{FIRESTORE_USER_EXPERIMENT_SUBCOLLECTION}"
    ).document(experiment_id)

    if attributes:
        # update if exists, otherwise create a new doc
        doc_ref.set(attributes, merge=True)
