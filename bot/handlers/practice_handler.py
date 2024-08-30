from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import practice_buttons
from bot.buttons.text import practice, practice_en, practice_ru
from bot.dispatcher import dp


@dp.message_handler(Text(equals=[practice, practice_en, practice_ru]))
async def practice_handler(msg: types.Message):
    if msg.text == practice:
        await msg.answer(text="Qaysi yo'nalishda amaliyot qilmoxchisiz? 🤔", reply_markup=await practice_buttons())
    elif msg.text == practice_en:
        await msg.answer(text="Which direction do you practice? 🤔", reply_markup=await practice_buttons())
    else:
        await msg.answer(text="В каком направлении вы практикуете? 🤔", reply_markup=await practice_buttons())