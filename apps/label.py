import csv
import os
from pathlib import Path

import streamlit as st


def image_label_only():
    train_path = Path("plate_dataset/train")
    train_path.mkdir(parents=True, exist_ok=True)
    csv_path = Path("plate_dataset/train.csv")

    if not csv_path.exists():
        st.toast(
            f"Không tìm thấy tệp {csv_path} tại đường dẫn.",
            icon="❌",
        )
        return

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) <= 1:
        st.toast(f"Không có dữ liệu trong tệp {csv_path}", icon="❌")
        return

    metadata = rows[1:]
    total = len(metadata)

    if "current_idx" not in st.session_state:
        st.session_state.current_idx = 0

    with st.sidebar:
        col_left, col_mid, col_right = st.columns([1, 4, 1])
        with col_left:
            if st.button("⬅️", key="prev_sidebar") and st.session_state.current_idx > 0:
                st.session_state.current_idx -= 1
        with col_mid:
            st.write(
                "<h2 style='text-align: center;'>Điều hướng</h2>",
                unsafe_allow_html=True,
            )
        with col_right:
            if (
                st.button("➡️", key="next_sidebar")
                and st.session_state.current_idx < total - 1
            ):
                st.session_state.current_idx += 1

    with st.sidebar.form("jump_form"):
        jump_to = st.number_input(
            "Nhập số thứ tự ảnh muốn xem (từ 1 đến {})".format(total),
            min_value=1,
            max_value=total,
            step=1,
        )
        jump = st.form_submit_button("Nhảy tới ảnh này!")
        if jump:
            st.session_state.current_idx = jump_to - 1

    idx = st.session_state.current_idx
    image_path, plate_text, ocr_confidence, checked = metadata[idx]
    image_path = train_path / image_path

    st.write(
        f"<h3 style='text-align: center;'>Hình số: {idx+1}/{total}</h3>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.text("Ảnh BSX hiện tại")
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.warning(f"Không tìm thấy hình tại đường dẫn `{image_path}`")
        st.success(f"Độ tin cậy: {float(ocr_confidence):.2f}")

    with col2:
        if checked == "True":
            st.success("Dòng này đã được duyệt")
        else:
            st.error("Dòng này chưa được duyệt")
        fixed_output = st.text_area(
            "(Chỉnh sửa) kết quả nhận diện tự động:",
            value=plate_text,
            key=f"fixed_output_{idx}",
        )

        @st.dialog("Xác nhận xóa ảnh")
        def delete_row():
            st.error("Bạn có chắc muốn xóa ảnh này chứ?")
            if st.button("Xác nhận"):
                if image_path.exists():
                    os.remove(image_path)
                metadata.pop(idx)
                st.session_state.current_idx = max(0, idx - 1)
                with open(csv_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(rows[0])
                    writer.writerows(metadata)
                st.toast("Đã xoá thành công!", icon="✅")
                st.rerun()

        is_checked = st.button("Duyệt", key=f"checked_{idx}")
        if st.button("Xoá dòng", key=f"delete_{idx}"):
            delete_row()

        if is_checked:
            metadata[idx][1] = fixed_output
            metadata[idx][3] = "True"
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(rows[0])
                writer.writerows(metadata)
            st.toast("Đã lưu kết quả thành công!", icon="✅")
            st.rerun()
