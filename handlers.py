from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from weather import weather_api
from keyboards import (
    get_main_keyboard,
    get_cancel_keyboard,
    get_addresses_keyboard,
    get_confirmation_keyboard,
)
from states import WeatherStates


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    if not user:
        return
    db.add_user(user_id=user.id, username=user.username, first_name=user.first_name)

    await message.answer(
        f"👋 Hello, {user.first_name or 'friend'}!\n\n"
        "I'm a weather bot. I can show you the weather in any city.\n\n"
        "📍 You can save addresses and quickly get weather for them.\n\n"
        "Use buttons below to interact with me:",
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
<b>How to use this bot:</b>
<b>Get Weather</b> - Enter city name to get current weather
<b>My Addresses</b> - View saved addresses and get weather
<b>Add Address</b> - Save a new address for quick access
<b>Delete Address</b> - Remove saved address (click trash icon)
<i>Just type a city name to get weather instantly!</i>
"""
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text == "Get Weather")
async def btn_get_weather(message: Message, state: FSMContext):
    await message.answer(
        "Enter city name to get weather:", reply_markup=get_cancel_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_address)


@router.message(F.text == "My Addresses")
async def btn_my_addresses(message: Message):
    if not message.from_user:
        return

    addresses = db.get_user_addresses(message.from_user.id)

    if not addresses:
        await message.answer(
            "📭 You don't have any saved addresses yet.\n\n"
            "Use Add Address button to save your first address!",
            reply_markup=get_main_keyboard(),
        )
        return

    await message.answer(
        f"📍 Your saved addresses ({len(addresses)}):\n\n"
        "Click on address to get weather or 🗑 to delete:",
        reply_markup=get_addresses_keyboard(addresses),
    )


@router.message(F.text == "Add Address")
async def btn_add_address(message: Message, state: FSMContext):
    await message.answer(
        "📝 Enter city or address to save:", reply_markup=get_cancel_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_address)


@router.message(F.text == "Help")
async def btn_help(message: Message):
    await cmd_help(message)


@router.message(F.text == "Cancel")
async def btn_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(" Cancelled.", reply_markup=get_main_keyboard())


@router.message(StateFilter(WeatherStates.waiting_for_address))
async def process_address(message: Message, state: FSMContext):
    if not message.from_user or not message.text:
        return

    city = message.text.strip()

    # Get weather
    weather_data = await weather_api.get_weather(city)

    if "error" in weather_data:
        await message.answer(weather_data["error"], reply_markup=get_cancel_keyboard())
        return

    # Send weather
    weather_message = weather_api.format_message(weather_data)
    await message.answer(weather_message, parse_mode="HTML")

    # Ask to save
    addresses = db.get_user_addresses(message.from_user.id)

    # Check existing address
    address_exists = any(addr[1].lower() == city.lower() for addr in addresses)

    if not address_exists:
        # Save if not exist
        db.add_address(message.from_user.id, city)
        await message.answer(
            f" Address '{city}' has been saved!", reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "This address is already saved.", reply_markup=get_main_keyboard()
        )
    await state.clear()


@router.callback_query(F.data.startswith("weather:"))
async def callback_get_weather(callback: CallbackQuery):
    if not callback.message or not callback.from_user or not callback.data:
        return

    address_id = int(callback.data.split(":")[1])
    addresses = db.get_user_addresses(callback.from_user.id)

    # Находим нужный адрес
    city = None
    for addr in addresses:
        if addr[0] == address_id:
            city = addr[1]
            break

    if not city:
        await callback.answer(" Address not found!", show_alert=True)
        return

    weather_data = await weather_api.get_weather(city)
    if "error" in weather_data:
        await callback.answer(weather_data["error"], show_alert=True)
        return

    weather_message = weather_api.format_message(weather_data)
    await callback.message.answer(weather_message, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("delete:"))
async def callback_delete_address(callback: CallbackQuery):
    if not callback.message or not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    address_id = int(callback.data.split(":")[1])

    await callback.message.edit_text(
        " Are you sure you want to delete this address?",
        reply_markup=get_confirmation_keyboard(address_id),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete:"))
async def callback_confirm_delete(callback: CallbackQuery):
    if not callback.message or not callback.from_user or not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    address_id = int(callback.data.split(":")[1])

    success = db.delete_users_addresses(address_id, callback.from_user.id)

    if success:
        await callback.message.edit_text(" Address deleted successfully!")
        await callback.answer("Deleted!", show_alert=False)
    else:
        await callback.message.edit_text("Failed to delete address.")
        await callback.answer("Error!", show_alert=True)


@router.callback_query(F.data == "cancel_delete")
async def callback_cancel_delete(callback: CallbackQuery):
    if not callback.message or not callback.from_user:
        return

    if not isinstance(callback.message, Message):
        return

    addresses = db.get_user_addresses(callback.from_user.id)

    await callback.message.edit_text(
        f"Your saved addresses ({len(addresses)}):\n\n"
        "Click on address to get weather or 🗑 to delete:",
        reply_markup=get_addresses_keyboard(addresses),
    )

    await callback.answer("Cancelled")


@router.message(
    ~F.text.in_(["Get Weather", "My Addresses", "Add Address", "Help", "Cancel"])
)
async def handle_text(message: Message):

    if not message.text or not message.from_user:
        return

    city = message.text.strip()

    # Получаем погоду
    weather_data = await weather_api.get_weather(city)

    if "error" in weather_data:
        await message.answer(
            weather_data["error"] + "\n\nUse buttons to navigate.",
            reply_markup=get_main_keyboard(),
        )
        return

    # Отправляем погоду
    weather_message = weather_api.format_message(weather_data)
    await message.answer(
        weather_message, parse_mode="HTML", reply_markup=get_main_keyboard()
    )
