# Библиотеки
import logging
from aiogram import Bot, Dispatcher, types, executor
from bot_config import data
import bot_config.keyboard
from arbitr_parser import case_numbers

chat_id = data.id_a
access_id =data.id_a

# Объект бота
bot = Bot(data.token, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot_config.keyboard.Buttoms(dp, bot, chat_id, access_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
