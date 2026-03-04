import bentoml
from ultralytics import YOLOE, YOLO
import shutil
from config import CLASSES, confidence_threshold

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



