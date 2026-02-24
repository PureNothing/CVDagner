from dotenv import load_dotenv
import os
from app.logger import logger
import sys
load_dotenv()

class MINIO:
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
    VIDEOS_BUCKET = os.getenv("MINIO_BUCKET_NAME_VIDEOS")
    FRAMES_BUCKET = os.getenv("MINIO_BUCKET_NAME_FRAMES")

class BD:
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

KAFKA_URL = "localhost:9092"

def check_env():
    logger.debug("="*20)
    logger.debug("ЗАПУСК")
    logger.debug("Начинаю проверку необходимых переменных..")
    must_have = [
            "MINIO_ROOT_USER",
            "MINIO_ROOT_PASSWORD",
            "MINIO_ENDPOINT_URL",
            "MINIO_BUCKET_NAME_VIDEOS",
            "MINIO_BUCKET_NAME_FRAMES",
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_DB"
        ]
    for env in must_have:
        try:
            os.environ[env]
        except Exception as e:
            logger.critical(f"Переменная {env} отсутствует, не могу начать работу. {e}")
            sys.exit(1)