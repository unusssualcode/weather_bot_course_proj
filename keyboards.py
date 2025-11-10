from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

MAIN_BUTTON_GET_WEATHER = "🌤 Get Weather"
MAIN_BUTTON_MY_ADDRESSES = "📍 My Addresses"
MAIN_BUTTON_ADD_ADDRESS = "➕ Add Address"
MAIN_BUTTON_HELP = "ℹ️ Help"
MAIN_BUTTON_CANCEL = "❌ Cancel"


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=MAIN_BUTTON_GET_WEATHER),
            KeyboardButton(text=MAIN_BUTTON_MY_ADDRESSES),
        ],
        [
            KeyboardButton(text=MAIN_BUTTON_ADD_ADDRESS),
            KeyboardButton(text=MAIN_BUTTON_HELP),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Choose an action..."
    )

    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=MAIN_BUTTON_CANCEL)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Enter address or cancel...",
    )
    return keyboard


def get_addresses_keyboard(addresses: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for addr_id, address, created_at in addresses:
        builder.button(text=f"🌡 {address}", callback_data=f"weather:{addr_id}")
        builder.button(text="🗑", callback_data=f"delete:{addr_id}")

    builder.adjust(2)
    return builder.as_markup()


def get_confirmation_keyboard(address_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=" Yes, delete", callback_data=f"confirm_delete:{address_id}")
    builder.button(text=" Cancel", callback_data="cancel_delete")

    builder.adjust(2)

    return builder.as_markup()
