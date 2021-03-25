import pytest
import numpy as np
import cv2

from main import face_detection, process_img, create_mask
from exceptions import InvalidFaceImage


def test_smiling_face():
    uri = (
        "https://image.freepik.com/free-photo/"
        "smiling-man-face-white-background_33839-3342.jpg"
    )
    with pytest.raises(
        InvalidFaceImage,
        match="Please make sure your image has neutral facial expression.",
    ):
        face_detection(uri)


def test_not_human_face():

    uri = "https://whyy.org/wp-content/uploads/2020/02/eyebrow-1.jpeg"
    with pytest.raises(
        InvalidFaceImage, match="Please ensure the image has your face in it."
    ):
        face_detection(uri)


def test_tilted_face():
    uri = (
        "https://westsidetoastmasters.com/resources/"
        "book_of_body_language/images/233-head_tilt.jpg"
    )
    with pytest.raises(
        InvalidFaceImage,
        match="Please face straight towards your camera, avoid tiliting.",
    ):
        face_detection(uri)


def test_low_light_photo():

    uri = (
        "https://64.media.tumblr.com/0a2c59e9b675e8d11a2fca8398150"
        "d7f/tumblr_oaevfwGlQL1up31rro1_1280.jpg"
    )
    with pytest.raises(
        InvalidFaceImage, match="Please make sure your image is well-lit."
    ):
        face_detection(uri)


def test_multiple_face_in_photo():

    uri = "https://i1.sndcdn.com/avatars-atGTli7E1tTMoT74-wKcmmQ-t500x500.jpg"
    with pytest.raises(
        InvalidFaceImage, match="Please ensure exactly ONE face is in the image."
    ):
        face_detection(uri)


def test_neutral_face():
    uri = (
        "https://t4.ftcdn.net/jpg/02/46/14/93/"
        "360_F_246149382_KHkt8Mw8pptlmVuiqmhavvHBC4SEqBu1.jpg"
    )

    vertex1 = 134
    vertex2 = 24
    vertex3 = 333
    vertex4 = 255
    midEyes = (228, 133)
    nose = (230, 168)
    leftEar = (169, 163)
    rightEar = (300, 147)
    chin = (237, 235)

    # Call tested function
    result = face_detection(uri)
    assert vertex1 == result[0]
    assert vertex2 == result[1]
    assert vertex3 == result[2]
    assert vertex4 == result[3]
    assert midEyes == result[4]
    assert nose == result[5]
    assert leftEar == result[6]
    assert rightEar == result[7]
    assert chin == result[8]


def test_process_image():
    """
    Test if the final processed image is properly detected, cropped
    and masked.
    """
    full_image_path = "test_assets/ori.jpg"
    expected_image_path = "test_assets/final_expected.jpg"
    test_image_path = process_img(
        full_image_path,
        134,
        24,
        333,
        255,
        (228, 133),
        (230, 168),
        (169, 163),
        (300, 147),
        (237, 235),
    )

    expected_matrix = cv2.imread(expected_image_path)  # Load expected image
    test_matrix = cv2.imread(test_image_path)  # Load test produced image
    assert (expected_matrix == test_matrix).all()  # compare both arrays


def test_create_mask():
    """
    Test masking when coordinates valid
    """
    masked_matrix = create_mask(
        360, 512, (228, 133), (230, 168), (169, 163), (300, 147), (237, 235)
    )
    expected_matrix = np.load("test_assets/masked_array.npy")
    assert (expected_matrix == masked_matrix).all()


def test_create_mask_invalid():
    """
    Test masking when coordinates invalid
    """
    masked_matrix = create_mask(
        360, 512, (200, 133), (230, 168), (169, 163), (250, 147), (237, 235)
    )
    expected_matrix = np.load("test_assets/masked_array.npy")
    assert not (expected_matrix == masked_matrix).all()
