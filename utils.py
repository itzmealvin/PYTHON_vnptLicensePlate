"""
Vehicle License Plate Recognition Utilities

This module provides core utility functions for processing images and identifying
license plates using an ALPR (Automatic License Plate Recognition) model.

Functions:
    - return_url(uploaded_image): Converts an uploaded image (file-like object)
      into a base64-encoded string for further processing or transmission.

    - process_image(image_url): Decodes a base64-encoded image (or data URL),
      processes it with an ALPR model, and returns license plate detection results.
"""

import base64

import cv2
import numpy as np
from fast_alpr import ALPR

alpr = ALPR(
    detector_model="yolo-v9-t-512-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
)


def return_url(uploaded_image):
    """
    Convert a file-like object to a base64-encoded data URL string.

    Args:
        uploaded_file (BytesIO): The uploaded file.

    Returns:
        str: A base64-encoded data URL.
    """
    return base64.b64encode(uploaded_image.getvalue()).decode("utf-8")


def process_image(image_url):
    """
    Process an image from base64 or data URL and detect license plate.

    Args:
        image_url (str): Image in base64 or data:image/png;base64,... format.

    Returns:
        dict: License plate detection result or empty dict if no plate found.
    """
    if image_url.startswith("data:image"):
        base64_data = image_url.split(",")[1]
    else:
        base64_data = image_url

    image_array = np.frombuffer(base64.b64decode(base64_data), dtype=np.uint8)
    img = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
    alpr_results = alpr.predict(img)
    if len(alpr_results) >= 1:
        return {
            "bounding_box": alpr_results[0].detection.bounding_box,
            "box_confidence": alpr_results[0].detection.confidence,
            "license_plate": alpr_results[0].ocr.text,
            "ocr_confidence": alpr_results[0].ocr.confidence,
        }
    return {}
