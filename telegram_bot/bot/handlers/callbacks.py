from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.core.config import GRAPHQL_URL
from aiogram.fsm.context import FSMContext
import aiohttp
from bot.queries import cameras
from bot.parsers.single_camera_parser import format_answer
from bot.parsers.full_report_parser import report_format_answer
from bot.handlers.states import Settings

router = Router()

@router.callback_query(F.data == "camera_1")
async def camera_1(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.query_parse(1)}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(format_answer(response))

@router.callback_query(F.data == "camera_2")
async def camera_2(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.query_parse(2)}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(format_answer(response))

@router.callback_query(F.data == "camera_3")
async def camera_3(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.query_parse(3)}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(format_answer(response))

@router.callback_query(F.data == "camera_4")
async def camera_4(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.query_parse(4)}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(format_answer(response))

@router.callback_query(F.data == "camera_5")
async def camera_5(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.query_parse(5)}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(format_answer(response))

@router.callback_query(F.data == "full_report")
async def full_report(callback: CallbackQuery):
    async with aiohttp.ClientSession() as conn:
        async with conn.post(GRAPHQL_URL, json={"query": cameras.full_general_report}) as client:
            await callback.answer()
            response = await client.json()
            await callback.message.answer(report_format_answer(response))

@router.callback_query(Settings.in_settings, F.data == "alert_settings")
async def alert_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "Выберете номер камеры для которой хотите установить порог."
        "Затем выберете класс для которого хотите установить порог"
        "Затем укажите сам порог:"
        "🔢 (целое число):\n"
        "Например: порог танков для камеры один хочу 5 (если опасностей больше 5)"
    )
    await state.set_state(Settings.waiting_threshold)

@router.callback_query(Settings.in_settings, F.data == "exit_settings")
async def exit_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("🚪 Вы вышли из настроек")
    await state.clear()