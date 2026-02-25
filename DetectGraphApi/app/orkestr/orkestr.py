from app.core.config import DETECOR_URL
from app.services.s3loadupload import s3_client_download_frames, s3_client_upload_to_detected
from app.services.dbfuncs import DBFuncs
from app.drawers.drawer import draw_box
from app.services.kafkaproducevideoserv import publish_video_produce_service
from app.services.kafkaproducealertserv import publish_alert_service
import aiohttp
import base64



async def orkerstr_func(minio_path: str, camera_id: int):

    orig_frame = await s3_client_download_frames.download_file(
        minio_path=minio_path)
    b64_frame = base64.b64encode(orig_frame)
    b64_frame = b64_frame.decode("utf-8")
    
    file_type = "jpeg"
    if "." in minio_path:
        file_type = minio_path.split(".")[-1]

    async with aiohttp.ClientSession() as session:
        async with session.post(DETECOR_URL, json = {"image": b64_frame}) as response:
            response.raise_for_status()
            dict_response = await response.json()
    
    uniq_name = None
        
    if len(dict_response["boxes"]) > 0:
    
        detected_img = draw_box(
            orig_frame,
            dict_response["boxes"],
            dict_response["labels"],
            dict_response["scores"])
        
        if "." in minio_path:
            end = minio_path.split(".")[-1]
            start = minio_path.split(".")[0]
            uniq_name = str(start) + "_detected." + str(end)
        else:
            uniq_name = str(minio_path) + "_detected"

        await s3_client_upload_to_detected.upload_file(
            file_data=detected_img,
            file_name=uniq_name
        )

    frame_id = await DBFuncs.insert_detected_frame(camera_id=camera_id,
                                            not_detected_minio_path=minio_path,
                                            detected_minio_path=uniq_name)
    
    if len(dict_response["boxes"]) > 0:

        for box, label, score in zip(dict_response["boxes"], dict_response["labels"], dict_response["scores"]):
            box_x1, box_y1, box_x2, box_y2 = box
            await DBFuncs.insert_detected_object(
                camera_id = camera_id,
                frame_id = frame_id,
                label = label,
                score = score,
                box_x1 = box_x1,
                box_y1 = box_y1,
                box_x2 = box_x2,
                box_y2 = box_y2
            )

        await publish_alert_service(detection_results = dict_response)
    
    await publish_video_produce_service(minio_path=minio_path)
