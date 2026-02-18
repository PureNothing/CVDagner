import bentoml
from ultralytics import YOLOE, YOLO
from config import CLASSES, confidence_threshold

#model = YOLOE("yoloe-26x-seg.pt")
#model = YOLO("BentoService/runs/train/yolo_finetuned/weights/best.pt")
model = YOLO("BentoService/FineTune/KaggleModel/map761e36.pt")

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