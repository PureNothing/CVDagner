import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.core.kafkabroker import broker
from contextlib import asynccontextmanager
from app.logger import logger
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
class SingleCameraReport:
    camera_id: strawberry.ID
    last_description_time: str
    people_count_row: int
    is_weapon_detected: bool

@strawberry.type
class GeneralDailyReport:
    total_alerts_24h: int
    most_dangerous_camera_id: int
    status_overviev: str


@strawberry.type
class Query:
    @strawberry.field
    def get_camera_report(self, camera_id: int) -> SingleCameraReport:
        if camera_id == 1:
            return SingleCameraReport(
                camera_id=strawberry.ID("1"),
                last_description_time="2024-01-15 14:03:25",
                people_count_row=3,
                is_weapon_detected=True
            )
    
    @strawberry.field
    def get_general_report(self) -> GeneralDailyReport:
        return GeneralDailyReport(
            total_alerts_24h=10,
            most_dangerous_camera_id=1,
            status_overviev="Камера 1: 3 человека, оружия нет."
        )


schema = strawberry.Schema(query=Query)
router = APIRouter(lifespan=lifespawn)
router.include_router(GraphQLRouter(schema=schema, graphql_ide=True), prefix="/graphql")