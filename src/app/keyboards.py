from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.app.values import languages

inline_start_language = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=languages['ru'], callback_data='ru'),
     InlineKeyboardButton(text=languages['en'], callback_data='en')],
    [InlineKeyboardButton(text=languages['es'], callback_data='es'),
     InlineKeyboardButton(text=languages['fr'], callback_data='fr')]
])

inline_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Activate audio translation🔈',
        callback_data='audio_on'
    )],
    [InlineKeyboardButton(
        text='Deactivate audio translation🔇',
        callback_data='audio_off'
    )]
])
