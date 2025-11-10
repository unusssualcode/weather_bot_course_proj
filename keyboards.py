from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🌤 Get Weather"), KeyboardButton(text="📍 My Addresses")],
        [KeyboardButton(text="➕ Add Address"), KeyboardButton(text="ℹ️ Help")],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Choose an action..."
    )

    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text="❌ Cancel")]]
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
