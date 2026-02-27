from app.dbmodels.dbmodel import Detected_frames, Detected_objects
from app.core.dbengine import async_session, engine, Base
from app.logger import logger
from sqlalchemy import text, insert, select, func

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

    @staticmethod
    async def get_single_camera_labels(
        camera_id: int,
    ):
        try:
            logger.debug(f"Получил запрос на получение информации с камеры = {camera_id}. Обрабатываю..")
            async with async_session() as session:
                stmt = select(Detected_objects.label, func.count(Detected_objects.label)).where(
                    text("detected_at > now() - INTERVAL '24 hours'")
                ).where(Detected_objects.camera_id==camera_id).group_by(Detected_objects.label)
                response = await session.execute(statement=stmt)
                rows = response.all()
                logger.debug(f"Отчет по объектам камеры = {camera_id} успешно полчен.")
                return rows
        except Exception as e:
            logger.error(f"Не вышло обработать запрос на возрат данные по камере = {camera_id}. {e}")

    @staticmethod
    async def get_singe_camera_last_detect(
        camera_id: int
    ):
        try:
            logger.debug(f"Получен запрос на время последней детекции камеры = {camera_id}.")
            async with async_session() as session:
                stmt = select(Detected_objects.detected_at).where(
                    Detected_objects.camera_id == camera_id).order_by(
                        Detected_objects.detected_at.desc()
                    ).limit(1)
                response = await session.execute(statement=stmt)
                last_time = response.scalar_one_or_none()
                logger.debug(f"Последние время детекции камеры = {camera_id} получены.")
                return last_time
        except Exception as e:
            logger.error(f"Не удалось получить последнее время детекции для камеры = {camera_id}. {e}")

    @staticmethod
    async def get_most_dangerous_camera_and_stats():
        try:
            logger.debug(f"Пришел запрос узнать самую опасную камреу, обрабатываю..")
            async with async_session() as session:

                substmt = select(Detected_objects.camera_id).group_by(Detected_objects.camera_id).order_by(
                    func.count(Detected_objects.label).desc()).limit(1).scalar_subquery()
                
                stmt = select(Detected_objects.camera_id, Detected_objects.label, func.count(Detected_objects.detected_at)).where(
                    Detected_objects.camera_id == substmt).group_by(
                    Detected_objects.label, Detected_objects.camera_id)
                
                result = await session.execute(statement=stmt)
                most_danger_camera_and_stat = result.all()
                logger.debug(f"Самая опасная камера и ее статистика успешно узнана, отправляю.")
                return most_danger_camera_and_stat
        except Exception as e:
            logger.error(f"Ошибка обработки запроса по самой опасной камере. {e}")

    @staticmethod
    async def get_every_camera_labels_and_count():
        try:
            logger.debug(f"Пришел запрос на статистику по всем камерам за всё время, обрабатываю..")
            async with async_session() as session:
                stmt = select(Detected_objects.camera_id, Detected_objects.label, func.count(Detected_objects.label)).group_by(
                    Detected_objects.camera_id, Detected_objects.label)
                result = await session.execute(statement=stmt)
                all_rows = result.all()
                logger.debug(f"Статистика по всем камерам и объектам на них, успешно получена")
                return all_rows
        except Exception as e:
            logger.error(f"Не вышло предоставить отчет по всем камерам. {e}")









        
                    


                

        
                    


                


