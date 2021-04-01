#!/usr/bin/env python

"""
This module contains helper methods to modify firestore documents
"""


from google.cloud import firestore
from gcp_config import FIRESTORE_USER_COLLECTION, FIRESTORE_USER_EXPERIMENT_COLLECTION

db = firestore.Client()


def update_user_doc(participant_id: str, experiment_id: str, attributes: dict):
    """
    Update a firestore user document with corresponding attributes
    Args:
        participant_id: user's uid
        experiment_id: experiment's id
        qualtrics_responses: dict of qualtrics responses
    Returns:
        None
    """

    user_doc_ref = db.collection(
        f"""
        {FIRESTORE_USER_COLLECTION}/
        {participant_id}/
        {FIRESTORE_USER_EXPERIMENT_COLLECTION}"""
    ).document(experiment_id)

    if attributes:
        # update if exists, otherwise create a new doc
        user_doc_ref.set(attributes, merge=True)
