from collections import defaultdict

def report_format_answer(response, cor_plc):
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
            all_cameras_dict[int(each_row["cameraId"])] = all_cameras_dict[int(each_row["cameraId"])] + f"• {each_row['label']} — {each_row['count']} шт.\n"



        text = (
            f"📹 Отчет по всем камерам\n"
            f"⚠️ Самая опасная камера {most_d_c_id}:\n\n"
            f"{most_d_c_s}\n"
            f"📊 Статистика по всем камерам\n"
            f"📷 Статистика 1 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[0][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[0][1]}\n\n"
            f"{all_cameras_dict[1]}\n\n"
            f"📷 Статистика 2 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[1][0]}"
            f"🏔️ Местность:\n"
            f"{cor_plc[1][1]}\n"
            f"{all_cameras_dict[2]}\n\n"
            f"📷 Статистика 3 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[2][0]}"
            f"🏔️ Местность:\n"
            f"{cor_plc[2][1]}\n"
            f"{all_cameras_dict[3]}\n\n"
            f"📷 Статистика 4 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[3][0]}"
            f"🏔️ Местность:\n"
            f"{cor_plc[3][1]}\n"
            f"{all_cameras_dict[4]}\n\n"
            f"📷 Статистика 5 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[4][0]}"
            f"🏔️ Местность:\n"
            f"{cor_plc[4][1]}\n"
            f"{all_cameras_dict[5]}\n\n"
            f"🛡️ {status_overviev}\n"
            f"Если какие то камеры не указаны, значит на них ничего не было обнаружено."
            f"Если какие то объекты не указаны значит их не было обнаружено на камере."
        )
        return text
    else:
        text = (
            f"📭 Отчёт по всем камерам.\n"
            f"📷 Статистика 1 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[0][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[0][1]}\n"
            f"📷 Статистика 2 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[1][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[1][1]}\n\n"
            f"📷 Статистика 3 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[2][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[2][1]}\n\n"
            f"📷 Статистика 4 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[3][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[3][1]}\n\n"
            f"📷 Статистика 5 камеры:\n"
            f"📍 Коордианаты:\n"
            f"{cor_plc[4][0]}\n\n"
            f"🏔️ Местность:\n"
            f"{cor_plc[4][1]}\n\n"
            f"🟢 {status_overviev}\n"
            f"Если какие то камеры не указаны, значит на них ничего не было обнаружено."
            f"Если какие то объекты не указаны значит их не было обнаружено на камере."
        )
        return text