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

"""
pehota (155).jpg
pehota (320).jpg
pehota (44).jpg
"pehota%20(320).jpg",19.9673735725938,47.79834312080537,233.0309951060359,153.97283976510067,"btr"
"pehota%20(44).jpg",94.10114192495921,20.81048201107011,179.8727569331158,170.27173662361625,"pehota"
"rszo%20(155).jpg",8.711256117455138,9.942569524913093,221.70146818923328,186.1789542294322,"rszo"
"""