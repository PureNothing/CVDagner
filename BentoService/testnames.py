import bentoml
model = bentoml.picklable_model.load_model("yoloe_detector:latest")
print(model.names)