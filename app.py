import streamlit as st

from apps.label import image_label_only
from apps.license import license_plate_only


def start_application():
    st.set_page_config(page_title="Nhận dạng biển số xe", layout="centered")
    st.title("HỆ THỐNG NHẬN DẠNG BIỂN SỐ XE")

    st.sidebar.title("Chế độ hoạt động")
    mode = st.sidebar.radio(
        "Vui lòng chọn một chế độ:",
        ["Nhận diện BSX", "Dán nhãn hình ảnh"],
    )

    st.warning(
        "Hệ thống có thể tạo ra phản hồi sai. Vui lòng kiểm tra lại thông tin trước khi sử dụng."
    )

    if mode == "Nhận diện BSX":
        license_plate_only()
    elif mode == "Dán nhãn hình ảnh":
        image_label_only()


if __name__ == "__main__":
    start_application()
