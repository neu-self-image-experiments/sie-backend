#!/usr/bin/env python

"""
This module contains helper methods to modify firestore documents
"""

from google.cloud import firestore

FIRESTORE_USER_COLLECTION = "Users"
db = firestore.Client()


def update_user_doc(participant_id, experiment_id, error_message):
    """
    Update a firestore user document with corresponding attributes.
    The purpose of this function is to let the frontend team know
    about any InvalidFaceImage exception messages.
    Args:
        participant_id: user's uid
        experiment_id: experiment's id
        error_message: 'error message'
    Returns:
        None
    """
    user_doc_ref = db.collection(FIRESTORE_USER_COLLECTION).document(participant_id)
    user_doc_ref.update({"sie_stimuli_generation_status": error_message})
