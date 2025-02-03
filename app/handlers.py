import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.values import languages, speaker_value
import app.keyboards as keyboards

from googletrans import Translator
from gtts import gTTS

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        text='Это бот переводчик. Выберите язык, на который переводить',
        reply_markup=keyboards.inline_start
    )


@router.message(Command('settings'))
async def settings_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = languages[data.get('language', 'en')]
    speaker = speaker_value[data.get('speaker', 'on')]

    await message.answer(
        text=f'Настройки переводчика'
             f'\nПереводит: Auto'
             f'\nПереводит на: {language}'
             f'\nДиктор: {speaker}',
        reply_markup=keyboards.inline_settings
    )


@router.message()
async def translate_handler(message: Message, state: FSMContext) -> None:
    loading_message = await message.answer('Загрузка... ')

    data = await state.get_data()
    language = data.get('language', 'en')
    speaker = data.get('speaker', 'on')

    async with Translator() as translator:
        translated_text = await translator.translate(
            text=message.text,
            dest=language
        )

    if speaker == 'on':
        gtts = gTTS(translated_text.text, lang=language)
        gtts.save('voice.mp3')
        voice = FSInputFile('voice.mp3')

        await loading_message.delete()
        await message.answer_voice(
            voice=voice,
            caption=f'{message.text} | {translated_text.text}'
        )

        os.remove('voice.mp3')
    else:
        await loading_message.delete()
        await message.answer(
            text=f'{message.text} | {translated_text.text}'
        )


@router.callback_query(F.data == 'ru')
async def ru_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='ru')

    await callback.answer()
    await callback.message.answer(
        f'Все следующие сообщения будут переведены на {languages['ru']}'
    )


@router.callback_query(F.data == 'en')
async def en_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='en')

    await callback.answer()
    await callback.message.answer(
        f'Все следующие сообщения будут переведены на {languages['en']}'
    )


@router.callback_query(F.data == 'es')
async def es_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='es')

    await callback.answer()
    await callback.message.answer(
        f'Все следующие сообщения будут переведены на {languages['es']}'
    )


@router.callback_query(F.data == 'fr')
async def fr_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='fr')

    await callback.answer()
    await callback.message.answer(
        f'Все следующие сообщения будут переведены на {languages['fr']}'
    )


@router.callback_query(F.data == 'speaker_on')
async def speaker_on_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(speaker='on')

    await callback.answer()
    await callback.message.answer(
        speaker_value['on']
    )


@router.callback_query(F.data == 'speaker_off')
async def speaker_off_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(speaker='off')

    await callback.answer()
    await callback.message.answer(
        speaker_value['off']
    )

