"""
Vehicle License Plate Recognition Web App (Streamlit)

This Streamlit application allows users to upload or capture an image of a vehicle,
then processes it using an ALPR (Automatic License Plate Recognition) system to detect
and extract the license plate number.
"""

import time

import streamlit as st

from utils import process_image, return_url

st.set_page_config(page_title="Nhận dạng biển số xe", layout="centered")
st.title("HỆ THỐNG NHẬN DẠNG BIỂN SỐ XE")

if "vehicle_history" not in st.session_state:
    st.session_state.vehicle_history = []

upload = st.toggle("CHẾ ĐỘ TẢI ẢNH")

if upload:
    uploaded_image = st.file_uploader("Tải ảnh")
else:
    uploaded_image = st.camera_input("Chụp ảnh")

if uploaded_image:
    with st.spinner("Đang nhận dạng biển số...", show_time=True):
        start_time = time.time()
        image_url = return_url(uploaded_image)
        response = process_image(image_url)
        duration_ms = time.time() - start_time
        if response and response.get("error"):
            st.error("Không tìm thấy biển số xe")
        else:
            st.success(
                f"""Biển số xe: {response["license_plate"]}
                    Độ tin cậy {response["ocr_confidence"]:.2f}
                    Thời gian xử lý: {duration_ms:.2f} s"""
            )
            st.image(uploaded_image)
