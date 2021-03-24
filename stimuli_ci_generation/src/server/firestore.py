#!/usr/bin/env python

"""
This module contains helper methods to modify firestore documents
"""

from google.cloud import firestore
from gcp_config import FIRESTORE_USER_COLLECTION

db = firestore.Client()


def update_user_doc(participant_id, experiment_id, stimuli_status=None):
    """
    Update a firestore user document with corresponding attributes
    Args:
        participant_id: user's uid
        experiment_id: experiment's id
        stimuli_status: 'completed' or None
    Returns:
        None
    """
    user_doc_ref = db.collection(FIRESTORE_USER_COLLECTION).document(participant_id)
    user_doc_ref.update({"sie_stimuli_generation_status": stimuli_status or ""})
