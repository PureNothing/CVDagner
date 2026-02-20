from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import GRAPHQL_URL
import aiohttp
from queries import cameras

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

