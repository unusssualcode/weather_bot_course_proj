# ⛅️ Weather Bot

[![Aiogram](https://img.shields.io/badge/Aiogram-3.22-2b5278)](https://docs.aiogram.dev/)
[![Python](https://img.shields.io/badge/Python-3.13%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![OpenWeather](https://img.shields.io/badge/OpenWeather-API-orange)](https://openweathermap.org/api)
[![SQLite](https://img.shields.io/badge/SQLite-embedded-003b57?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)

> 🌍 A Telegram companion that delivers live weather briefings, remembers your go-to spots, and keeps conversations delightful.

## ✨ Highlights
- ⚡️ Instant onboarding with `/start`, persisting Telegram profiles in SQLite.
- 🌦 Real-time city forecasts powered by the OpenWeather API.
- 📍 Smart address book with save, list, and delete controls via inline keyboards.
- 🧭 Guided journeys using reply keyboards and AIogram FSM states.
- 🛡 Defensive messaging for invalid input, API issues, and credential problems.

## 🧱 Architecture
- `main.py`: dispatcher bootstrap, lifecycle hooks, logging.
- `handlers.py`: slash commands, button callbacks, FSM transitions.
- `database.py`: SQLite wrapper for users and saved addresses.
- `weather.py`: async OpenWeather client and HTML-rich message builder.
- `keyboards.py`: reply/inline keyboard factories.
- `states.py`: FSM definition for conversational steps.
- `config.py`: dotenv loader that validates required tokens.

> 🧩 Storage is handled by SQLite, weather data by OpenWeather, and the dialogue engine by Aiogram 3.

## 📦 Requirements
- Python 3.13+
- Telegram bot token (BotFather)
- OpenWeather API key
- Dependencies listed in `requirements.txt`

## 🚀 Quick Start
1. **Clone**
   ```bash
git clone https://github.com/your-org/weather_bot.git
cd weather_bot
   ```
2. **Create venv**
   ```bash
python3 -m venv .venv
source .venv/bin/activate
   ```
3. **Install deps**
   ```bash
pip install -r requirements.txt
   ```
4. **Configure `.env`**
   ```bash
BOT=1234567890:your-telegram-bot-token
WEATHER_API_KEY=your-openweather-api-key
   ```
5. **Launch**
   ```bash
python main.py
   ```

> 🗄 First run will initialise `weather_bot.db` with all tables.

## ⚙️ Runtime Variables
- `BOT`: Telegram bot token.
- `WEATHER_API_KEY`: OpenWeather credential (metric mode).

`config.py` aborts early if either value is missing, preventing silent failures.

## 🗃 Database Snapshot
- `users`: Telegram user metadata and timestamps.
- `user_addresses`: saved locations bound to user IDs.
- Schema auto-creates during `on_startup()`.

Reset the bot by removing `weather_bot.db` (a new one will be generated).

## 💬 Bot Usage
### 🧾 Commands
- `/start`: greets and renders the main menu.
- `/help`: displays quick guidance and button actions.

### 🕹 Main Menu Buttons
- `🌤 Get Weather`: asks for a city and returns a formatted forecast.
- `📍 My Addresses`: lists saved spots with quick weather/delete buttons.
- `➕ Add Address`: saves a location and fetches its weather instantly.
- `ℹ️ Help`: mirrors `/help` for convenience.
- `❌ Cancel`: exits current flow and restores the main menu.

### 🔄 Inline Controls
- `🌡 city`: fetches stored-location weather.
- `🗑`: prompts a confirmation dialog before deletion.
- `Yes, delete`: removes the address.
- `Cancel`: aborts deletion and reloads the list.

## 🎞 Flow Highlights
```
🌅 0s  → User taps /start
💬 1s  → Bot greets and shows menu
🌤 3s  → User selects Get Weather
🔍 5s  → Address submitted, API queried
📦 7s  → Forecast delivered with HTML styling
📌 9s  → Location autosaved for future use
```

> 🧠 FSM guards each step so inputs are validated before database or API work happens.

## 🚨 Error Handling
- ❌ City not found (`404` from OpenWeather).
- 🔐 Invalid API key (`401`).
- 🌐 Network-level issues handled via `aiohttp` exceptions.
- 🧱 SQLite insert/delete failures reported gracefully.

All events are logged with Python `logging` for easier diagnostics.

## 🛠 Extending
- ➕ Register new handlers in `handlers.py`, update keyboards, and reuse FSM states.
- 🗄 Enhance persistence by expanding `Database` with extra tables or indexes.
- 📅 Schedule forecasts via background tasks (e.g., `asyncio.create_task`).

## 🧯 Troubleshooting
| Issue | Fix |
| --- | --- |
| `ValueError: BOT_TOKEN not found` | Confirm `.env` exists and contains a valid token. |
| `Invalid API key` response | Reissue OpenWeather key and update `.env`. |
| `Connection error` | Check network reachability and firewall rules. |
| Address not removed | Ensure callback data matches an existing entry; retry after refresh. |

> ♻️ Restart the bot after updating environment variables or packages.

## 🌐 Deployment Tips
- 🧠 Run under systemd, Docker, or Supervisor for automatic restarts.
- 🔒 Keep `.env` and `weather_bot.db` outside public directories; restrict file permissions.
- ♻️ Rotate tokens regularly; back up the SQLite database if historical data matters.

## 📜 License
Specify the licence that applies to this project (e.g., MIT, Apache 2.0). Without an explicit licence, usage defaults to **all rights reserved**.
