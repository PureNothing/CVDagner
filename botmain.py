import aiohttp
from config import bot_token, full_camera_query
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import asyncio


bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def anwser(message: Message):
    await message.answer("Привет, я наблюдая за безопасностью, не отвлекай если не интересно узнать о её состоянии!")
    await message.answer(f"Я уже знаю твой ID: {message.from_user.id} и твой Username: {message.from_user.username}, поэтому за твою безопасность не ручаюсь, не беспокой меня!")

@dp.message(Command("camera_1"))
async def camera(message: Message):
    async with aiohttp.ClientSession() as conn:
      async with conn.post("http://localhost:8000/graphql", json={"query": full_camera_query}) as client:
        await message.answer(str(client.json()))
        await message.answer(str(client.status_code))

@dp.message()
async def message(message: Message):
    text = message.text
    if text == "картинка":
      await message.answer_document(FSInputFile("Адрес картинки webm"), caption="Держи картинку!")
    elif text == "файл":
        await message.answer_document(FSInputFile("Адрес файла PDF"), caption="Держи файл!")
    else:
        await message.answer("Чел.... Лучше молчи...")

async def check_and_alert():
    #Проверяем услвоие, если Да , сообщаем
    while True:
      await bot.send_message(
        chat_id=1111215202,
        text="Тревога! На камере 1 обнаружена опасность!",
        protect_content=True
      )
      await asyncio.sleep(30)

async def main():
    await asyncio.gather(
      check_and_alert(),
      dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())

