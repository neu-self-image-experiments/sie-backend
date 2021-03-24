"""
    Google Vision - These constants are used to detect and
    validate the face in the image
"""
EMOTION_THRESHOLD = 3
LIGHTING_THRESHOLD = 2
BLURRY_THRESHOLD = 2
ANGLE_THRESHOLD = 10.0

MID_EYES = 7
NOSE_TIP = 8
LEFT_EAR = 27
RIGHT_EAR = 28
CHIN_BOTTOM = 32

ANGLE = 0
START_ANGLE = 0
END_ANGLE = 360
WHT_COLOR = (255, 255, 255)  # White color in BGR
THICKNESS = -1  # Line thickness

ORIGIN_COORD = (0, 0)  # origin coordinates

"""
    PROJECT SPECIFIC
"""
TEMP_DIR = "/tmp"
SOURCE_IMAGE = "ori.jpg"
PROCESSED_IMAGE = "neutral.jpg"
