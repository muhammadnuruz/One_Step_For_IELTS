import json
import random
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.buttons.reply_buttons import main_menu_buttons, test_buttons
from bot.buttons.text import vocabulary_practice, end_test
from bot.dispatcher import dp


def determine_final_level(level_correct_count):
    thresholds = {
        'a1': 5,
        'a2': 4,
        'b1': 4,
        'b2': 4,
        'c1': 3,
        'c2': 3
    }
    for level in reversed(['a1', 'a2', 'b1', 'b2', 'c1', 'c2']):
        if level_correct_count[level]['correct'] >= thresholds[level]:
            return level
    return 'a1'


def calculate_level_percentages(level_correct_count):
    percentages = {}
    for level, counts in level_correct_count.items():
        total = counts['total']
        correct = counts['correct']
        if total > 0:
            percentages[level] = round((correct / total) * 100, 2)
    return percentages


async def adjust_level(consecutive_questions):
    level = 'a1'
    if consecutive_questions >= 25:
        level = 'c2'
    elif consecutive_questions >= 20:
        level = 'c1'
    elif consecutive_questions >= 15:
        level = 'b2'
    elif consecutive_questions >= 10:
        level = 'b1'
    elif consecutive_questions >= 5:
        level = 'a2'
    return level


async def get_test(level: str, words: list):
    all_words = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/words/{level}").content)
    used_words = set(words)
    while True:
        num = random.randint(0, len(all_words) - 1)
        word_id = all_words[num]['id']
        if word_id not in used_words:
            break
    word = all_words[num]
    word = json.loads(requests.get(url=f"http://127.0.0.1:8003/api/words/detail/{word['id']}").content)
    return word, all_words


@dp.message_handler(Text(equals=[vocabulary_practice]))
async def test_vocabulary_practice_function(msg: types.Message, state: FSMContext):
    word, all_words = await get_test(level='a1', words=[])
    async with state.proxy() as data:
        data['word_number'] = 1
        data['words_count'] = len(all_words)
        data['words'] = [word['word']['id']]
        data['correct_answers'] = 0
        data['correct_answer'] = word['word']['definition']
        data['word'] = word['word']['word']
        data['consecutive_questions'] = 0
        data['levels'] = ['a1']
        data['level_correct_count'] = {
            'a1': {'correct': 0, 'total': 0},
            'a2': {'correct': 0, 'total': 0},
            'b1': {'correct': 0, 'total': 0},
            'b2': {'correct': 0, 'total': 0},
            'c1': {'correct': 0, 'total': 0},
            'c2': {'correct': 0, 'total': 0}
        }
    await msg.answer(text=f"Test 1\n\nFind the definition of {data['word']}",
                     reply_markup=await test_buttons(words=word))
    await state.set_state('test_vocabulary_practice')


@dp.message_handler(Text(end_test), state="test_vocabulary_practice")
async def test_vocabulary_practice_function_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await msg.delete()
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8003/api/telegram-users/chat_id/{msg.from_user.id}/").content)

        user_level = determine_final_level(data['level_correct_count'])
        level_percentages = calculate_level_percentages(data['level_correct_count'])
        levels_info = "\n".join(
            [f"{level.upper()}: {percent}%" for level, percent in level_percentages.items() if level in data['levels']])

        if tg_user['language'] == 'uz':
            await msg.answer(
                text=f"Siz testni yakunladingiz 🎉\n\nDarajalar:\n{levels_info}\n\nUmumiy darajangiz: {user_level.upper()}",
                reply_markup=await main_menu_buttons(msg.from_user.id))
        elif tg_user['language'] == 'ru':
            await msg.answer(
                text=f"Вы прошли тест 🎉\n\nУровни:\n{levels_info}\n\nВаш общий уровень: {user_level.upper()}",
                reply_markup=await main_menu_buttons(msg.from_user.id)
            )
        else:
            await msg.answer(
                text=f"You have completed the test 🎉\n\nLevels:\n{levels_info}\n\nYour overall level: {user_level.upper()}",
                reply_markup=await main_menu_buttons(msg.from_user.id)
            )
        await state.finish()


@dp.message_handler(state="test_vocabulary_practice")
async def test_vocabulary_practice_function_4(msg: types.Message, state: FSMContext):
    answer = "False"
    async with state.proxy() as data:
        if msg.text == data['correct_answer']:
            answer = "True"
            data['consecutive_questions'] += 1
            data['correct_answers'] += 1
            current_level = data['levels'][-1]
            data['level_correct_count'][current_level]['correct'] += 1
        else:
            data['consecutive_questions'] = max(0, data['consecutive_questions'] - 1)

        current_level = data['levels'][-1]
        data['level_correct_count'][current_level]['total'] += 1

        if data['level_correct_count'][current_level]['total'] == data['words_count']:
            await msg.delete()
            tg_user = json.loads(
                requests.get(url=f"http://127.0.0.1:8003/api/telegram-users/chat_id/{msg.from_user.id}/").content)

            user_level = determine_final_level(data['level_correct_count'])
            level_percentages = calculate_level_percentages(data['level_correct_count'])
            levels_info = "\n".join(
                [f"{level.upper()}: {percent}%" for level, percent in level_percentages.items() if
                 level in data['levels']])

            if tg_user['language'] == 'uz':
                await msg.answer(
                    text=f"Siz barcha testni tugatdingiz 🎉\n\nDarajalar:\n{levels_info}\n\nUmumiy darajangiz: {user_level.upper()}",
                    reply_markup=await main_menu_buttons(msg.from_user.id))
            elif tg_user['language'] == 'ru':
                await msg.answer(
                    text=f"Вы прошли весь тест 🎉\n\nУровни:\n{levels_info}\n\nВаш общий уровень: {user_level.upper()}",
                    reply_markup=await main_menu_buttons(msg.from_user.id)
                )
            else:
                await msg.answer(
                    text=f"You have completed all tests 🎉\n\nLevels:\n{levels_info}\n\nYour overall level: {user_level.upper()}",
                    reply_markup=await main_menu_buttons(msg.from_user.id)
                )
            await state.finish()
        else:
            new_level = await adjust_level(consecutive_questions=data['consecutive_questions'])
            word, all_words = await get_test(level=new_level, words=data['words'])
            if new_level not in data['levels']:
                data['levels'].append(new_level)
            data['word_number'] = data['word_number'] + 1
            data['words'].append(word['word']['id'])
            data['words_count'] = len(all_words)

            await msg.answer(text=f"""
{answer} answer

{data['word']} - {data['correct_answer']}

Test {data['word_number']}

Find the definition of {word['word']['word']}""",
                             reply_markup=await test_buttons(words=word))
            data['word'] = word['word']['word']
            data['correct_answer'] = word['word']['definition']
