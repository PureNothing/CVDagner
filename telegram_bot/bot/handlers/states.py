from aiogram.fsm.state import State, StatesGroup

class Settings(StatesGroup):
    waiting_key = State()
    in_settings = State()
    waiting_threshold = State()
    waiting_newcamera_settings = State()