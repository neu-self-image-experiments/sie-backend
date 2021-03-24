#!/usr/bin/env python

"""
This module contains helper methods to modify firestore documents
"""

from google.cloud import datastore

db = datastore.Client()


def update_user_doc(participant_id, experiment_id, stimuli_status=None):
    """
    Update a firestore user document with corresponding attributes
    Args:
        participant_id: user's uid
        experiment_id: experiment's id
        qualtrics_consent: 'yes' or 'no'
        stimuli_status: 'completed' or None
    Returns:
        None
    """
    user_doc_ref = db.collection("Users").document(participant_id)
    user_doc_ref.set({"sie-stimuli-generation-status": stimuli_status or ""})
