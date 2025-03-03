from io import BytesIO

from googletrans import Translator
from gtts import gTTS


async def translate(text: str, language: str) -> str:
    async with Translator() as translator:
        translated = await translator.translate(text, language)
        return translated.text


def text_to_audio(text: str, language: str) -> bytes:
    with BytesIO() as buffer:
        tts = gTTS(text, lang=language)
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.getvalue()
