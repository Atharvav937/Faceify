import cv2

MODULE_NAME = "quality"


def apply_jpeg_compression(image, quality):
    """
    Compress an image to JPEG in memory and decode it back to return the degraded image array.
    """
    success, encoded = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not success:
        raise ValueError("JPEG compression failed")
    return cv2.imdecode(encoded, cv2.IMREAD_COLOR)