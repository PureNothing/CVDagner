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
            f"📍 Координаты:\n"
            f"{response_coordinates}\n\n"
            f"🏔️ Местность:\n"
            f"{response_place}\n\n"
            f"🕐 Последнее обнаружение: {last_detection_time}\n"
            f"📊 Обнаруженные объекты:\n"
            f"{object_text}\n"
            f"✅ {description}"
        )
    
    else:
        text = (
            f"✅ {camera_id_report}\n"
            f"📍 Координаты:\n"
            f"{response_coordinates}\n\n"
            f"🏔️ Местность:\n"
            f"{response_place}\n"
            f"{description}"
        )

    return text