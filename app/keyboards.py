from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.values import languages

inline_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=languages['ru'], callback_data='ru'),
     InlineKeyboardButton(text=languages['en'], callback_data='en')],
    [InlineKeyboardButton(text=languages['es'], callback_data='es'),
     InlineKeyboardButton(text=languages['fr'], callback_data='fr')]
])

inline_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text='Enable audio speaker🔈',
        callback_data='on'
    )],
    [InlineKeyboardButton(
        text='Disable audio speaker🔇',
        callback_data='off'
    )]
])
