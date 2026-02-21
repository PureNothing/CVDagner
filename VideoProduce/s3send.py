from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from logger import logger
from config import MINIO

class S3Client:
    def __init(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def bucket_check(self):
        async with self.get_client() as client:
            logger.debug("Проверяю есть ли Bucket..")
            try:
                await client.head_bucket(Bucket=self.bucket_name)
                logger.debug("Bucket уже есть, отлично!")
            except:
                try:
                    logger.debug("Bucket не оказалось, создаю..")
                    await client.create_bucket(Bucket=self.bucket_name)
                    await client.head_bucket(Bucket=self.bucket_name)
                    logger.debug(f"Bucket с именем {self.bucket_name} успешно создан!")
                except Exception as e:
                    logger.error("Не удалось создать Bucket!")
                    raise

    async def upload_file(
            self,
            file_data: bytes,
            file_name: str
    ):
        async with self.get_client() as client:
            try:
                logger.debug("Получил данные пробую загрузить")
                await client.put_object(
                    Bucket = self.bucket_name,
                    Body = file_data,
                    Key = file_name
                )
                logger.debug("Файл успешно загружен в S3")
            except Exception as e:
                logger.error("Не удалось загрузить файл в S3")
                raise

s3_client_videos = S3Client(
    MINIO.MINIO_ROOT_USER,
    MINIO.MINIO_ROOT_PASSWORD,
    MINIO.MINIO_ENDPOINT_URL,
    MINIO.VIDEOS_BUCKET
)

s3_client_frames = S3Client(
    MINIO.MINIO_ROOT_USER,
    MINIO.MINIO_ROOT_PASSWORD,
    MINIO.MINIO_ENDPOINT_URL,
    MINIO.FRAMES_BUCKET
)


