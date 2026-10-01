import cv2
import numpy as np


def apply_age(image, age_level="adult"):
    """
    Apply a controlled synthetic age appearance effect.

    This is a simulation for dataset diversity, not
    photorealistic age transformation.
    """

    if image is None:
        raise ValueError("Input image cannot be None.")

    if age_level == "young":
        return _young_effect(image)

    if age_level == "adult":
        return image.copy()

    if age_level == "older":
        return _older_effect(image)

    raise ValueError(
        f"Unsupported age level: {age_level}"
    )


def _young_effect(image):
    """
    Slightly smoother and brighter appearance.
    """

    # Mild smoothing
    smooth = cv2.GaussianBlur(
        image,
        (5, 5),
        0
    )

    # Blend original and smooth image
    output = cv2.addWeighted(
        image,
        0.65,
        smooth,
        0.35,
        0
    )

    # Slight brightness adjustment
    output = cv2.convertScaleAbs(
        output,
        alpha=1.02,
        beta=3
    )

    return output


def _older_effect(image):
    """
    Simulates visual characteristics associated
    with older image appearance using texture,
    local contrast and mild sharpening.
    """

    # ----------------------------------------------------------
    # Increase local contrast
    # ----------------------------------------------------------

    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    l_channel = clahe.apply(l_channel)

    enhanced = cv2.merge(
        [l_channel, a_channel, b_channel]
    )

    enhanced = cv2.cvtColor(
        enhanced,
        cv2.COLOR_LAB2BGR
    )

    # ----------------------------------------------------------
    # Mild sharpening
    # ----------------------------------------------------------

    blurred = cv2.GaussianBlur(
        enhanced,
        (0, 0),
        2
    )

    sharpened = cv2.addWeighted(
        enhanced,
        1.35,
        blurred,
        -0.35,
        0
    )

    # ----------------------------------------------------------
    # Subtle fine texture
    # ----------------------------------------------------------

    noise = np.random.normal(
        0,
        2.0,
        sharpened.shape
    ).astype(np.float32)

    textured = sharpened.astype(
        np.float32
    ) + noise

    textured = np.clip(
        textured,
        0,
        255
    ).astype(np.uint8)

    return textured