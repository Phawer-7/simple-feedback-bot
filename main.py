from aiogram import types, Bot, Dispatcher, executor
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from db import createData, getUser_id

bot = Bot(token="")
dp = Dispatcher(bot)

ADMIN_USER_ID = 00000000
ADMIN_GROUP_ID = -00000000


async def sendMessageIfBotCan(message_text: str, user_id: int, is_pic: bool = False):
    if not user_id is None:
        try:
            if not is_pic:
                await bot.send_message(chat_id=user_id, text=message_text, parse_mode='HTML')
            else:
                await bot.send_photo(chat_id=user_id, photo=message_text)
            await bot.send_message(chat_id=ADMIN_GROUP_ID, text='Сообщение было отправлено.')
        except BotBlocked:
            await bot.send_message(chat_id=ADMIN_GROUP_ID, text='Пользователь заблокировал бота.')
        except ChatNotFound:
            await bot.send_message(chat_id=ADMIN_GROUP_ID, text="Ты не можешь писать пользователю который боту еще "
                                                                "ничего не писал.")
    else:
        await bot.send_message(chat_id=ADMIN_GROUP_ID, text="Error. Используй /send id текст")


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Привет, я бот для обратной связи.')
    else:
        if not message.from_user.id == ADMIN_USER_ID:
            await message.answer('Я работаю только в личных чатах.')


@dp.message_handler(commands=['send', 'отправить'], commands_prefix="!?/\.#$")
async def sendMessageToUser(message: types.Message):
    if message.from_user.id == ADMIN_USER_ID:
        try:
            userid = int(message.text.split()[1])
            text = " ".join(message.text.split()[2:])

            await sendMessageIfBotCan(message_text=text, user_id=userid)
        except IndexError or ValueError:
            await message.answer('<code>/send id_пользователя текст</code>', parse_mode='HTML')


@dp.message_handler(content_types=['text', 'photo'])
async def wrote_text(message: types.Message):
    if message.chat.type == 'private':
        if not message.from_user.id == ADMIN_USER_ID:
            if message.content_type == 'text':
                msgId = await bot.send_message(ADMIN_GROUP_ID, text=message.text)
                createData(text=message.text, message_id=msgId['message_id'], user_id=message.from_user.id)
            else:
                msgId = await bot.send_photo(ADMIN_GROUP_ID, photo=message['photo'][0]["file_id"])
                createData(text="photo", message_id=msgId['message_id'], user_id=message.from_user.id)

    else:
        if message.reply_to_message:
            if message.from_user.id == ADMIN_USER_ID:
                id = getUser_id(message_id=message.reply_to_message.message_id)
                if not message.content_type == 'text':
                    await sendMessageIfBotCan(message_text=message['photo'][0]["file_id"], user_id=id, is_pic=True)
                else:
                    await sendMessageIfBotCan(message_text=message.text, user_id=id)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)

