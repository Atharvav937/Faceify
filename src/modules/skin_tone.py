import cv2
import numpy as np
from utils.segmentation import get_portrait_mask
from config import (
    YCRCB_RANGE,
    HSV_RANGE,
    MORPH_CLOSE_KERNEL_SIZE,
    MORPH_OPEN_KERNEL_SIZE,
    GAUSSIAN_KERNEL_SIZE
)

MODULE_NAME = "skin_tone"


def adjust_skin_tone(image, y_scale, y_offset, cr_shift, cb_shift):
    """
    Adjusts the skin tone of the face in the image using YCrCb and HSV color spaces,
    refined using Deep Learning Portrait Segmentation and Contour Hole-Filling to
    dynamically isolate the person's skin and prevent background leakage or highlight patchiness.

    Parameters:
        image : Input BGR image
        y_scale : Scale factor for luminance channel (Y)
        y_offset : Absolute offset for luminance channel (Y)
        cr_shift : Shift value for red-difference channel (Cr)
        cb_shift : Shift value for blue-difference channel (Cb)

    Returns:
        Image with modified skin tone.
    """
    h_img, w_img = image.shape[:2]

    # 1. Get portrait mask isolating the person from the background
    portrait_mask = get_portrait_mask(image)

    # 2. Convert to YCrCb and HSV for skin color thresholding
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Skin color range in YCrCb from config
    min_ycrcb = np.array([YCRCB_RANGE["y_min"], YCRCB_RANGE["cr_min"], YCRCB_RANGE["cb_min"]], dtype=np.uint8)
    max_ycrcb = np.array([YCRCB_RANGE["y_max"], YCRCB_RANGE["cr_max"], YCRCB_RANGE["cb_max"]], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, min_ycrcb, max_ycrcb)

    # Skin color range in HSV from config
    min_hsv = np.array([HSV_RANGE["h_min"], HSV_RANGE["s_min"], HSV_RANGE["v_min"]], dtype=np.uint8)
    max_hsv = np.array([HSV_RANGE["h_max"], HSV_RANGE["s_max"], HSV_RANGE["v_max"]], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, min_hsv, max_hsv)

    # Combine color masks
    color_skin_mask = cv2.bitwise_and(mask_ycrcb, mask_hsv)

    # Combine color mask and portrait mask to isolate skin strictly on the person
    skin_mask = cv2.bitwise_and(color_skin_mask, portrait_mask)

    # Bridge forehead glare gap touching the hair boundary (virtual headband closed by portrait mask)
    x_p, y_p, w_p, h_p = cv2.boundingRect(portrait_mask)
    headband_y = int(y_p + 0.12 * h_p)
    cv2.line(skin_mask, (x_p, headband_y), (x_p + w_p, headband_y), 255, 5)
    skin_mask = cv2.bitwise_and(skin_mask, portrait_mask)

    # 3. Clean up the mask: morphological opening to smooth edges
    open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (MORPH_OPEN_KERNEL_SIZE, MORPH_OPEN_KERNEL_SIZE))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, open_kernel)

    # 4. Bridge gaps inside the face skin mask using a larger morphological closing
    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (MORPH_CLOSE_KERNEL_SIZE, MORPH_CLOSE_KERNEL_SIZE))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, close_kernel)

    # 5. Flood fill from point (0, 0) to fill all remaining internal holes (e.g. eyes, glasses, highlights)
    floodfill_mask = skin_mask.copy()
    ff_temp = np.zeros((h_img + 2, w_img + 2), np.uint8)
    cv2.floodFill(floodfill_mask, ff_temp, (0, 0), 255)

    # Invert floodfilled mask to isolate all internal holes, then combine with original mask
    floodfill_inv = cv2.bitwise_not(floodfill_mask)
    skin_mask = skin_mask | floodfill_inv

    # 6. Feather mask using Gaussian Blur to ensure smooth transitions
    skin_mask_blurred = cv2.GaussianBlur(skin_mask, (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), 0)

    # Normalize mask to range [0, 1] for blending
    mask_norm = skin_mask_blurred.astype(np.float32) / 255.0
    mask_norm = np.expand_dims(mask_norm, axis=2)  # Shape: (H, W, 1)

    # Apply transformations on YCrCb channels
    y, cr, cb = cv2.split(ycrcb)

    # Apply luminance scaling and offset
    y_new = y.astype(np.float32) * y_scale + y_offset
    y_new = np.clip(y_new, 0, 255).astype(np.uint8)

    # Apply chrominance shifts
    cr_new = cr.astype(np.int16) + cr_shift
    cr_new = np.clip(cr_new, 0, 255).astype(np.uint8)

    cb_new = cb.astype(np.int16) + cb_shift
    cb_new = np.clip(cb_new, 0, 255).astype(np.uint8)

    # Merge channels and convert back to BGR
    ycrcb_modified = cv2.merge([y_new, cr_new, cb_new])
    modified_bgr = cv2.cvtColor(ycrcb_modified, cv2.COLOR_YCrCb2BGR)

    # Blend modified skin region with original image
    output_image = (image.astype(np.float32) * (1.0 - mask_norm) +
                    modified_bgr.astype(np.float32) * mask_norm)

    return np.clip(output_image, 0, 255).astype(np.uint8)
