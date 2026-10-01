import cv2
import numpy as np


def detect_face(image):
    """
    Detect the largest frontal face in the image.

    Returns:
        (x, y, w, h) or None
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cascade_path = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    face_cascade = cv2.CascadeClassifier(cascade_path)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    if len(faces) == 0:
        return None

    # Use the largest detected face
    return max(
        faces,
        key=lambda face: face[2] * face[3]
    )


def apply_camera_angle(
    image,
    angle="frontal",
    strength=0.12
):
    """
    Simulate a small horizontal camera-angle change.

    angle:
        frontal
        slight_left
        slight_right
        left
        right

    strength:
        Controls the amount of horizontal perspective distortion.
    """

    if image is None:
        raise ValueError("Input image cannot be None.")

    height, width = image.shape[:2]

    if angle == "frontal":
        return image.copy()

    face = detect_face(image)

    if face is None:
        # Safely return original image if no face is detected.
        return image.copy()

    x, y, w, h = face

    # Face center
    face_center_x = x + w / 2
    face_center_y = y + h / 2

    # Direction
    if angle in ("left", "slight_left"):
        direction = -1.0
    else:
        direction = 1.0

    if angle in ("slight_left", "slight_right"):
        amount = strength
    else:
        amount = strength * 1.8

    # Perspective displacement.
    shift = w * amount * direction

    src = np.float32([
        [0, 0],
        [width - 1, 0],
        [0, height - 1],
        [width - 1, height - 1]
    ])

    dst = np.float32([
        [shift, 0],
        [width - 1 + shift, 0],
        [0, height - 1],
        [width - 1, height - 1]
    ])

    matrix = cv2.getPerspectiveTransform(
        src,
        dst
    )

    transformed = cv2.warpPerspective(
        image,
        matrix,
        (width, height),
        borderMode=cv2.BORDER_REFLECT
    )

    return transformed