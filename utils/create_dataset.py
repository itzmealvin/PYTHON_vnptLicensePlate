from pathlib import Path

import cv2
import pandas as pd
from fast_alpr import ALPR

from utils import crop_and_save_plate

alpr = ALPR(
    detector_model="yolo-v9-t-512-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
)


def main():
    full_path = Path("plate_dataset/full")
    train_path = Path("plate_dataset/train")
    train_path.mkdir(parents=True, exist_ok=True)
    csv_path = "./plate_dataset/train.csv"

    records = []
    dimensions = []

    for image_file in full_path.glob("*.[jp][pn]g"):
        alpr_results = alpr.predict(str(image_file))
        if not alpr_results:
            print(f"Cannot get result from {image_file.name}")
            continue

        result = {
            "bounding_box": alpr_results[0].detection.bounding_box,
            "license_plate": alpr_results[0].ocr.text,
            "ocr_confidence": alpr_results[0].ocr.confidence,
        }

        img = cv2.imread(str(image_file))

        cropped_filename = f"{image_file.stem}.jpg"
        cropped_path = train_path / cropped_filename

        dimensions.append(
            crop_and_save_plate(img, result["bounding_box"], cropped_path)
        )

        records.append(
            {
                "image_path": cropped_filename,
                "plate_text": result["license_plate"],
                "ocr_confidence": result["ocr_confidence"],
                "checked": False,
            }
        )

    if records:
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(records)} records to {csv_path}")

        max_width = max(x2 - x1 for x1, _, x2, _ in dimensions)
        max_height = max(y2 - y1 for _, y1, _, y2 in dimensions)
        print(f"Max dimensions: W:{max_width} x H:{max_height}")
    else:
        print("No license plates found")


if __name__ == "__main__":
    main()
