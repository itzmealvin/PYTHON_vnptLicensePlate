import base64

import cv2
import numpy as np
from fast_alpr import ALPR

alpr = ALPR(
    detector_model="yolo-v9-t-512-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
)


def return_url(uploaded_image):
    return base64.b64encode(uploaded_image.getvalue()).decode("utf-8")


def process_image(image_url):
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


def crop_and_save_plate(img, bbox, output_path):
    x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
    cropped = img[y1:y2, x1:x2]
    cv2.imwrite(str(output_path), cropped)
    return [x1, y1, x2, y2]
