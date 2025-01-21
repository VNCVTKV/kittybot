import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv 

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


urls = ('https://api.thecatapi.com/v1/images/search',
        'https://api.thedogapi.com/v1/images/search'
        )


def get_new_image(x):
    try:
        response = requests.get(urls[x])
    except Exception as error:
        # Печатать информацию в консоль теперь не нужно:
        # всё необходимое будет в логах
        # print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = urls[1 - x]
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(0))


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(1))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['/newcat'], ['/newdog']],
        resize_keyboard=True,
          )

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри какого котика я тебе нашел'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image(0))


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 