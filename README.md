# nonebot-plugin-asf

NoneBot plugin for controlling ArchiSteamFarm through Telegram and ASF IPC.

## Runtime Model

Load `nonebot_plugin_asf` from a NoneBot app. The plugin handles Telegram Bot
API long polling directly and forwards authorized `!` commands to ASF IPC.

## Configuration

Set these environment variables:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_PROXY`, optional HTTP or SOCKS proxy URL for Telegram API access
- `TELEGRAM_ALLOWED_USER_IDS`, comma-separated Telegram user IDs
- `TELEGRAM_ALLOWED_CHAT_IDS`, optional comma-separated chat IDs
- `ASF_BASE_URL`, default `http://asf:1242`
- `ASF_IPC_PASSWORD`
- `POLL_TIMEOUT_SECONDS`, default `45`

At least one of `TELEGRAM_ALLOWED_USER_IDS` or `TELEGRAM_ALLOWED_CHAT_IDS` must
be set.

## Usage

- `/help` shows wrapper usage.
- `/commands` lists ASF commands and is registered in Telegram's bot menu.
- ASF commands require `!`, for example `!status`.
