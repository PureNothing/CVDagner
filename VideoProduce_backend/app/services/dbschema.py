from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, text, insert, update, select, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
import datetime
from datetime import timezone
from typing import Optional, Annotated
from config import BD
from logger import logger

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
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), ondelete='CASCADE')
    minio_path: Mapped[str]
    camera_id: Mapped[int] 

    video: Mapped["Videos"] = relationship(back_populates="frames", foreign_keys=[video_id])


class BDCORE:
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
        video_name, 
        minio_path, 
        camera_id,
        frames):
        logger.debug("Получены данные о видео, отправляю в БД..")
        try:
            async with async_session() as session:
                stmt = insert(Videos).values(
                    minio_path=minio_path,
                    camera_id=camera_id).returning(Videos.id)
                v_id = session.execute(stmt)

                for index, frame in enumerate(frames):
                    


                


