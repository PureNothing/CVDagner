from ultralytics import YOLOE
from ultralytics.models.yolo.yoloe import YOLOEPETrainer

model = YOLOE("yoloe-26x.yaml")
model.load("BentoService/yoloe-26x-seg.pt")

model.train(
    data="BentoService/FineTune/dataset.yaml",  
    epochs=1,                         
    batch=8,                             
    imgsz=640,                            
    trainer=YOLOEPETrainer,                
    lr0=1e-3,                              
    device="cpu",                               
    project="BentoService/runs/train",                   
    name="yoloe_finetuned"                   
)

print("✅ Обучение завершено!")

