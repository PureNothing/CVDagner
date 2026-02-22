from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BufferedInputFile, URLInputFile
from bot.keyboards.buttons import home_kb
from bot.handlers.states import Settings
from aiogram.fsm.context import FSMContext
import aiohttp

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
        threshold = int(message.text)
        await message.answer(f"✅ Порог установлен {threshold}")
        await state.clear()
    except ValueError:
        await message.answer("❌ Это не число. Введите число.")





@router.message() #Реагируем на все сообщения, пустые скобки.
async def message(message: Message):
    text = message.text
    if text == "О как":
        async with aiohttp.ClientSession() as conn:
            async with conn.get("https://avatars.mds.yandex.net/i?id=84b2a0e7f8dec69aac4475c5d2c78e97_l-5544703-images-thumbs&n=13") as response:
                photo = await response.read()
                await message.answer_photo(BufferedInputFile(file=photo, filename="molitva.jpg"), caption="Читать вслух ")
    elif text == "хайп":
        await message.answer_photo(photo="https://sun9-74.userapi.com/impf/OTkiwUdjRMxqEf8KDUP_S7L9SvwnOriyCutB1A/gBso05pegBY.jpg?size=1920x768&quality=95&crop=0,0,1920,767&sign=b9f1774c7cda184a3d459a855ad19815&type=cover_group", caption="Хайпим")
    elif text == "файл":
        await message.answer_document(FSInputFile("Адрес файла PDF"), caption="Держи файл!")
    else:
        await message.answer("Чел.... Лучше молчи...")