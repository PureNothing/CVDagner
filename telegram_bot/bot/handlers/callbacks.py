from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import GRAPHQL_URL
from aiogram.fsm.context import FSMContext
import aiohttp
from queries import cameras
from handlers.states import Settings

router = Router()

@router.callback_query(F.data == "camera_1")
async def camera_1(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json=cameras.full_camera1_query) as client:
            await callback.answer()
            await callback.message.answer(str(client.json))
            await callback.message.answer(str(client.status))

@router.callback_query(F.data == "camera_2")
async def camera_2(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Логика 2 камеры")

@router.callback_query(F.data == "camera_3")
async def camera_3(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Логика 3 камеры")

@router.callback_query(F.data == "camera_4")
async def camera_4(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Логика 4 камеры")

@router.callback_query(F.data == "camera_5")
async def camera_5(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Логика 5 камеры")

@router.callback_query(F.data == "full_report")
async def full_report(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Логика отчета за день по всем камерам")

@router.callback_query(Settings.in_settings, F.data == "alert_settings")
async def alert_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "🔢 Введите порог срабатывания (целое число):\n"
        "Например: 5 (если опасностей больше 5)"
    )
    await state.set_state(Settings.waiting_threshold)

@router.callback_query(Settings.in_settings, F.data == "exit_settings")
async def exit_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("🚪 Вы вышли из настроек")
    await state.clear()