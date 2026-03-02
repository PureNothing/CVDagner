from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.buttons import settings_kb
from bot.menus.mainmenu import main_menu
from aiogram.fsm.context import FSMContext
from bot.core.config import SETTINGS_KEY
from bot.handlers.states import Settings



router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(        
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Внизу появились две кнопки:\n"
        "🏠 <b>Главное меню</b> — открывает список камер и полный отчёт\n"
        "❓ <b>Помощь</b> — подробная информация о боте\n\n"
        "Если кнопки вдруг пропадут — просто нажмите /start снова.",
        parse_mode="HTML",
        reply_markup=main_menu
        )

@router.message(Command("molitva"))
async def moitva(message: Message):
    await message.answer_photo("https://i.pinimg.com/736x/8a/76/ff/8a76ffbd7b296b637393708d2ffcd63c.jpg", caption="Спасибо 🙏")


@router.message(Command("settings"))
async def settings(message: Message, state: FSMContext):
    await message.answer("🔐 Введите секретный ключ:")
    await state.set_state(Settings.waiting_key)

@router.message(Settings.waiting_key)
async def key_check(message: Message, state: FSMContext):
    if message.text == SETTINGS_KEY:
        await message.answer("✅ Доступ разрешен", reply_markup=settings_kb)
        await state.set_state(Settings.in_settings)
    else:
        await message.answer("❌ Неверно, доступ запрещен")
        await state.clear()



