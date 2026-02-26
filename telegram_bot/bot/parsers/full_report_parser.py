from collections import defaultdict

def report_format_answer(response):
    most_danger_camera_stats = response["data"]["getGeneralReport"]["mostDangerousCameraIdAndStats"]
    all_cameras_stat = response["data"]["getGeneralReport"]["totalDetectionsAllTimeAllCameras"]
    status_overviev = response["data"]["getGeneralReport"]["statusOverviev"]

    if most_danger_camera_stats:
        most_d_c_s = ""
        most_d_c_id = 0
        for each in most_danger_camera_stats:
            most_d_c_s = most_d_c_s + f"- {each['label']} — {each['count']} шт.\n"
            most_d_c_id = each["cameraId"]

    if all_cameras_stat:
        all_cameras_dict = defaultdict(str)
        for each_row in all_cameras_stat:
            all_cameras_dict[int(each_row["cameraId"])] = all_cameras_dict[int(each_row["cameraId"])] + f"• {each_row['label']} — {each_row['count']} шт."



        text = (
            f"📹 Отчет по всем камерам\n"
            f"⚠️ Самая опасная камера {most_d_c_id}:\n"
            f"{most_d_c_s}"
            f"📊 Статистика по всем камерам\n"
            f"📷 Статистика 1 камеры:\n"
            f"{all_cameras_dict[1]}"
            f"📷 Статистика 2 камеры:\n"
            f"{all_cameras_dict[2]}"
            f"📷 Статистика 3 камеры:\n"
            f"{all_cameras_dict[3]}"
            f"📷 Статистика 4 камеры:\n"
            f"{all_cameras_dict[4]}"
            f"📷 Статистика 5 камеры:\n"
            f"{all_cameras_dict[5]}"
            f"🛡️ {status_overviev}\n"
            f"Если какие то камеры не указаны, значит на них ничего не было обнаружено."
            f"Если какие то объекты не указаны значит их не было обнаружено на камере."
        )
        return text
    else:
        text = (
            f"📭 Отчёт по всем камерам.\n"
            f"🟢 {status_overviev}"
        )
        return text