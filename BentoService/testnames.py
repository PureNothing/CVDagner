import bentoml
from ultralytics import YOLO

model_ref = bentoml.models.get("yoloe_detector:latest")
model_path = model_ref.path_of("model.onnx")
model = YOLO(model_path)
print(model.names)