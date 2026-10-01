import cv2
import numpy as np


def _create_directional_light(
    height,
    width,
    direction="front",
    hardness="soft"
):
    """
    Create a normalized directional light gradient.

    direction:
        front
        left
        right
        top
        bottom

    hardness:
        soft
        hard
    """

    y, x = np.mgrid[0:height, 0:width]

    # Normalize coordinates to [0, 1]
    x = x.astype(np.float32) / max(width - 1, 1)
    y = y.astype(np.float32) / max(height - 1, 1)

    if direction == "left":
        light = 1.0 - x

    elif direction == "right":
        light = x

    elif direction == "top":
        light = 1.0 - y

    elif direction == "bottom":
        light = y

    else:
        # Front light
        center_x = 0.5
        center_y = 0.5

        distance = np.sqrt(
            (x - center_x) ** 2 +
            (y - center_y) ** 2
        )

        light = 1.0 - distance / np.sqrt(0.5 ** 2 + 0.5 ** 2)

    light = np.clip(light, 0.0, 1.0)

    if hardness == "soft":
        light = cv2.GaussianBlur(
            light,
            (0, 0),
            sigmaX=max(width, height) / 8
        )

    elif hardness == "hard":
        light = np.power(light, 2.0)

    return light


def _apply_color_temperature(image, temperature):
    """
    Apply a simple warm/cool color-temperature shift.
    """

    result = image.astype(np.float32)

    if temperature == "warm":
        result[:, :, 2] *= 1.08
        result[:, :, 1] *= 1.02
        result[:, :, 0] *= 0.92

    elif temperature == "cool":
        result[:, :, 2] *= 0.92
        result[:, :, 1] *= 1.00
        result[:, :, 0] *= 1.08

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_lighting(
    image,
    direction="front",
    hardness="soft",
    temperature="neutral",
    exposure=0.0,
    intensity=0.35
):
    """
    Apply physically-inspired synthetic lighting.

    Parameters
    ----------
    image : numpy.ndarray
        BGR OpenCV image.

    direction : str
        front, left, right, top, bottom

    hardness : str
        soft or hard

    temperature : str
        neutral, warm, cool

    exposure : float
        Exposure adjustment.

    intensity : float
        Strength of directional lighting.
    """

    if image is None:
        raise ValueError("Input image cannot be None.")

    height, width = image.shape[:2]

    light_map = _create_directional_light(
        height,
        width,
        direction,
        hardness
    )

    # Convert [0, 1] light map into a multiplicative factor.
    factor = 1.0 + (
        (light_map - 0.5) *
        2.0 *
        intensity
    )

    result = image.astype(np.float32)

    result *= factor[:, :, None]

    # Exposure adjustment
    if exposure != 0:
        result *= 2.0 ** exposure

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    # Color temperature
    result = _apply_color_temperature(
        result,
        temperature
    )

    return result


# ------------------------------------------------------------
# BACKWARD COMPATIBILITY
# ------------------------------------------------------------

def adjust_brightness(image, beta):
    """
    Keep the original API working.

    Existing generator code still calls this function.
    """

    return cv2.convertScaleAbs(
        image,
        alpha=1.0,
        beta=beta
    )