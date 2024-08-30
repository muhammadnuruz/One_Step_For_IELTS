import json
import random

import requests
from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, practice, end_test, choice_language, \
    choice_language_ru, practice_ru, choice_language_en, practice_en, vocabulary_practice, listening_practice, \
    reading_practice, back_main_menu_en, ready_text


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [practice],
            [choice_language]
        ]
    elif tg_user['language'] == 'en':
        design = [
            [practice_en],
            [choice_language_en]
        ]
    else:
        design = [
            [practice_ru],
            [choice_language_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button():
    design = [[back_main_menu_en]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def test_buttons(words: dict):
    design = [[words['word']['definition']]]
    for word in words['random_definitions']:
        design.append([word])
    random.shuffle(design)
    design.append([end_test])
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def practice_buttons():
    design = [
        [vocabulary_practice],
        [listening_practice],
        [reading_practice],
        [back_main_menu_en]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def start_listening_button():
    design = [
        [ready_text],
        [back_main_menu_en]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def get_options_button(options: dict):
    design = []
    try:
        for option in options:
            design.append([f"{option}"])
    except TypeError:
        pass
    design.append([back_main_menu_en])
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
