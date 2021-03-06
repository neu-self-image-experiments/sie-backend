#!/usr/bin/python3

"""
    Project level config
"""
PROJECT_ID = "cs6510-spr2021"

"""
    Bucket names configured on gcp cloud storage for this project
"""
RAW_IMG_BUCKET = "sie-raw-images"
MASKED_IMG_BUCKET = "sie-masked-images"
STIMULI_IMG_BUCKET = "sie-stimuli-images"
USER_SELECTION_BUCKET = "sie-user-selections"
CI_IMG_BUCKET = "sie-ci-images"


"""
    Pubsub topic ids
"""

SIE_IMG_PROCESSING_RESULT = "sie-image-processing-result-test"


"""
    Firestore collections
"""
FIRESTORE_USER_COLLECTION = "Users"
FIRESTORE_USER_EXPERIMENT_SUBCOLLECTION = "Experiments"
