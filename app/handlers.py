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
        text='This is a translating bot,'
             ' send him any message and he will translate it'
             ' on selected language, settings: /settings',
        reply_markup=keyboards.inline_start
    )


@router.message(Command('settings'))
async def settings_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = languages[data.get('language', 'en')]
    speaker = data.get('speaker', 'on')

    await message.answer(
        text=f'Bot settings'
             f'Selected language: {language}'
             f'Audio speaker: {speaker}',
        reply_markup=keyboards.inline_settings
    )


@router.message()
async def translate_handler(message: Message, state: FSMContext) -> None:
    translating_message = await message.answer('Translating... ')

    data = await state.get_data()
    language = data.get('language', 'en')
    speaker = data.get('speaker', 'on')

    # Translating
    async with Translator() as translator:
        translated_text = await translator.translate(
            text=message.text,
            dest=language
        )

    # Send message
    if speaker == 'on':
        gtts = gTTS(translated_text.text, lang=language)
        gtts.save('audio.mp3')
        voice = FSInputFile('audio.mp3')

        await translating_message.delete()
        await message.answer_voice(
            voice=voice,
            caption=translated_text.text
        )

        os.remove('audio.mp3')
    else:
        await translating_message.delete()
        await message.answer(
            text=translated_text.text
        )


@router.callback_query(F.data == 'ru')
async def ru_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='ru')

    await callback.answer()
    await callback.message.answer(
        f'All next messages will be translated on {languages['ru']}'
    )


@router.callback_query(F.data == 'en')
async def en_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='en')

    await callback.answer()
    await callback.message.answer(
        f'All next messages will be translated on {languages['en']}'
    )


@router.callback_query(F.data == 'es')
async def es_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='es')

    await callback.answer()
    await callback.message.answer(
        f'All next messages will be translated on {languages['es']}'
    )


@router.callback_query(F.data == 'fr')
async def fr_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='fr')

    await callback.answer()
    await callback.message.answer(
        f'All next messages will be translated on {languages['fr']}'
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
