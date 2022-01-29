from aiogram import types
from aiogram.dispatcher.filters import Text
import asyncio
import bot_config.data
from arbitr_parser import kad
import random
import time

def Buttoms(dp, bot, chat_id, access_id):

    loop = asyncio.get_event_loop()
    @dp.message_handler(commands="start")
    async def tap1(message: types.Message):
        if message.from_user.id in chat_id:
            await message.answer("Добро пожаловать в бота!")
            if len(bot_config.data.mail_list) == 0:
                bot_config.data.mail_list.append(message.from_user.id)
                loop.create_task(mail())
            elif (message.from_user.id) not in bot_config.data.mail_list:
                bot_config.data.mail_list.append(message.from_user.id)
        else:
            await message.answer("Нет доступа")


    @dp.message_handler(commands="stop")
    async def tap2(message: types.Message):
        bot_config.data.mail_list.remove(message.from_user.id)
        await message.answer("Рассылка остановлена")

    @dp.message_handler(commands="continue")
    async def tap3(message: types.Message):
        if message.from_user.id in chat_id:
            await message.answer("Рассылка возобовлена")
            if len(bot_config.data.mail_list) == 0:
                bot_config.data.mail_list.append(message.from_user.id)
                loop.create_task(mail())
            elif (message.from_user.id) not in bot_config.data.mail_list:
                bot_config.data.mail_list.append(message.from_user.id)





    async def mail():
        while bot_config.data.mail_list:
            await asyncio.sleep(5)
            scrap = kad.DriverScrapping()
            l = scrap.all_types()
            scrap.driver.quit()
            for j in bot_config.data.mail_list:
                if j in bot_config.data.mail_list:
                    for i in l:
                        message=f"Ссылка на дело: {str(i[0])}\n"
                        message+=f"Ссылка на документ: {str(i[1])}\n"
                        await bot.send_message(chat_id=j, text=message)  # чтобы отправлять сообщения нескольким пользователям сразу

    dp.register_message_handler(tap1, commands="start")
    dp.register_message_handler(tap2, commands="stop")
    dp.register_message_handler(tap3, commands="continue")



