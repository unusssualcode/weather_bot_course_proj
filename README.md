# Weather Bot

A Telegram assistant that delivers real-time weather updates, manages your frequently used locations, and keeps the conversation friendly. Built with Aiogram 3, SQLite, and the OpenWeather API.

## Key Features
- Onboard users instantly with `/start` and persist their profile in SQLite.
- Fetch real-time weather conditions for any city using OpenWeather.
- Save, list, and remove frequently used locations with inline keyboards.
- Offer guided workflows via custom reply keyboards and FSM states.
- Provide robust error messaging for invalid input, API failures, and missing credentials.

## Architecture Overview
The bot is organised into discrete modules to keep concerns separated and extensible:
- `main.py`: entry point, dispatcher wiring, and lifecycle hooks.
- `handlers.py`: command handlers, button callbacks, and FSM transitions.
- `database.py`: lightweight SQLite wrapper responsible for users and addresses.
- `weather.py`: asynchronous OpenWeather client plus message formatting.
- `keyboards.py`: reply and inline keyboard factories.
- `states.py`: finite state machine definition for interactive flows.
- `config.py`: environment loader that validates tokens.

SQLite is used for persistence, while OpenWeather supplies weather data. Aiogram 3 handles the Telegram bot runtime with asynchronous updates.

## Requirements
- Python 3.13+
- OpenWeather API key
- Telegram Bot token (via BotFather)

All Python dependencies are listed in `requirements.txt`.

## Quick Start
1. **Clone the repository**
   ```bash
git clone https://github.com/your-org/weather_bot.git
cd weather_bot
   ```
2. **Create a virtual environment**
   ```bash
python3 -m venv .venv
source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
pip install -r requirements.txt
   ```
4. **Provide environment variables** by creating a `.env` file in the project root:
   ```bash
BOT=1234567890:your-telegram-bot-token
WEATHER_API_KEY=your-openweather-api-key
   ```
5. **Run the bot**
   ```bash
python main.py
   ```

On first launch the bot will create `weather_bot.db` with the required tables.

## Runtime Configuration
- `BOT`: Telegram bot token obtained from BotFather.
- `WEATHER_API_KEY`: OpenWeather API key (metric units are used).

`config.py` loads the values and raises an error if either is missing, ensuring misconfiguration is caught early.

## Database Notes
- Uses SQLite (`weather_bot.db`) located in the project root.
- Table `users` stores Telegram user metadata.
- Table `user_addresses` persists saved locations linked to user IDs.
- Tables are created automatically during `on_startup()`.

No manual migrations are required. Back up or remove `weather_bot.db` to reset state.

## Bot Usage
### Commands
- `/start`: registers the user and displays the main menu.
- `/help`: shows concise usage instructions and button descriptions.

### Main Menu Buttons
- `Get Weather`: prompts for a city name and returns formatted weather data.
- `My Addresses`: lists saved locations with buttons to fetch or delete weather entries.
- `Add Address`: saves a new city/address and immediately fetches its conditions.
- `Help`: mirrors `/help` for quick access.
- `Cancel`: exits the current flow and restores the main menu.

### Inline Actions
- `🌡 city`: fetches weather for the selected saved address.
- `🗑`: triggers a confirmation dialog before deleting the address.
- `Yes, delete`: removes the address from storage.
- `Cancel`: aborts the deletion and reloads the saved addresses list.

Messages are enriched with emojis and HTML formatting to improve readability. FSM states ensure that user input is validated before saving addresses or making API calls.

## Error Handling
The bot responds with descriptive messages when:
- A city cannot be found (`404` from OpenWeather).
- The API key is invalid (`401`).
- Network errors occur during the HTTP request.
- SQLite operations fail during save or delete actions.

Errors are logged via Python's `logging` subsystem to aid debugging.

## Extending the Bot
- Add new commands by registering handlers in `handlers.py` and updating keyboards accordingly.
- Expand persistence by augmenting `Database` with additional tables or queries.
- Introduce scheduled forecasts by adding background tasks inside `main.py` (e.g., using `asyncio.create_task`).

## Troubleshooting
- **`ValueError: BOT_TOKEN not found in .env file`**: ensure `.env` exists and the token is spelled correctly.
- **`Invalid API key`**: verify `WEATHER_API_KEY` matches the one from OpenWeather.
- **`Connection error`**: check network connectivity or firewall settings.
- **`Address not found`**: confirm the location spelling; the bot preserves the raw string to simplify matching.

Restart the bot after updating environment variables or dependencies.

## Deployment Tips
- Use systemd, Docker, or a process manager (e.g., Supervisor) to keep the bot running.
- Secure `.env` and database files with restricted file permissions.
- Regularly rotate tokens and backup `weather_bot.db` if persistent history matters.

## License
Specify your project license here (e.g., MIT, Apache 2.0). If none is provided, clarify that the project is currently unlicensed.
