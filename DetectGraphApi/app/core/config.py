from dotenv import load_dotenv
import os
import sys
from app.logger import logger
load_dotenv()


def check_env():
    logger.debug("="*20)
    logger.debug("ЗАПУСК")
    logger.debug("Начинаю проверку необходимых переменных..")
    must_have = [
        "MINIO_ROOT_USER",
        "MINIO_ROOT_PASSWORD",
        "MINIO_ENDPOINT_URL",
        "MINIO_BUCKET_NAME_FRAMES",
        "MINIO_BUCKET_NAME_DETECTED",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT"
    ]

    for env in must_have:
        try:
            os.environ[env]
        except Exception as e:
            logger.critical(f"Перемення {env} не найдена, не могу работать. {e}")
            sys.exit(1)



class MINIO:
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
    MINIO_BUCKET_NAME_FRAMES = os.getenv("MINIO_BUCKET_NAME_FRAMES")
    MINIO_BUCKET_NAME_DETECTED = os.getenv("MINIO_BUCKET_NAME_DETECTED")

class DB:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

KAFKA_URL = "localhost:9092"
DETECOR_URL = "http://localhost:7777/detect"




