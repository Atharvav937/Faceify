import cv2

def read_image(path):
    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {path}")

    return image


def save_image(path, image):
    cv2.imwrite(path, image)