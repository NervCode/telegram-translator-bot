from io import BytesIO

from aiogram.types import BufferedInputFile
from googletrans import Translator
from gtts import gTTS


async def translate(text: str, language: str) -> str:
    async with Translator() as translator:
        translated = await translator.translate(text, language)
        return translated.text


def text_to_audio(text: str, language: str) -> BufferedInputFile:
    with BytesIO() as buffer:
        tts = gTTS(text, lang=language)
        tts.write_to_fp(buffer)
        buffer.seek(0)
        value = buffer.getvalue()
        return BufferedInputFile(value, 'audio.mp3')
