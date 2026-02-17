import bentoml
from ultralytics import YOLOE
from config import CLASSES, confidence_threshold

model = YOLOE("yoloe-26x-seg.pt")

saved_model = bentoml.picklable_model.save_model(
    "yoloe_detector",
    model,
    labels={
        "framework": "ultralytics",
        "type": "yoloe",
        "task": "detection"
    },
    metadata={
            "classes": CLASSES,
            "input_size": 640,
            "conf_threshold": confidence_threshold
    }
)

print(f"Model saved: {saved_model}")