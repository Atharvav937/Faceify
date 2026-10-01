import cv2
import numpy as np


def detect_face(image):
    """
    Detect the largest frontal face.

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

    return max(
        faces,
        key=lambda face: face[2] * face[3]
    )


def apply_pose(
    image,
    pose="frontal",
    strength=0.05
):
    """
    Apply controlled head-pose simulation.

    Supported poses:
        frontal
        tilt_left
        tilt_right
        tilt_up
        tilt_down
    """

    if image is None:
        raise ValueError("Input image cannot be None.")

    height, width = image.shape[:2]

    if pose == "frontal":
        return image.copy()

    face = detect_face(image)

    if face is None:
        # Keep original image if no face is detected.
        return image.copy()

    x, y, w, h = face

    # Face center
    center_x = x + w / 2
    center_y = y + h / 2

    # ------------------------------------------------------------
    # Head tilt
    # ------------------------------------------------------------

    if pose == "tilt_left":
        angle = -strength * 30.0

    elif pose == "tilt_right":
        angle = strength * 30.0

    else:
        angle = 0.0

    # ------------------------------------------------------------
    # Vertical pose
    # ------------------------------------------------------------

    vertical_shift = 0.0

    if pose == "tilt_up":
        vertical_shift = -h * strength

    elif pose == "tilt_down":
        vertical_shift = h * strength

    # ------------------------------------------------------------
    # Rotation matrix
    # ------------------------------------------------------------

    rotation_matrix = cv2.getRotationMatrix2D(
        (center_x, center_y),
        angle,
        1.0
    )

    rotation_matrix[1, 2] += vertical_shift

    transformed = cv2.warpAffine(
        image,
        rotation_matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return transformed