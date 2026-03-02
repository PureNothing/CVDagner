def format_answer(response, response_coordinates, response_place):
    camera_id_report = response["data"]["getCameraReport"]["cameraIdReport"]
    last_detection_time = response["data"]["getCameraReport"]["lastDescriptionTime"]
    objects_summary = response["data"]["getCameraReport"]["objectsSummary"]
    is_danger_detected = response["data"]["getCameraReport"]["isDangerDetected"]
    description = response["data"]["getCameraReport"]["statusCamera"]

    if is_danger_detected:
        
        object_text = ""
        for obj in objects_summary:
                object_text = object_text + f"• {obj['label']} — {obj['count']} шт.\n"

        text = (
            f"🚨 {camera_id_report}\n"
            f"📍 Координаты:"
            f"{response_coordinates}"
            f"🏔️ Местность:"
            f"{response_place}\n"
            f"🕐 Последнее обнаружение: {last_detection_time}\n"
            f"📊 Обнаруженные объекты:\n"
            f"{object_text}"
            f"✅ {description}"
        )
    
    else:
        text = (
            f"✅ {camera_id_report}\n"
            f"📍 Координаты:"
            f"{response_coordinates}"
            f"🏔️ Местность:"
            f"{response_place}\n"
            f"{description}"
        )

    return text