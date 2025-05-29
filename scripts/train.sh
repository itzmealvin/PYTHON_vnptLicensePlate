KERAS_BACKEND=tensorflow fast_plate_ocr train \
    --annotations ./plate_dataset/train.csv \
    --val-annotations ./plate_dataset/val.csv \
    --config-file ./yaml/config.yaml \
    --batch-size 128 \
    --epochs 750 \
    --dense \
    --early-stopping-patience 100 \
    --reduce-lr-patience 50