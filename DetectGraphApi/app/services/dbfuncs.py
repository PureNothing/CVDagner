from app.dbmodels.dbmodel import Detected_frames, Detected_objects
from app.core.dbengine import async_session, engine, Base
from app.logger import logger
from sqlalchemy import text, insert

class DBFuncs:

    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            logger.debug("Создаю схему, удаляю таблицы, создаю новые..")
            try:
                logger.debug("Создаю схему DetectionService если её нет..")
                await conn.execute(text('CREATE SCHEMA IF NOT EXISTS "DetectionService"'))
                logger.debug("Схема успешно создана.")
                logger.debug("Удаляю таблицы..")
                await conn.run_sync(Base.metadata.drop_all)
                logger.debug("Таблицы удалены успешно.")
                logger.debug("Создаю новые таблицы..")
                await conn.run_sync(Base.metadata.create_all)
                logger.debug("Таблицы (Detected_frames), (Deteted_objects) успешно созданы БД готов к работе.")
            except Exception as e:
                logger.error(f"Не удалось инициализировать БД готовую к работе. {e}")
                raise

    @staticmethod
    async def insert_detected_frame(
        camera_id,
        not_detected_minio_path,
        detected_minio_path
    ):
        logger.debug("Получен обработанной фрейм пробую вставить данные о нем в БД..")

        try:
            async with async_session() as session:

                stmt = insert(Detected_frames).values(
                    camera_id=camera_id,
                    not_detected_minio_path = not_detected_minio_path,
                    detected_minio_path = detected_minio_path).returning(Detected_frames.id)
                
                response = await session.execute(statement=stmt)
                frame_id = response.scalar_one()
                await session.commit()

                logger.debug("Данные о детектерированном фрейме успешно загружены в БД возвращаю его id.")

                return frame_id
        except Exception as e:
            logger.error(f"Не удалось загрузить фрейм в БД. {e}")
            raise
    
    @staticmethod
    async def insert_detected_object(
        camera_id,
        frame_id,
        label,
        score,
        box_x1,
        box_y1,
        box_x2,
        box_y2
    ):
        logger.debug("Полученные данные о детектированном объекте, гружу в БД...")
        try:
            async with async_session() as session:

                stmt = insert(Detected_objects).values(
                    camera_id = camera_id,
                    frame_id = frame_id,
                    label = label,
                    score = score,
                    box_x1 = box_x1,
                    box_y1 = box_y1,
                    box_x2 = box_x2,
                    box_y2 = box_y2
                )

                await session.execute(statement=stmt)
                await session.commit()

                logger.debug("Данные о детектированном объекте успешно загружены в БД.")
        except Exception as e:
            logger.error(f"Не удалось загрузить данные о детектированном объекте в БД {e}")
            raise









        
                    


                

        
                    


                


