import streamlit as st
import cv2
import tempfile
import numpy as np
import pandas as pd
from ultralytics import YOLO
from detect_and_track import process_video, process_image
from utils import get_available_classes, get_model_description

st.set_page_config(page_title="🎯 Object Detection & Tracking", layout="wide")
st.title("🎯 Object Detection & Tracking (YOLOv8 + Deep SORT)")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
model_choice = st.sidebar.selectbox("YOLOv8 Model Variant", ["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"])
st.sidebar.info(get_model_description(model_choice))
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
deep_sort_enabled = st.sidebar.toggle("Enable Deep SORT Tracking", value=True)
class_filter = st.sidebar.multiselect("Filter by Classes (optional)", get_available_classes())
show_logs = st.sidebar.checkbox("Show Detection Log Console")

# Footer
st.sidebar.markdown("<hr style='margin-top: 40px; margin-bottom: 10px;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 14px;'>Developed by <b>Aryan Sengar</b></p>", unsafe_allow_html=True)

# Input
source_type = st.radio("📹 Select Input Type", ["Webcam", "Video File", "Image"])

if source_type == "Webcam":
    stframe = st.empty()
    run_btn = st.button("▶ Start Webcam")
    stop_btn = st.button("⏹ Stop")
    if run_btn:
        process_video(source=0, model_variant=model_choice, stframe=stframe,
                      use_deepsort=deep_sort_enabled, class_filter=class_filter,
                      show_fps=True, conf=confidence, show_logs=show_logs)

elif source_type == "Video File":
    uploaded_video = st.file_uploader("📤 Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_video:
        temp_video = tempfile.NamedTemporaryFile(delete=False)
        temp_video.write(uploaded_video.read())
        st.video(temp_video.name)

        if st.button("▶ Process Video"):
            output_path, object_count, logs = process_video(
                source=temp_video.name, model_variant=model_choice,
                use_deepsort=deep_sort_enabled, class_filter=class_filter,
                conf=confidence, show_logs=show_logs)
            st.success("✅ Processing Complete!")
            st.video(output_path)

            df = pd.DataFrame(list(object_count.items()), columns=["Class", "Count"])
            st.dataframe(df)
            st.download_button("📥 Download Summary CSV", df.to_csv(index=False), "summary.csv")

            with open(output_path, "rb") as f:
                st.download_button("⬇ Download Processed Video", f, file_name="processed_output.mp4")

            if show_logs and logs:
                st.expander("📋 Detection Log").code("\n".join(logs))

elif source_type == "Image":
    uploaded_image = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        file_bytes = uploaded_image.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), 1)
        st.image(image, channels="BGR", caption="Original Image", use_container_width=True)

        if st.button("🔍 Process Image"):
            processed_img, count, object_count, logs = process_image(
                image, model_variant=model_choice,
                use_deepsort=deep_sort_enabled, class_filter=class_filter,
                conf=confidence, show_logs=show_logs)
            st.image(processed_img, channels="BGR", caption=f"Detected Objects: {count}", use_container_width=True)

            df = pd.DataFrame(list(object_count.items()), columns=["Class", "Count"])
            st.dataframe(df)
            st.download_button("📥 Download Summary CSV", df.to_csv(index=False), "image_summary.csv")

            if show_logs and logs:
                st.expander("📋 Detection Log").code("\n".join(logs))