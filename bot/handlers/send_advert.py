import asyncio
import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from aiogram.utils.exceptions import ChatNotFound

from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, advert_menu_buttons, admin_menu_buttons
from bot.buttons.text import adverts, none_advert, forward_advert
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(commands='admin')
async def admin_handler(msg: types.Message):
    if msg.from_user.id in admins:
        await msg.answer("Admin menuga xush kelibisz ℹ️", reply_markup=await admin_menu_buttons())


@dp.message_handler(Text(adverts))
async def advert_handler(msg: types.Message):
    if msg.from_user.id in admins:
        await msg.answer("Qaysi uslubda habar yuborasiz ❓", reply_markup=await advert_menu_buttons())


@dp.message_handler(Text(none_advert))
async def advert_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in admins:
        await state.set_state("advert")
        await msg.answer("Habarni yuboring ❗", reply_markup=await back_main_menu_button())


@dp.message_handler(state='advert', content_types=ContentType.ANY)
async def get_user_id_for_send_to_user(msg: types.Message, state: FSMContext):
    await state.finish()
    users = json.loads(requests.get(f"http://127.0.0.1:8003/api/telegram-users/").content)['results']
    suc = 0
    session = await msg.answer(text="✅ Xabar yuborish boshlandi!")
    for user in users:
        try:
            await msg.copy_to(chat_id=int(user['chat_id']), caption=msg.caption,
                              caption_entities=msg.caption_entities,
                              reply_markup=msg.reply_markup)
            suc += 1
            await asyncio.sleep(0.05)
        except ChatNotFound:
            pass
        except Exception:
            pass
    else:
        await session.delete()
        await msg.answer(
            text=f"Habar userlarga tarqatildi✅\n\n{suc}-ta userga yetib bordi✅",
            reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.message_handler(Text(forward_advert))
async def send_forward(msg: types.Message, state: FSMContext):
    if msg.from_user.id in admins:
        await state.set_state('send_forward')
        await msg.answer(text=f"📨 Forward xabarni yuboring", reply_markup=await back_main_menu_button())


@dp.message_handler(state='send_forward', content_types=ContentType.ANY)
async def forward_txt(msg: types.Message, state: FSMContext):
    await state.finish()
    users = json.loads(requests.get(f"http://127.0.0.1:8003/api/telegram-users/").content)['results']
    suc = 0
    session = await msg.answer(text="✅ Xabar yuborish boshlandi!")
    for user in users:
        try:
            await bot.forward_message(chat_id=int(user['chat_id']), from_chat_id=msg.chat.id,
                                      message_id=msg.message_id)
            suc += 1
            await asyncio.sleep(0.05)
        except ChatNotFound:
            pass
        except Exception:
            pass
    else:
        await session.delete()
        await msg.answer(
            text=f"Habar userlarga tarqatildi✅\n\n{suc}-ta userga yetib bordi✅",
            reply_markup=await main_menu_buttons(msg.from_user.id))
