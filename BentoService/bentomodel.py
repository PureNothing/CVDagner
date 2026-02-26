import bentoml
from ultralytics import YOLOE, YOLO
import shutil
from config import CLASSES, confidence_threshold

#model = YOLOE("yoloe-26x-seg.pt")
#model.save("yoloe-26x-seg.pt") - далее передаем этот путь в код ниже.
#model = YOLO("BentoService/runs/train/yolo_finetuned/weights/best.pt")
#model = YOLO("BentoService/FineTune/KaggleModel/map761e36.pt")
#model = YOLO("BentoService/FineTune/KaggleModel/map823e50.onnx")

with bentoml.models.create(
    name="yoloe_detector",
    metadata={
        "classes": CLASSES,
        "input_size": 640,
        "conf_threshold": confidence_threshold
    }
) as model_ref:
    shutil.copy("BentoService/FineTune/KaggleModel/map823e50.onnx",
                model_ref.path_of("model.onnx"))
    print(f"Model saved: {model_ref}")



"""saved_model = bentoml.picklable_model.save_model(
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

print(f"Model saved: {saved_model}")"""