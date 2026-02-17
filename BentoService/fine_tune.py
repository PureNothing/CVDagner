from ultralytics import YOLOE
from ultralytics.models.yolo.yoloe import YOLOEPETrainer

# Загружаем предобученную модель
model = YOLOE("yoloe-26x-seg.pt")

# Запускаем дообучение
model.train(
    data="yolo_dataset/dataset.yaml",  # путь к твоему dataset.yaml
    epochs=50,                          # количество эпох
    batch=8,                             # размер батча (уменьши до 4, если мало памяти)
    imgsz=640,                            # размер картинок
    trainer=YOLOEPETrainer,                # линейное зондирование (быстро)
    lr0=1e-3,                              # начальная скорость обучения
    device="cpu",                               # GPU (если есть)
    project="runs/train",                   # куда сохранять результаты
    name="yoloe_finetuned"                   # имя эксперимента
)

print("✅ Обучение завершено!")