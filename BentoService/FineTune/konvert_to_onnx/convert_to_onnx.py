from ultralytics import YOLOE

model = YOLOE("BentoService/FineTune/KaggleModel/map823e50.pt")
model.export(format = "onnx", imgsz = 640)