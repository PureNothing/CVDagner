from aiogram.types import BotCommand

MENU_COMMANDS = [
    BotCommand(command="start", description = "Вызвать кнопки меню "),
    BotCommand(command="settigns", description = "⚙️ Настройки")
]

async def setup_menu(bot):
    await bot.set_my_commands(MENU_COMMANDS)