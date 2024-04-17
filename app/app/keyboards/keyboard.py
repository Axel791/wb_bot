from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

get_stat_btn = InlineKeyboardButton(text="Получить статистику", callback_data="get_stat")
yes_btn = InlineKeyboardButton(text="Да", callback_data="yes")
no_btn = InlineKeyboardButton(text="Нет", callback_data="no")
cancel_btn = InlineKeyboardButton(text="Отмена", callback_data="cancel")

stat_kb = InlineKeyboardMarkup(inline_keyboard=[[get_stat_btn]])
yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[[yes_btn, no_btn, cancel_btn]])
cancel_kb = InlineKeyboardMarkup(inline_keyboard=[[cancel_btn]])
