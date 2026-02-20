from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from keyboards.buttons import home_kb

router = Router()

@router.message(F.text == "🏠 Главное меню")
async def home(message: Message):
    await message.answer("Какую информацию предоставить?", reply_markup=home_kb)


@router.message(F.text == "❓ Помощь")
async def help(message: Message):
    await message.answer(
        f"📋 <b>Справка по боту</b>\n\n"
        f"🔍 <b>Что умеет бот?</b>\n"
        f"Этот бот следит за вашей безопасностью через камеры. "
        f"Вы можете запросить информацию о текущей обстановке.\n\n"
        f"📸 <b>Детекция</b>\n"
        f"Если бот обнаружит человека, оружие или военную технику — "
        f"он сообщит вам, где, когда и сколько объектов заметил.\n\n"
        f"🎛 <b>Как получить информацию</b>\n"
        f"• 🏠 <b>Главное меню</b> — вызывает кнопки с камерами\n"
        f"• 📹 <b>Камера 1–5</b> — данные по конкретной камере\n"
        f"• 📊 <b>Полный отчет</b> — сводка за последние 24 часа по всем камерам\n\n"
        f"⚠️ <b>Алерты</b>\n"
        f"При серьёзной опасности бот сам пришлёт уведомление. "
        f"Вы можете настроить критерии срабатывания через секретный ключ.\n\n"
        f"🆔 <b>Ваши данные</b>\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Username: @{message.from_user.username}\n\n"
        f"☝️ Не заигрывайтесь с ботом — он следит за вами 😉",
        parse_mode="HTML"
    )

@router.message() #Реагируем на все сообщения, пустые скобки.
async def message(message: Message):
    text = message.text
    if text == "картинка":
      await message.answer_document(FSInputFile("Адрес картинки webm"), caption="Держи картинку!")
    elif text == "файл":
        await message.answer_document(FSInputFile("Адрес файла PDF"), caption="Держи файл!")
    else:
        await message.answer("Чел.... Лучше молчи...")