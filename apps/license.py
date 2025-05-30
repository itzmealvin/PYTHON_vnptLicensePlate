import time

import streamlit as st

from utils.utils import process_image, return_url


def license_plate_only():
    upload = st.toggle("CHẾ ĐỘ TẢI ẢNH")

    if upload:
        uploaded_image = st.file_uploader("Tải ảnh")
    else:
        uploaded_image = st.camera_input("Chụp ảnh")

    if uploaded_image:
        with st.spinner("Đang nhận dạng biển số", show_time=True):
            start_time = time.time()
            image_url = return_url(uploaded_image)
            response = process_image(image_url)
            duration_ms = time.time() - start_time
            if response and response.get("error"):
                st.toast("Không tìm thấy biển số xe!", icon="❌")
            else:
                st.success(
                    f"""Biển số xe: {response["license_plate"]}
                        Độ tin cậy: {response["ocr_confidence"]:.2f}
                        Thời gian xử lý: {duration_ms:.2f} s"""
                )
                st.image(uploaded_image)
