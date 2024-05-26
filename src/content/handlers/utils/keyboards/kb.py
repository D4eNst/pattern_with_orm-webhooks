from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Keyboards can be created here (in the form of variables or functions)

# Example builder
def get_reply_kb(items: str | list):
    if isinstance(items, str):
        items = [items]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=text) for text in items]

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


# Remove keyboard
rkr = ReplyKeyboardRemove()

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
