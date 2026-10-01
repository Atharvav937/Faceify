import cv2

MODULE_NAME = "blur"


def apply_gaussian_blur(image, kernel_size, sigma):
    """
    Apply Gaussian Blur to an image.

    Parameters:
        image : Input image
        kernel_size : Tuple (must be odd)
        sigma : Standard deviation

    Returns:
        Blurred image
    """

    return cv2.GaussianBlur(
        image,
        kernel_size,
        sigma
    )