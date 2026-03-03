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
        "⚙️ <b>Настройка порогов алертов</b>\n\n"
        "Укажите номер камеры, класс и желаемый порог одним сообщением.\n\n"
        "🎯 <b>Доступные классы:</b>\n"
        "🪖 Пехота\n"
        "🛡 Танк\n"
        "🚛 БМП (Боевая Машина Пехоты)\n"
        "🚜 БТР (Бронетранспортер)\n"
        "🚗 Бронемашина\n"
        "💣 Артиллерия\n"
        "🚀 РСЗО (Ракетная Система Залпового Огня)\n"
        "✈️ БПЛА (Беспилотный Летательный Аппарат)\n\n"
        "📝 <b>Пример:</b>\n"
        "Порог танков для камеры 1 хочу 5 (если танков станет больше 5 — придёт алерт)",
        parse_mode="HTML"
    )
    await state.set_state(Settings.waiting_threshold)

@router.callback_query(Settings.in_settings, F.data == "add_camera")
async def add_camera(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        "📷 <b>Добавление новой камеры</b>\n\n"
        "Напишите данные камеры одним сообщением:\n\n"
        "🔢 <b>Номер камеры</b> — целое число\n"
        "📍 <b>Координаты</b> — два числа через пробел\n"
        "🌍 <b>Описание местности</b> — что находится вокруг камеры\n\n"
        "📝 <b>Пример:</b>\n"
        "Добавь камеру 6, координаты 48.123 и 37.456, открытое поле рядом с густым лесом, гражданских нет.\n\n"
        "Порог для каждого класса по умолачнию установится = 2, позже вы сможете это сменить через настройки алертов.",
        parse_mode="HTML"
    )
    await state.set_state(Settings.waiting_newcamera_settings)

@router.callback_query(Settings.in_settings, F.data == "exit_settings")
async def exit_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("🚪 Вы вышли из настроек")
    await state.clear()