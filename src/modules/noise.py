import numpy as np

MODULE_NAME = "noise"


def add_gaussian_noise(image, std_dev):
    noise = np.random.normal(
        0,
        std_dev,
        image.shape
    )

    noisy_image = image.astype(np.float32) + noise

    noisy_image = np.clip(
        noisy_image,
        0,
        255
    )

    return noisy_image.astype(np.uint8)