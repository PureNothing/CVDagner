По умолчанию Bento Service работает на yoloe-26x-seg.pt
При использованний базовой модели:
1. self.model.set_classes(self.classes) ракоментировать эту строчку в modelservice.py
2. labels.append(CLASSES_MAP.get(self.classes[cls_id], self.classes[cls_id])) - раскоментировать эт строчку в modelservice.py


Fine-Tune:
1. Загрузить нужные картинки в images/train
2. Загрузить нужный CSV в yolo_dataset/csv
3. Заменить классы в conver_csv_to_yolo.py в переменной label_map на ваши.
4. Заменить классы в dataset.yaml на ваши.
3. uv run BentoService/FineTune/convert_csv_to_yolo.py
4. uv run BentoService/FineTune/fine_tune.py
5. Дождаться конца обучения, зайти в папку runs->yolo_finetuned->weights->best.pt
6. Заменить модель в BentoService везде на best.pt
7. Либо раскоментировать просто готовые строки которые сами заберут лучшую модель.
8. uv run BentoService/bentomodel.py

Локальный запуск:
1. cd BentoService
2. uv run bentoml modelservice.py:YOLOEDetecot
