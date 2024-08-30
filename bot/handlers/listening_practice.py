import json
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import asyncio

from aiogram.types import ReplyKeyboardRemove
from pydantic.v1.utils import path_type

from bot.buttons.reply_buttons import start_listening_button, get_options_button, main_menu_buttons
from bot.buttons.text import listening_practice, ready_text
from bot.dispatcher import dp, bot


async def get_question(used_questions: list, audio_id: str):
    questions = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/audios/detail/{audio_id}").content)['questions']
    while True:
        num = random.randint(0, len(questions) - 1)
        question_id = questions[num]['id']
        if question_id not in used_questions:
            return questions[num], num


async def get_audio(section: int, audio_type: str):
    all_audios = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/audios/{section}/{audio_type}").content)
    num = random.randint(0, len(all_audios) - 1)
    audio = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/audios/detail/{all_audios[num]['id']}").content)
    return audio


@dp.message_handler(Text(equals=[listening_practice]))
async def listening_practice_function(msg: types.Message, state: FSMContext):
    audio = await get_audio(section=1, audio_type='practice')
    message = await msg.answer("Lets go!", reply_markup=ReplyKeyboardRemove())
    await message.delete()
    loading_message = await msg.answer("Preparing your test🔄 Please wait.")
    file = open(audio['audio']['audio_file'][22:], 'rb')
    animation_texts = [
        "Preparing your test.🔄 Please wait.",
        "Preparing your test..🔄 Please wait.",
        "Preparing your test...🔄 Please wait.",
        "Almost done... 🚀 Please hold on."
    ]
    for i in range(len(animation_texts)):
        await asyncio.sleep(0.5)
        if animation_texts[i] != loading_message.text:
            await loading_message.edit_text(animation_texts[i])
    await state.set_state('starting_audio_practice')
    await msg.answer_audio(audio=file,
                           reply_markup=await start_listening_button())
    file.close()
    await loading_message.delete()
    async with state.proxy() as proxy:
        proxy['audio_id'] = audio['audio']['id']
        proxy['questions_count'] = len(audio['questions'])
        proxy['correct_answers'] = 0
        proxy['used_questions'] = []
        proxy['question_id'] = 0
        proxy['num'] = 0
        proxy['answers_count'] = 0
        proxy['questions'] = []
        proxy['answers'] = []


@dp.message_handler(Text(equals=[ready_text]), state='starting_audio_practice')
async def listening_practice_function_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        await state.set_state("listening_practice_2")
        question, num = await get_question(used_questions=[], audio_id=proxy['audio_id'])
        proxy['question_id'] = question['id']
        proxy['num'] = num
        proxy['questions'] = question['options']
        proxy['used_questions'].append(proxy['question_id'])
        try:
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 1)
        except Exception:
            pass
        await msg.answer(text=f"{question['condition']}\n\n{question['question']}",
                         reply_markup=await get_options_button(question['options']))


@dp.message_handler(state='listening_practice_2')
async def listening_practice_function_3(msg: types.Message, state: FSMContext):
    async with (state.proxy() as proxy):
        user_answer = msg.text
        questions = \
            json.loads(requests.get(url=f"http://127.0.0.1:8003/api/audios/detail/{proxy['audio_id']}").content)[
                'questions']
        correct_answer = questions[proxy['num']]['correct_answer']
        if proxy['questions_count'] == len(proxy['used_questions']):
            await msg.answer(
                f"Test completed! 🎉\nYou answered {proxy['correct_answers']} out of {proxy['questions_count']} correctly.",
                reply_markup=await main_menu_buttons(chat_id=msg.from_user.id))
            await state.finish()
        elif len(correct_answer) == 1:
            question, num = await get_question(used_questions=proxy['used_questions'], audio_id=proxy['audio_id'])
            proxy['question_id'] = question['id']
            proxy['num'] = num
            proxy['questions'] = question['options']
            if len(question['correct_answer']) == 1:
                proxy['used_questions'].append(proxy['question_id'])
            await msg.answer(text=f"{question['condition']}\n\n{question['question']}",
                             reply_markup=await get_options_button(question['options']))
            if user_answer == correct_answer[-1]:
                proxy['correct_answers'] += 1
        elif proxy['answers_count'] == len(correct_answer) - 1:
            question, num = await get_question(used_questions=proxy['used_questions'], audio_id=proxy['audio_id'])
            proxy['used_questions'].append(proxy['question_id'])
            proxy['question_id'] = question['id']
            proxy['num'] = num
            proxy['questions'] = question['options']
            proxy['used_questions'].append(proxy['question_id'])
            proxy['answers'].append(msg.text)
            await msg.answer(text=f"{question['condition']}\n\n{question['question']}",
                             reply_markup=await get_options_button(question['options']))
            for answer in proxy['answers']:
                if answer in correct_answer:
                    proxy['correct_answers'] += 1
            proxy['answers'] = []
        else:
            proxy['answers'].append(msg.text)
            proxy['answers_count'] += 1
            proxy['questions'].remove(msg.text)
            await msg.answer(
                text=f"{questions[proxy['num']]['condition']}\n\n{questions[proxy['num']]['question']}",
                reply_markup=await get_options_button(proxy['questions']))
