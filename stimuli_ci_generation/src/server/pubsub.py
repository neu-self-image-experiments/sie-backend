#!/usr/bin/env python

from google.cloud import pubsub_v1
from google import api_core

from gcp_config import PROJECT_ID


publisher = pubsub_v1.PublisherClient()


# Configure the retry settings. Defaults shown in comments are values applied
# by the library by default, instead of default values in the Retry object.
# doc: https://cloud.google.com/pubsub/docs/publisher
custom_retry = api_core.retry.Retry(
    initial=0.250,  # seconds (default: 0.1)
    maximum=90.0,  # seconds (default: 60.0)
    multiplier=1.45,  # default: 1.3
    deadline=120.0,  # seconds (default: 60.0)
    predicate=api_core.retry.if_exception_type(
        api_core.exceptions.Aborted,
        api_core.exceptions.DeadlineExceeded,
        api_core.exceptions.InternalServerError,
        api_core.exceptions.ResourceExhausted,
        api_core.exceptions.ServiceUnavailable,
        api_core.exceptions.Unknown,
        api_core.exceptions.Cancelled,
    ),
)


def get_callback(future, data):
    """
    Handle callback from msg publishing
    Args:
        future: future object
        data: published message
    """

    def callback(future):
        try:
            print(future.result())
        except:  # noqa
            print("Please handle {} for {}.".format(future.exception(), data))

    return callback


def pub_msg(msg: str, topic_id: str, identifier: str):
    """
    Publish a message to a pubsub topic
    Args:
        msg: message to be published
        topic_id: pubsub topic id
        identifier: survey identifier
    """

    data = msg.encode("utf-8")
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)
    future = publisher.publish(
        topic_path,
        data,
        identifier=identifier,
        retry=custom_retry,
    )
    future.add_done_callback(get_callback(future, data))
