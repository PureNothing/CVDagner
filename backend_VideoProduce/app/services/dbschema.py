from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, text, insert, update, select, func, ForeignKey
import datetime
from typing import Annotated
from app.core.config import BD
from app.logger import logger

intpk = Annotated[int, mapped_column(primary_key=True)]
s_time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

engine = create_async_engine(
    url=BD.DB_URL,
    echo = False,
    pool_size = 5,
    max_overflow = 10
)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Videos(Base):
    __tablename__ ="videos"

    id: Mapped[intpk]
    uploaded_at: Mapped[s_time]
    minio_path: Mapped[str]
    camera_id: Mapped[int]

    frames: Mapped[list["Frames"]] = relationship(back_populates="video")   

class Frames(Base):
    __tablename__ = "frames"

    id: Mapped[intpk]
    created_at: Mapped[s_time]
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id", ondelete='CASCADE'))
    minio_path: Mapped[str]
    camera_id: Mapped[int]
    status: Mapped[str] = mapped_column(server_default="not_processed")

    video: Mapped["Videos"] = relationship(back_populates="frames", foreign_keys=[video_id])


class DBCORE:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            logger.debug("Удаляю все Таблицы..")
            await conn.run_sync(Base.metadata.drop_all)
            logger.debug("Создаю новые..")
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Таблицы успено созданы!")

    @staticmethod
    async def insert_videos(
        minio_path, 
        camera_id,
    ):
        logger.debug("Получены данные о видео, отправляю в БД..")
        try:
            async with async_session() as session:
                stmt = insert(Videos).values(
                    minio_path=minio_path,
                    camera_id=camera_id).returning(Videos.id)
                video_id = await session.execute(stmt)
                video_id = video_id.scalar_one()
                await session.commit()

                logger.debug("Видео успешно загружено возвращаю id")

                return video_id
        except Exception as e:
            logger.error(f"Не удалось загрузить информацю о видео в БД. {e}")
            raise

    @staticmethod
    async def insert_frames(
        video_id,
        minio_path,
        camera_id
    ):
        try:
            logger.debug("Получена ифна о фрейме, гружу в БД..")
            async with async_session() as session:
                stmt = insert(Frames).values(
                    minio_path=minio_path,
                    camera_id=camera_id,
                    video_id=video_id
                )
                await session.execute(stmt)
                await session.commit()

                logger.debug("Инфа о фрейме успешно загружена в БД!")
        except Exception as e:
            logger.error(f"Не удалось загрузить инфу о фрейме в БД. {e}")
            raise

    @staticmethod
    async def update_status_frames(
        minio_path
    ):
        try:
            logger.debug("Получил из очереди о том что фрейм детектирован, обновляю статус..")
            async with async_session() as session:
                stmt = update(Frames).where(Frames.minio_path == minio_path).values(status = "processed")
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.error(f"Ошибка обновления статуса детектированного фрейма. {e}")
        
                    


                


