from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from app.logger import logger
from app.core.config import MINIO

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            edpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": edpoint_url
        }

        self.bucket_name = bucket_name
        self.session = get_session()


    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def bucket_check(self):
        async with self.get_client() as client:
            logger.debug(f"Проверяю есть ли Buckett = {self.bucket_name}")
            try:
                await client.head_bucket(Bucket=self.bucket_name)
                logger.debug(f"Bucket = {self.bucket_name} уже есть, отлично!")
            except:
                try:
                    logger.debug(f"Bucker = {self.bucket_name} не оказалось, создаю..")
                    await client.create_bucket(Bucket=self.bucket_name)
                    await client.head_bucket(Bucket=self.bucket_name)
                    logger.debug(f"Bucket = {self.bucket_name} успешно создан!")
                except Exception as e:
                    logger.error(f"Не удалось создать Bucket = {self.bucket_name}. {e}")
                    raise

    async def upload_file(
            self,
            file_data: bytes,
            file_name: str
    ):
        async with self.get_client() as client:
            try: 
                logger.debug(f"Получил данные пробую загрузить в Bucket = {self.bucket_name}")
                await client.put_object(
                    Bucket = self.bucket_name,
                    Body = file_data,
                    Key = file_name
                )
                logger.debug(f"Файл успешно загружен в S3, Bucket = {self.bucket_name}")
            except Exception as e:
                logger.error(f"Не удалось загрузить файл в S3.")
                raise

    async def download_file(
            self,
            minio_path
    ):
        async with self.get_client() as client:
            try:
                logger.debug(f"Получил путь пробую скачать файл из Bucket = {self.bucket_name}")
                response = await client.get_object(
                    Bucket = self.bucket_name,
                    Key = minio_path
                )
                logger.debug(f"Файл успешно скачан из Bucket = {self.bucket_name}")
                return response['Body'].read()
            except Exception as e:
                logger.debug(f"Не удалось скачать файл из Bucket = {self.bucket_name}")
                raise


s3_client_upload_to_detected = S3Client(
    MINIO.MINIO_ROOT_USER,
    MINIO.MINIO_ROOT_PASSWORD,
    MINIO.MINIO_ENDPOINT_URL,
    MINIO.MINIO_BUCKET_NAME_DETECTED
)

s3_client_download_frames = S3Client(
    MINIO.MINIO_ROOT_USER,
    MINIO.MINIO_ROOT_PASSWORD,
    MINIO.MINIO_ENDPOINT_URL,
    MINIO.MINIO_BUCKET_NAME_FRAMES
)
