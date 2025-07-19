def get_model_description(name):
    descriptions = {
        "yolov8n": "YOLOv8n (nano): Fastest, low accuracy, ideal for CPU/webcam.",
        "yolov8s": "YOLOv8s (small): Balanced for speed and accuracy.",
        "yolov8m": "YOLOv8m (medium): Better accuracy, slightly slower.",
        "yolov8l": "YOLOv8l (large): High accuracy, GPU recommended.",
        "yolov8x": "YOLOv8x (xlarge): Best accuracy, needs powerful GPU."
    }
    return descriptions.get(name, "Model variant not recognized.")

def get_available_classes():
    return ["person", "car", "bicycle", "motorcycle", "bus", "truck", "cat", "dog", "bottle"]