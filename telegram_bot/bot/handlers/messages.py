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
        f"📋 <b>Справка</b>\n\n"
        
        f"🔒 <b>О боте</b>\n"
        f"Этот бот следит за вашей безопасностью. Вы можете запросить у него информацию.\n"
        f"Он расскажет, спокойно ли там, где камера, или есть опасность. "
        f"Если кого-то обнаружит — скажет, где, когда, кого и в каком количестве.\n\n"
        
        f"🖱 <b>Как получить информацию</b>\n"
        f"Нажмите большую кнопку <b>🏠 Главное меню</b> внизу экрана.\n"
        f"Откроется список:\n"
        f"  • 📹 Камера 1–5 — данные по конкретной камере\n"
        f"  • 📊 Полный отчёт — сводка за сутки по всем камерам\n\n"
        
        f"⚙️ <b>Настройки</b>\n"
        f"Чтобы изменить параметры работы:\n"
        f"  1. Откройте меню слева (три полоски)\n"
        f"  2. Выберите команду <b>/settings</b>\n"
        f"  3. Подтвердите личность секретным ключом\n\n"
        
        f"🔄 <b>Если кнопки внизу пропали</b>\n"
        f"Нажмите команду <b>/start</b> в левом меню — они появятся снова.\n\n"
        
        f"⚠️ <b>Алерты</b>\n"
        f"При серьёзной опасности бот предупредит сам. "
        f"Пороги можно настроить в разделе Настройки.\n\n"
        
        f"🆔 <b>Ваши данные</b>\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Username: @{message.from_user.username}\n\n"
        
        f"☝️ Не заигрывайтесь — он уже знает, кто вы.",
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