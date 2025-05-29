import albumentations as A
import cv2

BORDER_COLOR_BLACK = (0, 0, 0)

TRAIN_AUGMENTATION = A.Compose(
    [
        # Biến dạng hình học như nghiêng lệch
        A.Affine(
            scale=(0.9, 1.1),
            translate_percent=(-0.06, 0.06),
            rotate=(-9, 9),
            mode=cv2.BORDER_CONSTANT,
            cval=BORDER_COLOR_BLACK,
            p=1,
        ),
        # Giả lập mờ do chuyển động hoặc sương mù
        A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=1),
        A.MotionBlur(blur_limit=(3, 5), p=0.5),
        # Giả lập méo ảnh, lệch ống kính
        A.OneOf(
            [
                A.OpticalDistortion(distort_limit=0.05, shift_limit=0.05, p=0.5),
                A.ElasticTransform(alpha=1, sigma=50, alpha_affine=10, p=0.5),
            ],
            p=0.5,
        ),
        # Giả lập bị khuất, bẩn, mất góc
        A.OneOf(
            [
                A.CoarseDropout(
                    min_holes=1,
                    max_holes=3,
                    min_height=10,
                    max_height=20,
                    min_width=20,
                    max_width=30,
                    fill_value=0,
                    p=0.5,
                ),
                A.PixelDropout(dropout_prob=0.01, p=0.5),
            ],
            p=0.5,
        ),
    ]
)

A.save(TRAIN_AUGMENTATION, "./yaml/transform_pipeline.yaml", data_format="yaml")
