# This cloud function gets triggered by a change
# in `sie-raw-images` storage bucket
# It picks up the newly created image and sends it
# to cloud vision API for pre-processing
# Then runs the provided R-script to generate processed images

import os
import cv2
import requests
import numpy as np
import traceback
import sys

from google.cloud import vision
from google.cloud import storage

import constants
import exceptions


def face_check(face):
    """
    The function validates the face expression and quality of the image.
    Args:
        face: face_annotations return by Google Vision API
    returns:
        bool: True if valid, otherwise raises InvalidFaceImage exception
    """
    if (
        face.joy_likelihood > constants.EMOTION_THRESHOLD
        or face.anger_likelihood > constants.EMOTION_THRESHOLD
        or face.surprise_likelihood > constants.EMOTION_THRESHOLD
        or face.sorrow_likelihood > constants.EMOTION_THRESHOLD
    ):
        raise exceptions.InvalidFaceImage(
            "Please make sure your image has neutral facial expression."
        )

    if face.under_exposed_likelihood > constants.LIGHTING_THRESHOLD:
        raise exceptions.InvalidFaceImage("Please make sure your image is well-lit.")

    if face.blurred_likelihood > constants.BLURRY_THRESHOLD:
        raise exceptions.InvalidFaceImage("Please make sure your image is clear.")

    if (
        face.roll_angle < -constants.ANGLE_THRESHOLD
        or face.roll_angle > constants.ANGLE_THRESHOLD
        or face.pan_angle < -constants.ANGLE_THRESHOLD
        or face.pan_angle > constants.ANGLE_THRESHOLD
        or face.tilt_angle < -constants.ANGLE_THRESHOLD
        or face.tilt_angle > constants.ANGLE_THRESHOLD
    ):
        raise exceptions.InvalidFaceImage(
            "Please face straight towards your camera, avoid tiliting."
        )

    return True


def face_detection(uri):
    """
    This function detects the faces in the file
    located in Google Cloud Storage or the web
    Args:
        uri: the file located in Google Cloud Storage or the web
    returns:
        None: Prints the likelihood of the face expressions
        or returns an errors resonse in string format
    """
    vision_client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    response = vision_client.face_detection(image=image)

    faceAnnotations = response.face_annotations

    # Making sure that there's only one person in the frame
    if len(faceAnnotations) != 1:
        raise exceptions.InvalidFaceImage(
            "Please ensure exactly ONE face is in the image."
        )

    face = faceAnnotations[0]

    face_check(face)

    vertices_list = []

    mid_eyes = (0, 0)
    nose = (0, 0)
    left_ear = (0, 0)
    right_ear = (0, 0)
    chin = (0, 0)

    for vertex in face.bounding_poly.vertices:
        vertices_list.append((vertex.x, vertex.y))

    for landmark in face.landmarks:
        if landmark.type_ == constants.MID_EYES:
            mid_eyes = (int(landmark.position.x), int(landmark.position.y))
        elif landmark.type_ == constants.NOSE_TIP:
            nose = (int(landmark.position.x), int(landmark.position.y))
        elif landmark.type_ == constants.LEFT_EAR:
            left_ear = (int(landmark.position.x), int(landmark.position.y))
        elif landmark.type_ == constants.RIGHT_EAR:
            right_ear = (int(landmark.position.x), int(landmark.position.y))
        elif landmark.type_ == constants.CHIN_BOTTOM:
            chin = (int(landmark.position.x), int(landmark.position.y))

    if (
        mid_eyes == (0, 0)
        or nose == (0, 0)
        or left_ear == (0, 0)
        or right_ear == (0, 0)
        or chin == (0, 0)
    ):
        raise exceptions.InvalidFaceImage(
            "Please ensure your full face is visible in the image, \
            including both ears."
        )

    return (
        vertices_list[0][0],
        vertices_list[0][1],
        vertices_list[2][0],
        vertices_list[2][1],
        mid_eyes,
        nose,
        left_ear,
        right_ear,
        chin,
    )


def process_img(
    path,
    top_left_x,
    top_left_y,
    bottom_right_x,
    bottom_right_y,
    mid_eyes,
    nose,
    left_ear,
    right_ear,
    chin,
):
    """
    This function is used to process a valid image. Processing steps are:
    masking, croping, grayscale, resize
    Args:
        top_left_x: top left x-coord of face bounding polygon
        top_left_y: top left y-coord of face bounding polygon
        bottom_right_x: bottom right x-coord of face bounding polygon
        bottom_right_y: bottom right y-coord of face bounding polygon
        mid_eyes: (x,y) coordinate of mid point of eyes
        nose: (x,y) coordinate of nose
        left_ear: (x,y) coordinate of left ear
        right_ear: (x,y) coordinate of right ear
        chin: (x,y) coordinate of chin
    returns:
        str: file path of the processed image
    """

    img = cv2.imread(path)

    # create mask
    mask = create_mask(
        img.shape[0], img.shape[1], mid_eyes, nose, left_ear, right_ear, chin
    )

    # apply mask
    masked_img = cv2.bitwise_and(img, mask)

    # crop
    height = bottom_right_y - top_left_y
    width = bottom_right_x - top_left_x
    if height > width:
        make_square = (height - width) / 2
        top_left_x = int(top_left_x) - int(make_square)
        bottom_right_x = int(bottom_right_x) + int(make_square)
    elif width > height:
        make_square = (width - height) / 2
        top_left_y = int(top_left_y) - int(make_square)
        bottom_right_y = int(bottom_right_y) + int(make_square)

    # Make the background color grey

    # naive fix for linting error: line getting to long ->
    crop_img = masked_img[top_left_y:bottom_right_y, top_left_x:bottom_right_x].copy()
    crop_img[np.where((crop_img == [0, 0, 0]).all(axis=2))] = [140, 141, 137]

    # Convert to Grayscale
    gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # resize
    final_img = resize(gray_img)

    # Save processed image to local dir
    processed_file_path = f"{constants.TEMP_DIR}/{constants.PROCESSED_IMAGE}"
    cv2.imwrite(processed_file_path, final_img)
    return processed_file_path


def create_mask(height, width, mid_eyes, nose, left_ear, right_ear, chin):
    """
    This function is used to create mask given the coordinates
    of face attributes
    Args:
        height: height of the image
        width: width of the image
        mid_eyes: (x,y) coordinate of mid point of eyes
        nose: (x,y) coordinate of nose
        left_ear: (x,y) coordinate of left ear
        right_ear: (x,y) coordinate of right ear
        chin: (x,y) coordinate of chin
    returns:
        numpy.ndarray: data containing the masked image
    """
    mask = np.zeros((height, width, 3), np.uint8)

    center_x = nose[0]
    center_y = int((nose[1] - mid_eyes[1]) / 2 + mid_eyes[1])
    center_coordinates = (center_x, center_y)
    axesLength = (
        int((right_ear[0] - left_ear[0]) // 2 * 1),
        int((chin[1] - center_y) * 1.05),
    )

    # Using cv2.ellipse() method
    # Draw a solid ellipse
    mask = cv2.ellipse(
        mask,
        center_coordinates,
        axesLength,
        constants.ANGLE,
        constants.START_ANGLE,
        constants.END_ANGLE,
        constants.WHT_COLOR,
        constants.THICKNESS,
    )

    return mask


def resize(image):
    """
    This function is used to resize height and width into either:
    512, 256 or 128 pixels
    Args:
        image: image data of type numpy.ndarray
    returns:
        numpy.ndarray: resize image data
    """
    if image.shape[0] >= 512 and image.shape[1] >= 512:
        return cv2.resize(image, (512, 512))
    elif image.shape[0] >= 256 and image.shape[1] >= 256:
        return cv2.resize(image, (256, 256))
    elif image.shape[0] >= 128 and image.shape[1] >= 128:
        return cv2.resize(image, (128, 128))
    else:
        return None


def detect_and_process(uri):
    """
    This is a mock function to test the functionality of our image
    processing pipeline without using Google Storage Bucket. In other
    words, we want the below functionality implemented in trigger_event()
    function later on.

    Currently the images are stored in /temp directory as ori.jpg (raw) and
    neutral.jpg (processed) instead of GStorageBuckets.
    Args:
        uri: URI of the source image
    returns:
        str: Error or Success message
    """

    try:
        # parse the image url from the uri
        # Example URI when testing locally:
        # http://localhost:${FUNCTION_PORT_HTTP}/?subject=https://images.pexels.com/
        # photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940
        url = uri.args.get("subject")

        results = face_detection(url)
        # temp directory to store images
        if not os.path.exists(constants.TEMP_DIR):
            os.makedirs(constants.TEMP_DIR)
        download_to = os.getcwd() + f"/{constants.TEMP_DIR}/{constants.SOURCE_IMAGE}"

        # valid face
        topLeft_x, topLeft_y, bottomRight_x, bottomRight_y = (
            results[0],
            results[1],
            results[2],
            results[3],
        )
        mid_eyes, nose, left_ear, right_ear, chin = (
            results[4],
            results[5],
            results[6],
            results[7],
            results[8],
        )

        # download the image into the temp directory
        data_downloaded = requests.get(url)
        with open(download_to, "wb") as outfile:
            outfile.write(data_downloaded.content)

        process_img(
            download_to,
            topLeft_x,
            topLeft_y,
            bottomRight_x,
            bottomRight_y,
            mid_eyes,
            nose,
            left_ear,
            right_ear,
            chin,
        )

    except exceptions.InvalidFaceImage as err:
        return str(err), 400
    except Exception as err:
        return str(err), 500

    return "Processed Sucessfully!", 200


def trigger_event(event, context):
    """
    Background Cloud Function to be triggered by Cloud Storage.
    This generic function logs relevant data when a file is changed.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                        The `data` field contains a description of the event in
                        the Cloud Storage `object` format described here:
                        https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    bucket_name = event["bucket"]
    source_img = event["name"]
    tmp_download_path = f"/tmp/{source_img}"

    try:
        download_image(bucket_name, source_img, tmp_download_path)
        print(f"Image {source_img} downloaded to {tmp_download_path}")
        # currenlty this makes sure there's one person
        # in the frame and prints a few other details
        face_detection(tmp_download_path)
        # TODO(jerry) call R script with features returned from Abi's part
        # TODO(hantao) put processed images to `sie-processed-images` bucket
    except Exception:
        pass
    finally:
        if os.path.isfile(tmp_download_path):
            os.remove(tmp_download_path)
        else:
            print("Error: %s file not found" % tmp_download_path)


def download_image(bucket_name, source_blob_name, destination_file_name):
    """Downloads the specified image from cloud storage
    Args:
        bucket_name = "your-bucket-name"
        source_blob_name = "image-name"
        destination_file_name = "local/path/to/file"

    Returns:
        Local path to downloaded image
    """

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_processed_images(bucket_name, source_file_folder):
    """Uploads images to the bucket.
    Args:
        bucket_name = "your-bucket-name"
        source_file_folder = Path to the folder that contains
                                all the processed images

    Returns:
        None;
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for file_name in os.listdir(source_file_folder):
        blob = bucket.blob(file_name)
        blob.upload_from_filename(os.path.join(source_file_folder, file_name))

        print("File {} uploaded to {}.".format(file_name, bucket_name))


def upload_image(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket.

    Args:
        bucket_name: Name of the bucket to upload file
        source_file_name: path of file to upload
    """

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return destination_blob_name


def trigger_detect_and_mask(event, context):
    """
    Trigger function to detect and mask an image storaged
    in the sie-raw-images bucket. Saves the masked image in
    sie-masked-images.

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                        The `data` field contains a description of the event in
                        the Cloud Storage `object` format described here:
                        https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        str; error or success message
    """

    bucket_name = event["bucket"]  # sie-raw-images bucket
    cloud_storage_prefix = "gs://" + bucket_name + "/"
    cloud_download_from = event["name"]  # file path

    # extract file name from path eg: folder/image.jpg
    file_name = cloud_download_from.split("/")[-1]

    # local directory to store image
    cloud_download_to = f"{constants.TEMP_DIR}/{file_name}"

    # fetching image from this URI
    uri = cloud_storage_prefix + cloud_download_from

    try:
        # check for face
        results = face_detection(uri)

        # download images from bucket sie-raw-images to create a mask
        download_image(bucket_name, cloud_download_from, cloud_download_to)
        print(f"Image {cloud_download_from} downloaded to {cloud_download_to}")

        # face annotations
        topLeft_x, topLeft_y, bottomRight_x, bottomRight_y = (
            results[0],
            results[1],
            results[2],
            results[3],
        )
        mid_eyes, nose, left_ear, right_ear, chin = (
            results[4],
            results[5],
            results[6],
            results[7],
            results[8],
        )

        # process and create a mask
        cloud_upload_from = process_img(
            cloud_download_to,
            topLeft_x,
            topLeft_y,
            bottomRight_x,
            bottomRight_y,
            mid_eyes,
            nose,
            left_ear,
            right_ear,
            chin,
        )

        # Upload masked image to sie-masked-images bucket
        participant_id = os.path.splitext(file_name)[0]  # remove file ext
        cloud_upload_to = f"{participant_id}/{constants.PROCESSED_IMAGE}"
        upload_image("sie-masked-images", cloud_upload_from, cloud_upload_to)
        print("Processed image saved at: " + cloud_upload_to)

    except exceptions.InvalidFaceImage as err:
        traceback.print_exception(*sys.exc_info())
        return str(err), 400
    except Exception as err:
        traceback.print_exception(*sys.exc_info())
        return str(err), 500

    return "Face detected and masked successfully!", 200
