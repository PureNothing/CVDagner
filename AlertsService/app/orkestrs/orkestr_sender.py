from app.funcs.get_rules import get_rules_func
from collections import defaultdict
from app.services.kafkaproducebot import kafka_send

async def orkestr_func(detection_results: dict, camera_id: int):
    camera_rules = await get_rules_func(camera_id = camera_id)
    labels_dict = defaultdict(int)
    for label in detection_results.labels:
        labels_dict[label] = labels_dict[label] + 1
    
    for label, thresholds in camera_rules.items():
        threshold = thresholds["threshold"]
        for label_dict, count_label in labels_dict.items():
            if label_dict == label and count_label >= threshold:
                await kafka_send(camera_id = camera_id, label = label_dict, count = count_label)
            else:
                continue
