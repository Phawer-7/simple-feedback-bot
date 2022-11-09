from aiogram import types, Bot, Dispatcher, executor
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from db import createData, getUser_id

bot = Bot(token="1111111111")
dp = Dispatcher(bot)

ADMIN_ID = 0000


async def sendMessageIfBotCan(message_text: str, user_id: int):
    if not user_id is None:
        try:
            await bot.send_message(chat_id=user_id, text=message_text, parse_mode='HTML')
            await bot.send_message(chat_id=ADMIN_ID, text='Сообщение было отправлено')
        except BotBlocked:
            await bot.send_message(chat_id=ADMIN_ID, text='Пользователь заблокировал бота.')
        except ChatNotFound:
            await bot.send_message(chat_id=ADMIN_ID, text="Ты не можешь писать пользователю который боту еще ничего не "
                                                          "писал")
    else:
        await bot.send_message(chat_id=ADMIN_ID, text="Error. Используй /send id текст")


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Чтобы зарегать свою пару заполните анкету - \n1. Юзы двух пар.\n2. Смайл пары')
    else:
        await message.answer('Я работаю только в личных чатах.')


@dp.message_handler(commands=['send', 'отправить'], commands_prefix="!?/\.#$")
async def sendMessageToUser(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            userid = int(message.text.split()[1])
            text = " ".join(message.text.split()[2:])

            await sendMessageIfBotCan(message_text=text, user_id=userid)

        except IndexError:
            await message.answer('<code>/send id_пользователя текст</code>', parse_mode='HTML')
        except ValueError:
            await message.answer('<code>/send id_пользователя текст</code>', parse_mode='HTML')


@dp.message_handler(content_types=['text'])
async def wrote_text(message: types.Message):
    if message.chat.type == 'private':
        if not message.from_user.id == ADMIN_ID:
            msgId = await bot.send_message(ADMIN_ID, text=message.text)
            createData(text=message.text, message_id=msgId['message_id'], user_id=message.from_user.id)
        else:
            if message.reply_to_message:
                id = getUser_id(message_id=message.reply_to_message.message_id)
                await sendMessageIfBotCan(message_text=message.text, user_id=id)
            else:
                await message.answer('Нужно отвечать в ответ на сообщение')


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)
