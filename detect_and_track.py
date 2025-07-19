import cv2
import numpy as np
import time
from ultralytics import YOLO

def process_video(source, model_variant, conf=0.5, stframe=None, use_deepsort=False,
                  class_filter=None, show_fps=True, show_logs=False):
    model = YOLO(f"{model_variant}.pt")
    cap = cv2.VideoCapture(source)
    width, height = int(cap.get(3)), int(cap.get(4))
    out_path = "output_processed.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))

    object_count = {}
    logs = []
    prev_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, conf=conf)[0]
        detections = results.boxes.data.cpu().numpy()

        for det in detections:
            x1, y1, x2, y2, confidence, cls = map(int, det[:6])
            class_name = model.names[int(cls)]
            if not class_filter or class_name in class_filter:
                object_count[class_name] = object_count.get(class_name, 0) + 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                if show_logs:
                    logs.append(label)

        if show_fps:
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        out.write(frame)
        if stframe:
            stframe.image(frame, channels="BGR", use_container_width=True)

    cap.release()
    out.release()
    return out_path, object_count, logs

def process_image(image, model_variant, use_deepsort=False, class_filter=None, conf=0.5, show_logs=False):
    model = YOLO(f"{model_variant}.pt")
    results = model.predict(image, conf=conf)[0]
    detections = results.boxes.data.cpu().numpy()
    object_count = {}
    logs = []
    count = 0

    for det in detections:
        x1, y1, x2, y2, confidence, cls = map(int, det[:6])
        class_name = model.names[int(cls)]
        if not class_filter or class_name in class_filter:
            count += 1
            object_count[class_name] = object_count.get(class_name, 0) + 1
            label = f"{class_name} {confidence:.2f}"
            logs.append(label)
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return image, count, object_count, logs