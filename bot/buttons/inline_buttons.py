import json
import random

import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import uz_language, ru_language, en_language, end_test, back_main_menu_ru, back_main_menu, \
    back_main_menu_en


async def language_buttons():
    design = [
        [InlineKeyboardButton(text=uz_language, callback_data='language_uz'),
         InlineKeyboardButton(text=ru_language, callback_data='language_ru'),
         InlineKeyboardButton(text=en_language, callback_data='language_en')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
