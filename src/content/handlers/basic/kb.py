from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# Inline keyboards can be created here (in the form of variables or functions)

# Example inline keyboard:
# def arrows() -> InlineKeyboardMarkup:
#     ikb_builder = InlineKeyboardBuilder()
#
#     ikb_builder.button(text="⬅", callback_data="arrow_back")
#     ikb_builder.button(text="➡", callback_data="arrow_next")
#
#     return ikb_builder.as_markup()


# Example builder
# def get_reply_kb(items: str | list):
#     if isinstance(items, str):
#         items = [items]
#
#     builder = ReplyKeyboardBuilder()
#     [builder.button(text=text) for text in items]
#
#     return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


# Remove keyboard
# rkr = ReplyKeyboardRemove()

# Example keyboard:
# def main_menu_btn() -> ReplyKeyboardMarkup:
#     keyboard = ReplyKeyboardMarkup(keyboard=[
#         [
#             KeyboardButton(
#                 text="text"
#             ),
#         ]
#     ], resize_keyboard=True)
#     return keyboard
#
# or a variable:
# main_kb = main_menu_btn()
