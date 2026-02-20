from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.buttons import home_kb
from menus.mainmenu import main_menu

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("""👋 Добро пожаловать!\n
                         Для ознакомления открой меню ниже и выбери - ❓ Помощь""", reply_markup=main_menu)

@router.message(Command("settings"))
async def settings(message: Message):
    await message.answer("🔐 Введите секретный ключ:")




