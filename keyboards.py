
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import INSTAGRAM_URL, TG_CHANNEL_URL
from aiogram.utils.keyboard import InlineKeyboardBuilder
def contact_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="☎️Kontaktni ulashish", request_contact=True))
    
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
def  subs_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="↗️Instagram",url=INSTAGRAM_URL),
        InlineKeyboardButton(text="↗️Telegram",url=TG_CHANNEL_URL),

        InlineKeyboardButton(text="✅Tekshirish",callback_data="check"),
    )
    builder.adjust(1)
    return builder.as_markup()