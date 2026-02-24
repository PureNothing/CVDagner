import bentoml
from pathlib import Path
import io
from typing import Annotated, Dict, Any
from PIL import Image
from bentoml.validators import ContentType
from BentoService.config import CLASSES_MAP, FINETUNED_MAP


@bentoml.service(resources={'cpu': '2', 'memory': '4Gi'}, traffic={"timeout": 60})
class Detector:
    def __init__(self): 
        self.model = bentoml.picklable_model.load_model("yoloe_detector:latest")

        model_info = bentoml.models.get("yoloe_detector:latest")
        self.classes = model_info.info.metadata['classes']
        self.conf = model_info.info.metadata['conf_threshold']
        print(f"Уверенность модели: {self.conf}")

        #self.model.set_classes(self.classes)
    
    @bentoml.api
    def detect(self, image: Annotated[bytes, ContentType("image/*")]) -> Dict[str, Any]:
        try:
            pil_image = Image.open(io.BytesIO(image)).convert('RGB')
            results = self.model(pil_image, conf=self.conf)
            boxes = []
            labels = []
            scores = []

            if len(results[0].boxes) > 0:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    xyxy = box.xyxy[0].tolist()
                    boxes.append(xyxy)
                    #labels.append(CLASSES_MAP.get(self.classes[cls_id], self.classes[cls_id]))
                    labels.append(FINETUNED_MAP[cls_id])
                    scores.append(conf)
            else:
                return {
                    "success": True,
                    "boxes": boxes,
                    "labels": labels,
                    "scores": scores,
                    "message": "Ничего не найдено"
                }
            
            return {
                "success": True,
                "boxes": boxes,
                "labels": labels,
                "scores": scores,
                "message": "Найдены объекты"
            }
        
        
        except Exception as e:
            raise