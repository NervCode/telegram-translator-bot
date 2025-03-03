from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.keyboards import inline_start
from app.values import languages, speaker_value
import app.keyboards as keyboards
from app.transcribation import translate, text_to_audio

router = Router()


class States:
    ON = 'on'
    OFF = 'off'
    LANGUAGE = 'language'
    SPEAKER = 'speaker'
    WAIT = 'wait'


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        text='This is a translating bot,'
             ' send him any message and he will translate it'
             ' on selected language\nSettings: /settings',
        reply_markup=keyboards.inline_start
    )


@router.message(Command('settings'))
async def settings_command(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = data.get(States.LANGUAGE, 'en')
    speaker = data.get(States.SPEAKER, States.ON)

    await message.answer(
        text=f'Bot settings\n'
             f'Selected language: {languages[language]}'
             f'Audio speaker: {speaker}',
        reply_markup=keyboards.inline_settings
    )


@router.message(Command('language'))
async def language_command(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    language = data.get(States.LANGUAGE, 'en')

    await message.answer(
        text=f'You can change the language using the buttons below,'
             f' currently {languages[language]} is selected',
        reply_markup=inline_start
    )


@router.message(F.text)
async def translate_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if data.get(States.WAIT, False):
        await message.answer('Please wait... You already send the request')
        return

    await state.update_data(wait=True)
    await message.bot.send_chat_action(message.chat.id, 'typing')

    language = data.get(States.LANGUAGE, 'en')
    speaker = data.get(States.SPEAKER, States.ON)
    translated_text = await translate(message.text, language)

    if speaker == States.ON:
        audio_bytes = text_to_audio(message.text, language)
        audio = BufferedInputFile(audio_bytes, 'audio.mp3')

        await message.answer_voice(voice=audio, caption=translated_text)
    else:
        await message.answer(text=translated_text)

    await state.update_data(wait=False)


@router.callback_query(F.data.in_(('ru', 'en', 'es', 'fr')))
async def change_language_callback(callback: CallbackQuery,
                                   state: FSMContext) -> None:
    language: str = callback.data
    await state.update_data(language=language)

    await callback.answer()
    await callback.message.answer(
        f'All next messages will be translated on {languages[language]}'
    )


@router.callback_query(F.data.in_(('on', 'off')))
async def change_speaker_callback(callback: CallbackQuery,
                                  state: FSMContext) -> None:
    speaker: str = callback.data
    await state.update_data(speaker=speaker)

    await callback.answer()
    await callback.message.answer(
        speaker_value[speaker]
    )
