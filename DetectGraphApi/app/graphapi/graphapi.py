import strawberry
from fastapi import APIRouter
from typing import Optional
import datetime
from strawberry.fastapi import GraphQLRouter
from app.core.kafkabroker import broker
from contextlib import asynccontextmanager
from app.logger import logger
from collections import defaultdict
from app.services.dbfuncs import DBFuncs
from app.services.s3loadupload import s3_client_download_frames, s3_client_upload_to_detected

@asynccontextmanager
async def lifespawn(router):
    try:
        logger.debug("Проверяю Bucket, создаю таблицы и схемы в БД..")
        await DBFuncs.create_tables()
        await s3_client_upload_to_detected.bucket_check()
        await s3_client_download_frames.bucket_check()
        logger.debug("БД и S3 успешно инициализированы и готовы к работе.")
    except Exception as e:
        logger.error(f"Ошибка иницилазиции БД или S3")
        raise
    try:
        logger.debug("Открываю TCP соединение с Kafka...")
        await broker.start()
        logger.debug("TCP соединение с Kafka успешно открыто.")
    except Exception as e:
        logger.error(f"Не удалось открыть TCP соединение с Kafka. {e}")
        raise
    yield
    try:
        logger.debug("Закрываю соединения Kafka, завершаю работу...")
        await broker.stop()
        logger.debug("Соединения закрыты работа заверешена успешно.")
        logger.debug("="*20)
    except Exception as e:
        logger.error(f"Не удалось закрыть соединение и завершить работу. {e}")



@strawberry.type
class ObjectsCount:
    label: str
    count: int

@strawberry.type
class SingleCameraReport:
    camera_id_report: str
    last_description_time: Optional[datetime.datetime] = None
    objects_summary: Optional[list[ObjectsCount]] = None
    is_danger_detected: bool
    status_camera: Optional[str] = None

######

@strawberry.type
class CameraLabelsSCountRow:
    camera_id: int
    label: str
    count: int

@strawberry.type
class GeneralDailyReport:
    most_dangerous_camera_id_and_stats: Optional[list[CameraLabelsSCountRow]] = None
    total_detections_all_time_all_cameras: Optional[list[CameraLabelsSCountRow]] = None
    status_overviev: str
    is_danger_detected: bool

#####

@strawberry.type
class Query:
    @strawberry.field
    async def get_camera_report(self, camera_id: int) -> SingleCameraReport:
        count_labels = await DBFuncs.get_single_camera_labels(camera_id=camera_id)
        last_detect_time = await DBFuncs.get_singe_camera_last_detect(camera_id=camera_id)
        
        if count_labels:
            obejects_list = []
            for count_label in count_labels:
                obejects_list.append(ObjectsCount(label=count_label[0], count=count_label[-1]))

            return SingleCameraReport(
                camera_id_report=f"Отчет по камере = {camera_id}",
                last_description_time=last_detect_time,
                objects_summary=obejects_list,
                is_danger_detected=True,
                status_camera="Отчет по камере за 24 часа предостален."            
            )
        else:
            return SingleCameraReport(
                camera_id_report=f"Отчет по камере = {camera_id}",
                is_danger_detected=False,
                status_camera="Опасностей за последние 24 часа не обраружено."
            )

    
    @strawberry.field
    async def get_general_report(self) -> GeneralDailyReport:
        all_cameras_and_labels = await DBFuncs.get_every_camera_labels_and_count()
        most_dang_camera_stat = await DBFuncs.get_most_dangerous_camera_and_stats()

        if all_cameras_and_labels:
            all_cameras_and_labels_dict = defaultdict(list)
            all_camers_and_labels_cls = list()

            for every_camera_and_label in all_cameras_and_labels:
                all_cameras_and_labels_dict[every_camera_and_label[0]].append({every_camera_and_label[1]: every_camera_and_label[-1]})
            for camera_id, labels_counts in all_cameras_and_labels_dict.items():
                    for labels_counts_dict in labels_counts:
                        for label, count in labels_counts_dict.items():
                            all_camers_and_labels_cls.append(CameraLabelsSCountRow(camera_id=camera_id, label=label, count=count))
        
        else: 
            return GeneralDailyReport(
                status_overviev="Ничего и никогда не было обнаружено ни на одной камере.",
                is_danger_detected=False
            )
        
        if most_dang_camera_stat:
            most_dang_camera_stat_cls = list()
            
            for camera_id, label, count in most_dang_camera_stat:
                        most_dang_camera_stat_cls.append(CameraLabelsSCountRow(camera_id=camera_id, label=label, count=count))

        else:
            return GeneralDailyReport(
                status_overviev="Ничего и никогда не было обнаружено ни на одной камере.",
                is_danger_detected=False
            )


        return GeneralDailyReport(
            total_detections_all_time_all_cameras=all_camers_and_labels_cls,
            most_dangerous_camera_id_and_stats=most_dang_camera_stat_cls,
            status_overviev="Обнаружены угрозы. Предоставлена самая опасная камера, её статистика и статистика по всем камерам.",
            is_danger_detected=True
        )


schema = strawberry.Schema(query=Query)
router = APIRouter(lifespan=lifespawn)
router.include_router(GraphQLRouter(schema=schema, graphql_ide=True), prefix="/graphql")