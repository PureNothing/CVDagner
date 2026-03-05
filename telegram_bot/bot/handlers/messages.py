from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BufferedInputFile, URLInputFile
from bot.keyboards.buttons import home_kb
from bot.handlers.states import Settings
from aiogram.fsm.context import FSMContext
import aiohttp
from bot.core.config import AI_THRESHOLD_URL, AI_NEW_CAMERA_URL
from bot.logger import logger

router = Router()

@router.message(F.text == "🏠 Главное меню")
async def home(message: Message):
    await message.answer("🧿 Какую информацию предоставить?", reply_markup=home_kb)


@router.message(F.text == "❓ Помощь")
async def help(message: Message):
    await message.answer(
        f"📋 <b>Справка по системе CVDanger</b>\n\n"

        f"🔒 <b>О системе</b>\n"
        f"Система автоматически анализирует видео с камер наблюдения в реальном времени. "
        f"При обнаружении военной техники или пехоты — немедленно уведомляет и принимает тактическое решение через AI агента.\n\n"

        f"🖱 <b>Отчёты по камерам</b>\n"
        f"Нажмите <b>🏠 Главное меню</b> внизу экрана:\n"
        f"  • <b>📹 Камера 1–5</b> — детекции за последние 24 часа: что обнаружено, сколько, когда\n"
        f"  • <b>📊 Полный отчёт</b> — агрегированная статистика по всем камерам за всё время\n\n"

        f"🔔 <b>Алерты в реальном времени</b>\n"
        f"При превышении порога бот уведомит автоматически — с указанием камеры, координат, местности и количества объектов. "
        f"Следом придёт решение AI агента: дрон или авиаудар.\n\n"

        f"⏰ <b>Автоматический доклад</b>\n"
        f"Каждые 10 минут система собирает данные по всем камерам и отправляет аналитический доклад с оценкой обстановки и рекомендациями.\n\n"

        f"⚙️ <b>Настройки</b>\n"
        f"Откройте меню слева → команда <b>/settings</b> → введите секретный ключ:\n"
        f"  • <b>🔔 Сменить порог алертов</b> — напишите в свободной форме, например: <i>«на второй камере для танков поставь порог три»</i>\n"
        f"  • <b>📷 Добавить камеру</b> — напишите в свободной форме, например: <i>«добавь камеру 6, координаты 48.5 и 37.9, жилой район»</i>\n\n"

        f"🔄 <b>Если кнопки внизу пропали</b>\n"
        f"Нажмите <b>/start</b> в левом меню — они появятся снова.\n\n"

        f"🆔 <b>Ваши данные</b>\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Username: @{message.from_user.username}\n\n"

        f"☝️ Система уже наблюдает. Вы только читаете справку.",
        parse_mode="HTML"
    )

@router.message(Settings.waiting_threshold)
async def save_threshold(message: Message, state: FSMContext):
    try:
        logger.debug(f"Пришло собщение от пользователя на замену порога - {message.text}.")
        async with aiohttp.ClientSession() as session:
            async with session.post(url=AI_THRESHOLD_URL, json={"message": message.text}) as response:
                result = await response.json()
        if response.status == 400:
            await message.answer(f"❌ {result['status']}")
        else:
            await message.answer(f"✅ Доставлено в сервис настроек: {result['status']}")
        await state.clear()
    except Exception as e:
        logger.error("Ошибка при изменении порога..")
        await message.answer("❌ Не понял. Переформулируйте.")

@router.message(Settings.waiting_newcamera_settings)
async def new_camera(message: Message, state: FSMContext):
    try:
        logger.debug(f"Пришло сообщение от пользователя на замену камеры в бота - {message.text} отправляю в AI.")
        async with aiohttp.ClientSession() as session:
            async with session.post(url=AI_NEW_CAMERA_URL, json={"message": message.text}) as response:
                result = await response.json()
        
        await message.answer(f"✅ Камера добавлена {result['status']}")
        await state.clear()
    except Exception as e:
        logger.error("Ошибка при доабвлении камеры.")
        await message.answer("❌ Не понял, переформулируйте запрос.")





@router.message()
async def unknown_message(message: Message):
    await message.answer(
        "⚠️ Неизвестная команда.\n"
        "Используйте кнопки меню или /start для начала работы."
    )