from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

home_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📹 Камера 1", callback_data="camera_1")],
    [InlineKeyboardButton(text="📹 Камера 2", callback_data="camera_2")],
    [InlineKeyboardButton(text="📹 Камера 3", callback_data="camera_3")],
    [InlineKeyboardButton(text="📹 Камера 4", callback_data="camera_4")],
    [InlineKeyboardButton(text="📹 Камера 5", callback_data="camera_5")],
    [InlineKeyboardButton(text="📊 Полный отчет", callback_data="full_report")]
])

