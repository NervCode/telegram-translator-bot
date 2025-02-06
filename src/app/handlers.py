import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.app.values import languages, audio_value
import src.app.keyboards as keyboards

from googletrans import Translator
from gtts import gTTS

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        text='This is a translator bot.\nSend any message to him,'
             'and he will translate it into the chosen language.\n'
             'Settings: /settings\nChange language: /language',
        reply_markup=keyboards.inline_start_language
    )


@router.message(Command('settings'))
async def settings_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = languages[data.get('language', 'en')]
    speaker = data.get('speaker', 'on')

    await message.answer(
        text=f'Bot settings\n'
             f'Selected language: {language}\n'
             f'Audio speaker: {speaker}\n',
        reply_markup=keyboards.inline_settings
    )


@router.message(Command('language'))
async def language_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = data.get('language', 'en')

    await message.answer(
        text=f'Select the language for translation,'
             f' currently it is set to {languages[language]}',
        reply_markup=keyboards.inline_start_language
    )


@router.message()
async def translate_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if data.get('wait', False):
        await message.answer('You have already sent the request, please wait')
        return None

    await state.update_data(wait=True)
    translating_message = await message.answer('Translating... ')

    user_id = str(message.from_user.id)
    language = data.get('language', 'en')
    audio = data.get('audio', 'on')

    # Translating
    async with Translator() as translator:
        translated_text = await translator.translate(
            text=message.text,
            dest=language
        )

    # Sending message
    if audio == 'on':
        gtts = gTTS(translated_text.text, lang=language)
        gtts.save(f'audio{user_id}.mp3')
        voice = FSInputFile(f'audio{user_id}.mp3')

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

    await state.update_data(wait=False)


@router.callback_query(F.data == 'ru')
async def ru_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='ru')

    await callback.answer()
    await callback.message.answer(
        f'All following messages will be translated into {languages['ru']}'
    )


@router.callback_query(F.data == 'en')
async def en_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='en')

    await callback.answer()
    await callback.message.answer(
        f'All following messages will be translated into {languages['en']}'
    )


@router.callback_query(F.data == 'es')
async def es_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='es')

    await callback.answer()
    await callback.message.answer(
        f'All following messages will be translated into {languages['es']}'
    )


@router.callback_query(F.data == 'fr')
async def fr_language_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language='fr')

    await callback.answer()
    await callback.message.answer(
        f'All following messages will be translated into {languages['fr']}'
    )


@router.callback_query(F.data == 'audio_on')
async def speaker_on_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(audio='on')

    await callback.answer()
    await callback.message.answer(
        audio_value['on']
    )


@router.callback_query(F.data == 'audio_off')
async def speaker_off_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(audio='off')

    await callback.answer()
    await callback.message.answer(
        audio_value['off']
    )
