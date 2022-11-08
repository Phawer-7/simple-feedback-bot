from aiogram import types, Bot, Dispatcher, executor
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

bot = Bot(token="")
dp = Dispatcher(bot)

admin_id = 1111111


async def sendMessageIfBotCan(message_text: str, user_id: int):
    try:
        await bot.send_message(chat_id=user_id, text=message_text, parse_mode='HTML')
        await bot.send_message(chat_id=admin_id, text='Сообщение было отправлено')
    except BotBlocked:
        await bot.send_message(chat_id=admin_id, text='Пользователь заблокировал бота.')
    except ChatNotFound:
        await bot.send_message(chat_id=admin_id, text="Ты не можешь писать пользователю который боту еще ничего не "
                                                      "писал", parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Я Фунтик, привет.')
    else:
        await message.answer('Я работаю только в личных чатах.')


@dp.message_handler(commands=['send', 'отправить'], commands_prefix="!?/\.#$")
async def sendMessageToUser(message: types.Message):
    if message.from_user.id == admin_id:
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
        if not message.from_user.id == admin_id:
            await message.forward(chat_id=admin_id)
            await bot.send_message(admin_id, f"id: <code>{message.from_user.id}</code>\n"
                                             f"name: {message.from_user.first_name}\n"
                                             f"username: @{message.from_user.username}",
                                   parse_mode='HTML')
            await message.answer('Фунтик скоро тебе ответит.')
        else:
            if message.reply_to_message:
                try:
                    await sendMessageIfBotCan(message_text=message.text, user_id=message.reply_to_message.forward_from.id)
                except AttributeError:
                    await bot.send_message(chat_id=admin_id, text="Чуть выше есть сообщение с информацией о пользователе"
                                                "(айди, имя, юзер). Оттуда берем ID и пишем /send то_самое_айди "
                                                "текст ", parse_mode='HTML')
            else:
                await message.answer('Нужно отвечать в ответ на сообщение')


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)
