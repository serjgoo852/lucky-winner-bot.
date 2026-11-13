# Lucky Winner Telegram Bot

Telegram bot: [@LuckyWinner_GlobalBot](https://t.me/LuckyWinner_GlobalBot)

## Requirements

- Python 3.10 or newer
- A Telegram bot token created with BotFather

## Install

```bash
python -m pip install -r requirements.txt
```

## Configure the token

The bot reads its token from the `BOT_TOKEN` environment variable.

**Do not write the real token in `main.py`, `README.md`, or any other repository file.**
Do not send the token in chat or commit it to GitHub.

For local testing, set the environment variable before starting the bot:

PowerShell:
```powershell
$env:BOT_TOKEN="PASTE_YOUR_TOKEN_IN_YOUR_TERMINAL_ONLY"
python main.py
```

On DADA Cloud, open the app's environment/settings section, add or update the variable:
- Name: `BOT_TOKEN`
- Value: your current BotFather token (without quotes or spaces)

Save the settings and restart the app.

## Run

```bash
python main.py
```

Then open the bot in Telegram and send `/start`.

## Current features

- Welcome screen
- Russian, English, and German interface
- Main menu buttons
- Help command

Giveaway creation is not implemented yet; the menu item currently displays a placeholder message.
