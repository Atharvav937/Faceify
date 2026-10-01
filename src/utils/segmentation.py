import os
import urllib.request
from pathlib import Path
import cv2
import numpy as np

# Cache model inside src/models/
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "selfie_segmentation.onnx"
MODEL_URL = "https://huggingface.co/onnx-community/mediapipe_selfie_segmentation_landscape/resolve/main/onnx/model.onnx"


def download_model_if_needed():
    """
    Downloads the pre-trained Selfie Segmentation ONNX model if not already present.
    """
    if not MODEL_PATH.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Downloading portrait segmentation model to {MODEL_PATH}...")
        try:
            urllib.request.urlretrieve(MODEL_URL, str(MODEL_PATH))
            print("Download completed successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to download segmentation model from {MODEL_URL}. Error: {e}")


def get_portrait_mask(image):
    """
    Generates a binary portrait mask isolating the person from the background.

    Parameters:
        image : Input BGR image

    Returns:
        Binary mask (255 for foreground, 0 for background)
    """
    download_model_if_needed()

    h, w = image.shape[:2]
    net = cv2.dnn.readNet(str(MODEL_PATH))

    # Preprocess image: size 256x144, scale 1/255, swapRB=True
    blob = cv2.dnn.blobFromImage(
        image,
        scalefactor=1.0 / 255.0,
        size=(256, 144),
        mean=(0, 0, 0),
        swapRB=True,
        crop=False
    )

    net.setInput(blob)
    output = net.forward()

    # Extract mask and resize back to original resolution
    mask = output[0, 0]  # 144x256
    mask_resized = cv2.resize(mask, (w, h))

    # Threshold mask (0.4 is standard for Google Selfie Segmenter)
    portrait_mask = (mask_resized > 0.4).astype(np.uint8) * 255
    return portrait_mask
