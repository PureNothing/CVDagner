from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.queries import cameras
from bot.parsers.single_camera_parser import format_answer
from bot.parsers.full_report_parser import report_format_answer
from bot.handlers.states import Settings
from bot.utils.requests_func import get_info, get_full_and_info_final

router = Router()

@router.callback_query(F.data == "camera_1")
async def camera_1(callback: CallbackQuery):
    response_camera, response_coordinates, response_place = await get_info(1)
    await callback.answer()
    await callback.message.answer(format_answer(response=response_camera, 
                                                response_coordinates=response_coordinates, 
                                                response_place=response_place))

@router.callback_query(F.data == "camera_2")
async def camera_2(callback: CallbackQuery):
    response_camera, response_coordinates, response_place = await get_info(2)
    await callback.answer()
    await callback.message.answer(format_answer(response=response_camera,
                                                response_coordinates=response_coordinates,
                                                response_place=response_place))

@router.callback_query(F.data == "camera_3")
async def camera_3(callback: CallbackQuery):
    response_camera, response_coordinates, response_place = await get_info(3)
    await callback.answer()
    await callback.message.answer(format_answer(response=response_camera,
                                         response_coordinates=response_coordinates,
                                         response_place=response_place))

@router.callback_query(F.data == "camera_4")
async def camera_4(callback: CallbackQuery):
    response_camera, response_coordinates, response_place = await get_info(4)
    await callback.answer()
    await callback.message.answer(format_answer(response=response_camera,
                                         response_coordinates=response_coordinates,
                                         response_place=response_place))


@router.callback_query(F.data == "camera_5")
async def camera_5(callback: CallbackQuery):
    response_camera, response_coordinates, response_place = await get_info(5)
    await callback.answer()
    await callback.message.answer(format_answer(response=response_camera,
                                         response_coordinates=response_coordinates,
                                         response_place=response_place))

@router.callback_query(F.data == "full_report")
async def full_report(callback: CallbackQuery):
    full_graph, full_cor_plc = await get_full_and_info_final()
    await callback.answer()
    await callback.message.answer(report_format_answer(response=full_graph,
                                                       cor_plc=full_cor_plc))

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